import logging
import multiprocessing as mp
import re
import typing as tt
from collections import namedtuple
from functools import partial

from strsimpy.cosine import Cosine
from strsimpy.jaro_winkler import JaroWinkler
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class SearchInText:
    """Search a string in a given text."""

    def __init__(
        self,
        score_threshold: float = 0.90,
        multiprocessing: bool = False,
        max_workers: int = 0,
        custom_score_func: tt.Callable = None,
    ):
        self.score_threshold = score_threshold
        self.multiprocessing = multiprocessing
        self.max_workers = max_workers
        self.custom_score_fun = custom_score_func
        self.jaro_winkler = JaroWinkler()
        self.normalized_levenshtein = NormalizedLevenshtein()
        self.cosine_similarity = Cosine(1)

        if self.multiprocessing:
            # check if max_workers is set
            if self.max_workers == 0:
                logger.info(
                    "Multiprocessing is enabled, but max_works is set to 0, defaulting to using all the available cores %d.",
                    mp.cpu_count(),
                )
                self.max_workers = mp.cpu_count()

    def _check_for_custom_score(self, ret_score) -> None:
        """Check if the return type of the custom score is in agreement with return type of score_threshold.

        Args:
            ret_score: Value of score from custom score function.

        Raises:
            ValueError: If the type of custom score function is different from type of score threshold.
        """
        type_of_ret_score = type(ret_score)
        type_of_score_threshold = type(self.score_threshold)

        if type_of_ret_score != type_of_score_threshold:
            raise ValueError(
                "The value returned from custom score function is of type {} and value of score_threshold is of type {} which is incompatible",
                str(type_of_ret_score),
                str(type_of_score_threshold),
            )

    def _normalize(self, text: str) -> str:
        """Normalize text before searching.

        In NLP text normalization means brining text into its basic form, here however, text normalization means that removing punctuations and lowering the text case.

        Args:
            text: Text to normalize.

        Returns:
            Normalized text.
        """
        no_punc_string = re.sub(r"[^\w\s]", "", text)
        return no_punc_string.lower()

    def _sliding_window(self, sequence: str, window_size: int, step: int):
        """Returns a generator that will iterate through the defined chunks of input sequence.

        Args:
            sequence: The text which need to chunked.
            window_size: Size of the chunks.
            step: Size of words to skip before creating window.

        Raises:
            Exception: If the type of window_size and step is not int.
            Exception: If step size is greater than window_size
            Exception: If window size is greater than the sequence.

        Yields:
            Generator with specified window_size and step.
        """
        # Verify the inputs
        if not isinstance(window_size, int) and isinstance(step, int):
            raise Exception("**ERROR** type(window_size) and type(step) must be int.")
        if step > window_size:
            raise Exception("**ERROR** step must not be larger than window_size.")
        if window_size > len(sequence):
            raise Exception(
                "**ERROR** window_size must not be larger than sequence length."
            )
        sequence = sequence.split()
        # Pre-compute number of chunks to emit
        num_of_chunks = int(((len(sequence) - window_size) / step) + 1)

        # Do the work
        for i in range(0, num_of_chunks * step, step):
            yield sequence[i : i + window_size]

    def _find_index(self, text_to_find: str, text_to_search: str):
        """Find the start and end index of searched text in the other text.

        Args:
            text_to_find: Text to be searched.
            text_to_search: Text in which the other text is to be searched.

        Returns:
            NamedTuple of with start index and end index if its found, None otherwise.
        """
        Indexes = namedtuple("Indexes", ["start", "end"])
        Indexes(None, None)
        index_search = re.compile(rf"{text_to_find}")
        result = index_search.search(text_to_search)
        if result:
            start = result.start()
            end = result.end()
            return Indexes(start, end)

    def _score(self, text: str, text_to_search: str) -> float:
        """Calculate the score based on Jaro Winkler, Normalized Levinstine and Cosine similarity.

        Args:
            text: Text to be searched.
            text_to_search: Text in which the other text is to be searched.

        Returns:
            Score of the match between text and text to search.
        """
        jaro_score = self.jaro_winkler.similarity(text, text_to_search)
        cosine_score = self.cosine_similarity.similarity(text, text_to_search)
        normalized_levinstine_score = self.normalized_levenshtein.similarity(
            text, text_to_search
        )

        average_sim_score = (
            jaro_score + cosine_score + normalized_levinstine_score
        ) / 3

        return average_sim_score

    def _cal_win_size(self, text_to_find: str) -> int:
        """Calculate window size.

        Args:
            text_to_find: Text to be searched.

        Returns:
            Window size.
        """
        return len(text_to_find.split())

    def _run_custom_score(self, func: tt.Callable, **kwargs):
        """Run the custom score function.

        Args:
            func (tt.Callable): Custom score function.
            **kwargs: Arbitrary keyword arguments

        Returns:
            score from user defined custom score function.
        """
        custom_score = func(**kwargs)
        self._check_for_custom_score(custom_score)
        return custom_score

    def _perform_search(
        self, words: tt.List, text_to_find: str, text_to_search: str
    ) -> tt.Optional[tt.Dict]:
        """Perform text search.

        Args:
            words: List of words after performing sliding window.
            text_to_find: Text to be searched in the another text.
            text_to_search: Text to be searched in.

        Returns:
            Dictionary of similarity score, searched_text, to_find, start_index, end_index if the sim_score is greater or equal to the set score_threshold.
        """
        slide_of_text = " ".join(words)
        if self.custom_score_fun:
            score = self._run_custom_score(
                self.custom_score_fun,
                slide_of_text=slide_of_text,
                text_to_find=text_to_find,
            )
        else:
            score = self._score(slide_of_text, text_to_find)
        if score >= self.score_threshold:
            # calculate the indexes
            indexes = self._find_index(text_to_find, text_to_search)

            return {
                "sim_score": score,
                "searched_text": slide_of_text,
                "to_find": text_to_find,
                "start": indexes.start,
                "end": indexes.end,
            }

    def find_in_text(self, text_to_find: str, text_to_search: str) -> tt.List:
        """Find a string in given text.

        Args:
            text_to_find: Text to be searched in the another text.
            text_to_search: Text to be searched in.

        Returns:
            All the matched text in another text, with dictionaries of similarity score, searched_text, to_find, start_index, end_index if the sim_score is greater or equal to the set score_threshold.
        """
        text_to_find = self._normalize(text_to_find)
        text_to_search = self._normalize(text_to_search)

        window_size = self._cal_win_size(text_to_find)
        textsearch_iter = self._sliding_window(
            sequence=text_to_search, window_size=window_size, step=1
        )

        if self.multiprocessing:
            pool = mp.Pool(self.max_workers)
            partial_perform_search = partial(
                self._perform_search,
                text_to_find=text_to_find,
                text_to_search=text_to_search,
            )
            scores = pool.map(partial_perform_search, textsearch_iter)

            return [score for score in scores if score]
        else:
            scores = []
            for i in textsearch_iter:
                scores.append(self._perform_search(i, text_to_find, text_to_search))
            return [score for score in scores if score]
