import os

from setuptools import find_packages, setup

DIR = os.path.dirname(__file__)
REQUIREMENTS = os.path.join(DIR, "requirements.txt")


with open(REQUIREMENTS, encoding="utf-8") as fobj:
    setup(
        name="pretty_trees",
        version="0.1.0",
        packages=find_packages(exclude=["tests*"]),
        install_requires=fobj.read().strip().splitlines(),
        include_package_data=True,
    )
