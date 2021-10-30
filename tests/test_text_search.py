import pytest

from kawadi.text_search import SearchInText


@pytest.fixture()
def input_data():
    text_to_find = "String distance algorithm"
    text_to_search = """SIFT4 is a general purpose string distance algorithm inspired by JaroWinkler and Longest Common Subsequence. It was developed to produce a distance measure that matches as close as possible to the human perception of string distance. Hence it takes into account elements like character substitution, character distance, longest common subsequence etc. It was developed using experimental testing, and without theoretical background."""

    return text_to_find, text_to_search


@pytest.fixture()
def output():
    return [
        {
            "sim_score": 1.0,
            "searched_text": "string distance algorithm",
            "to_find": "string distance algorithm",
            "start": 27,
            "end": 52,
        }
    ]


def test_search_in_text(input_data, output) -> None:
    search_text = SearchInText()
    result = search_text.find_in_text(input_data[0], input_data[1])
    assert output == result

    # test multiprocessing
    search_text = SearchInText(multiprocessing=True, max_workers=4)
    result = search_text.find_in_text(input_data[0], input_data[1])
    assert output == result

    # test threshold
    search_text = SearchInText(
        search_threshold=0.99, multiprocessing=True, max_workers=4
    )
    result = search_text.find_in_text("something stupid", input_data[1])
    assert result == []
