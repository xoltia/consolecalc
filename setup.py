from setuptools import setup

setup(
    name = "consolecalc",
    packages = ["consolecalc"],
    entry_points = {
        "console_scripts": ['consolecalc=consolecalc.runner:main']
    },
    version = '1.0',
    description = "Python command line calculator",
    author = "Xoltia",
    author_email = "auzrema@gmail.com",
)