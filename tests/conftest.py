import os
import collections
import py
import pytest
from lektor.builder import Builder
from lektor.db import Database
from lektor.project import Project
from lektor.environment import Environment
from lektor_webpack_support import WebpackSupportPlugin


expected_type = collections.namedtuple('expected_type', ['project_path', 'root_path', 'build_command', 'watch_command'])


def pytest_generate_tests(metafunc):
    if 'project' in metafunc.fixturenames:
        cwd = py.path.local(os.path.dirname(__file__)) 
        demo_project = cwd / 'demo-project'
        webpack_binary = demo_project / 'webpack' / 'node_modules' / '.bin' / 'webpack'
        metafunc.parametrize(
            "expected", [
                expected_type(demo_project, 'webpack', [webpack_binary], [webpack_binary, '--watch']),
                expected_type(cwd / 'demo-scripts-project', 'parcel', ['npm', 'run', 'build'], ['npm', 'run', 'watch']),
            ], indirect=True)


@pytest.fixture(scope='function')
def expected(request):
    return request.param


@pytest.fixture(scope='function')
def project(expected):
    return Project.from_path(str(expected.project_path))


@pytest.fixture(scope='function')
def env(project):
    return Environment(project)


@pytest.fixture(scope='function')
def pad(env):
    return Database(env).new_pad()


@pytest.fixture(scope='function')
def builder(tmpdir, pad):
    output_dir = str(tmpdir.mkdir("output"))
    try:
        return Builder(pad, output_dir, extra_flags=('webpack',))
    except TypeError:
        return Builder(pad, output_dir, build_flags=('webpack',))



@pytest.fixture
def plugin(env):
    return WebpackSupportPlugin(env, "webpack-support")
