import os
import pytest
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


@pytest.fixture
def plugin(env):
    return WebpackSupportPlugin(env, "testing")
