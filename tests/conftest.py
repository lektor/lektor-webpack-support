import os
import pytest
from lektor.builder import Builder
from lektor.db import Database
from lektor.project import Project
from lektor.environment import Environment
from lektor_webpack_support import WebpackSupportPlugin


@pytest.fixture(scope='function')
def project():
    return Project.from_path(os.path.join(os.path.dirname(__file__),
                                          'demo-project'))


@pytest.fixture(scope='function')
def env(project):
    return Environment(project)


@pytest.fixture(scope='function')
def pad(env):
    return Database(env).new_pad()


@pytest.fixture(scope='function')
def builder(tmpdir, pad):
    return Builder(pad, str(tmpdir.mkdir("output")),
                   extra_flags=('webpack',))


@pytest.fixture
def plugin(env):
    return WebpackSupportPlugin(env, "testing")
