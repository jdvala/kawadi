import os.path as path
from pathlib import Path

from setuptools import find_packages, setup

here = Path(__file__).parent

requirements_path = here / "requirements" / "prod.txt"

readme_path = path.join(here, "README.md")


def read_requirements(path):
    try:
        with path.open(mode="rt", encoding="utf-8") as fp:
            return list(filter(None, (line.split("#")[0].strip() for line in fp)))
    except IndexError:
        raise RuntimeError(f"{path} is broken")


def read_readme(path):
    with open(path, mode="rt", encoding="utf-8") as fp:
        return fp.read()


setup(
    name="kawadi",
    long_description=read_readme(readme_path),
    long_description_content_type="text/markdown",
    python_requires=">=3.7.0",
    setup_requires=["setuptools_scm"],
    install_requires=read_requirements(requirements_path),
    use_scm_version={
        "version_scheme": "guess-next-dev",
        "local_scheme": "dirty-tag",
        "write_to": "src/kawadi/_repo_version.py",
        "write_to_template": 'version = "{version}"\n',
        "relative_to": __file__,
    },
    include_package_data=True,
    package_data={},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    entry_points={"console_scripts": ["kawadi = kawadi.cli:entrypoint"]},
    author="Jay Vala",
    author_email="jay.vala@msn.com",
    url="https://github.com/jdvala/kawadi",
)
