import ast
import io
import re

from setuptools import setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

_description_re = re.compile(r"description\s+=\s+(?P<description>.*)")

with open("lektor_webpack_support.py", "rb") as f:
    description = str(
        ast.literal_eval(_description_re.search(f.read().decode("utf-8")).group(1))
    )

tests_require = [
    "lektor",
    "pytest",
    "pytest-cov",
    "pytest-mock",
]

setup(
    author="Armin Ronacher",
    author_email="armin.ronacher@active-4.com",
    description=description,
    keywords="Lektor plugin node webpack yarn scss static-site",
    extras_require={"test": tests_require},
    license="BSD",
    long_description=readme,
    long_description_content_type="text/markdown",
    py_modules=["lektor_webpack_support"],
    tests_require=tests_require,
    url="http://github.com/lektor/lektor-webpack-support",
    version="0.5",
    name="lektor-webpack-support",
    classifiers=[
        "Environment :: Plugins",
        "Environment :: Web Environment",
        "Framework :: Lektor",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
    ],
    entry_points={
        "lektor.plugins": [
            "webpack-support = lektor_webpack_support:WebpackSupportPlugin",
        ]
    },
)
