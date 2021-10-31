# kawadi

[![Build Status](https://github.com/jdvala/kawadi/workflows/Build%20main/badge.svg)](https://github.com/jdvala/kawadi/actions)
[![Code Coverage](https://codecov.io/gh/jdvala/kawadi/branch/main/graph/badge.svg)](https://codecov.io/gh/jdvala/kawadi)
![kawadi](https://raw.githubusercontent.com/jdvala/kawadi/main/kawadi.png)


kawadi (કવાડિ in Gujarati) (Axe in English) is a versatile tool that used as a form of weapon and is used to cut, shape and split wood.


kawadi is collection of small tools that I found useful for me more often. Currently it contains text search which searches a string inside another string.

## Text Search
Text search in kawadi uses sliding window technique to search for a word or phrase in another text. The step size in the sliding window is 1 and the window size is the size of the word/phrase we are interested in.

For example, if the text we are interested in searching is "The big brown fox jumped over the lazy dog" and the word that we want to search is "brown fox".

```
text = "The big brown fox jumped over the lazy dog"
interested_word = "brown fox"
window_size = len(interested.split()) -> len(["brown", ["fox"]])

slides = sliding_window(text, window_size) -> ['The', 'big']['big', 'brown']['brown', 'fox']['fox', 'jumped']['jumped', 'over']['over', 'the']['the', 'lazy']['lazy', 'dog']

for each slide in slides
  score(" ".join(slide), interested_word)
  if score >= threshold then
    select slide
  else
    continue
```

Currently, there are 3 similarity scores are calculated and averaged to calculate the final score. These similarity scores are `Cosine`, `JaroWinkler` and `Normalized Levinstine` similarities.


## In development
- [x] Add functionality to accept custom user similarity metrics.
- [] Generate documentation.
- [] Write the custom counter

You can follow the project development in the Projects tab.
---

## Quick Start
```python
from kawadi.text_search import SearchInText

search = SearchInText()

text_to_find = "String distance algorithm"
text_to_search = """SIFT4 is a general purpose string distance algorithm inspired by JaroWinkler and Longest Common Subsequence. It was developed to produce a distance measure that matches as close as possible to the human perception of string distance. Hence it takes into account elements like character substitution, character distance, longest common subsequence etc. It was developed using experimental testing, and without theoretical background."""

result = search.find_in_text(text_to_find, text_to_search)

print(result)
[
    {
        "sim_score": 1.0,
        "searched_text": "string distance algorithm",
        "to_find": "string distance algorithm",
        "start": 27,
        "end": 52,
    }
]
```

If the text that needs to be searched is big, `SearchInText` can utilize `multiprocessing` to make the search fast.

```py
from kawadi.text_search import SearchInText

search = SearchInText(multiprocessing=True, max_workers=8)
```

## Custom user defined score calculation.
Its often the case that the provided string similarity score is not enough for the use case that you may have. For this very case, you can add, your own score calculation.

```py
from kawadi.text_search import SearchInText


def my_custom_fun(**kwargs):

  slide_of_text:str = kwargs["slide_of_text"]
  text_to_find:str = kwargs["text_to_find"]

  # Here you can then go on to do preprocessing if you like,
  # or use them to count char based n-gram string matching scores.

  return score: float

search = SearchInText(search_threshold=0.9, custom_score_func= your custom func)
```
This custom score function will have access to two things `slide_of_text` for every slide in text (From the example above, "The big", "big brown" and so on...) and `text_to_find`.

> Note: The return type of this custom function should be same as the type of `search_threshold` as you can see from the above example.

## Installation
**Stable Release:** `pip install kawadi`<br>
**Development Head:** `pip install git+https://github.com/jdvala/kawadi.git`


## Development
See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.


***Free software: MIT license***
