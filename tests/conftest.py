import os

import pytest
from lektor.builder import Builder
from lektor.db import Database
from lektor.environment import Environment
from lektor.project import Project

from lektor_webpack_support import WebpackSupportPlugin


@pytest.fixture(scope="function")
def project():
    return Project.from_path(os.path.join(os.path.dirname(__file__), "demo-project"))


@pytest.fixture(scope="function")
def env(project):
    return Environment(project)


@pytest.fixture(scope="function")
def pad(env):
    return Database(env).new_pad()


@pytest.fixture(scope="function")
def builder(tmpdir, pad):
    output_dir = str(tmpdir.mkdir("output"))
    try:
        return Builder(pad, output_dir, extra_flags=("webpack",))
    except TypeError:
        return Builder(pad, output_dir, build_flags=("webpack",))


@pytest.fixture
def plugin(env):
    return WebpackSupportPlugin(env, "testing")
