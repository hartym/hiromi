# Generated by Medikit 0.7.5 on 2020-07-22.
# All changes will be overriden.
# Edit Projectfile and run “make update” (or “medikit update”) to regenerate.

from codecs import open
from os import path

from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Py3 compatibility hacks, borrowed from IPython.
try:
    execfile
except NameError:

    def execfile(fname, globs, locs=None):
        locs = locs or globs
        exec(compile(open(fname).read(), fname, "exec"), globs, locs)


# Get the long description from the README file
try:
    with open(path.join(here, "README.rst"), encoding="utf-8") as f:
        long_description = f.read()
except:
    long_description = ""

# Get the classifiers from the classifiers file
tolines = lambda c: list(filter(None, map(lambda s: s.strip(), c.split("\n"))))
try:
    with open(path.join(here, "classifiers.txt"), encoding="utf-8") as f:
        classifiers = tolines(f.read())
except:
    classifiers = []

version_ns = {}
try:
    execfile(path.join(here, "hiromi/_version.py"), version_ns)
except EnvironmentError:
    version = "dev"
else:
    version = version_ns.get("__version__", "dev")

setup(
    author="",
    author_email="",
    description="",
    license="Apache License, Version 2.0",
    name="hiromi",
    version=version,
    long_description=long_description,
    classifiers=classifiers,
    packages=find_packages(exclude=["ez_setup", "example", "test"]),
    include_package_data=True,
    extras_require={"dev": ["coverage ~= 4.5", "isort", "pytest ~= 4.6", "pytest-cov ~= 2.7"]},
    url="",
    download_url="".format(version=version),
)