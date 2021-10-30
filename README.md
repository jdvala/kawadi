# kulhadi

[![Build Status](https://github.com/jdvala/kulhadi/workflows/Build%20main/badge.svg)](https://github.com/jdvala/kulhadi/actions)
[![Code Coverage](https://codecov.io/gh/jdvala/kulhadi/branch/main/graph/badge.svg)](https://codecov.io/gh/jdvala/kulhadi)
![Kulhadi](kulhadi.png)


Kulhadi (कुल्हाड़ी in Hindi) (Axe in Englsih) is a versatile tool that used as a form of weapon and is used to cut, shape and split wood.


Kulhadi is collection of small tools that I found useful for me more often. Currently it contains text search which searches a string inside another string.



---

## Quick Start
```python
from kulhadi.text_search import SearchInText

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
from kulhadi.text_search import SearchInText

search = SearchInText(multiprocessing=True, max_workers=8)
```


## Installation
**Stable Release:** `pip install kulhadi`<br>
**Development Head:** `pip install git+https://github.com/jdvala/kulhadi.git`


## Development
See [CONTRIBUTING.md](CONTRIBUTING.md) for information related to developing the code.



#### Additional Optional Setup Steps:
* Turn your project into a GitHub repository:
  * Make sure you have `git` installed, if you don't, [follow these instructions](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
  * Make an account on [github.com](https://github.com)
  * Go to [make a new repository](https://github.com/new)
  * _Recommendations:_
    * _It is strongly recommended to make the repository name the same as the Python
    package name_
    * _A lot of the following optional steps are *free* if the repository is Public,
    plus open source is cool_
  * After a GitHub repo has been created, run the following commands:
    * `git remote add origin git@github.com:jdvala/kulhadi.git`
    * `git push -u origin master`
* Register kulhadi with Codecov:
  * Make an account on [codecov.io](https://codecov.io)
  (Recommended to sign in with GitHub)
  * Select `jdvala` and click: `Add new repository`
  * Copy the token provided, go to your [GitHub repository's settings and under the `Secrets` tab](https://github.com/jdvala/kulhadi/settings/secrets),
  add a secret called `CODECOV_TOKEN` with the token you just copied.
  Don't worry, no one will see this token because it will be encrypted.
* Generate and add an access token as a secret to the repository for auto documentation
generation to work
  * Go to your [GitHub account's Personal Access Tokens page](https://github.com/settings/tokens)
  * Click: `Generate new token`
  * _Recommendations:_
    * _Name the token: "Auto-Documentation Generation" or similar so you know what it
    is being used for later_
    * _Select only: `repo:status`, `repo_deployment`, and `public_repo` to limit what
    this token has access to_
  * Copy the newly generated token
  * Go to your [GitHub repository's settings and under the `Secrets` tab](https://github.com/jdvala/kulhadi/settings/secrets),
  add a secret called `ACCESS_TOKEN` with the personal access token you just created.
  Don't worry, no one will see this password because it will be encrypted.
* Register your project with PyPI:
  * Make an account on [pypi.org](https://pypi.org)
  * Go to your [GitHub repository's settings and under the `Secrets` tab](https://github.com/jdvala/kulhadi/settings/secrets),
  add a secret called `PYPI_TOKEN` with your password for your PyPI account.
  Don't worry, no one will see this password because it will be encrypted.
  * Next time you push to the branch: `stable`, GitHub actions will build and deploy
  your Python package to PyPI.
  * _Recommendation: Prior to pushing to `stable` it is recommended to install and run
  `bumpversion` as this will,
  tag a git commit for release and update the `setup.py` version number._
* Add branch protections to `master` and `stable`
    * To protect from just anyone pushing to `master` or `stable` (the branches with
    more tests and deploy
    configurations)
    * Go to your [GitHub repository's settings and under the `Branches` tab](https://github.com/jdvala/kulhadi/settings/branches), click `Add rule` and select the
    settings you believe best.
    * _Recommendations:_
      * _Require pull request reviews before merging_
      * _Require status checks to pass before merging (Recommended: lint and test)_

#### Suggested Git Branch Strategy
1. `master` is for the most up-to-date development, very rarely should you directly
commit to this branch. GitHub Actions will run on every push and on a CRON to this
branch but still recommended to commit to your development branches and make pull
requests to master.
2. `stable` is for releases only. When you want to release your project on PyPI, simply
make a PR from `master` to `stable`, this template will handle the rest as long as you
have added your PyPI information described in the above **Optional Steps** section.
3. Your day-to-day work should exist on branches separate from `master`. Even if it is
just yourself working on the repository, make a PR from your working branch to `master`
so that you can ensure your commits don't break the development head. GitHub Actions
will run on every push to any branch or any pull request from any branch to any other
branch.
4. It is recommended to use "Squash and Merge" commits when committing PR's. It makes
each set of changes to `master` atomic and as a side effect naturally encourages small
well defined PR's.
5. GitHub's UI is bad for rebasing `master` onto `stable`, as it simply adds the
commits to the other branch instead of properly rebasing from what I can tell. You
should always rebase locally on the CLI until they fix it.


***Free software: MIT license***
