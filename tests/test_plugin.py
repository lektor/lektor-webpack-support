import py


def test_disabled_by_default(plugin):
    extra_flags = {}
    assert not plugin.is_enabled(extra_flags)


def test_enabled_with_webpack_flag(plugin):
    extra_flags = {"webpack": True}
    assert plugin.is_enabled(extra_flags)


def test_basic(plugin, builder, env, mocker):
    mock_popen = mocker.patch("lektor_webpack_support.portable_popen")
    plugin.on_before_build_all(builder)
    env_path = py.path.local(env.root_path)
    mock_popen.assert_any_call(
        ["npm", "install"],
        cwd=env_path / 'webpack'
    )
    mock_popen.assert_any_call(
        [env_path / 'webpack' / 'node_modules' / '.bin' / 'webpack'],
        cwd=env_path / 'webpack'
    )
    assert plugin.webpack_process is None


def test_watcher(plugin, env, mocker):
    mock_popen = mocker.patch("lektor_webpack_support.portable_popen")
    plugin.on_server_spawn(extra_flags={"webpack": True})
    env_path = py.path.local(env.root_path)
    mock_popen.assert_any_call(
        ["npm", "install"],
        cwd=env_path / 'webpack'
    )
    mock_popen.assert_any_call(
        [env_path / 'webpack' / 'node_modules' / '.bin' / 'webpack', '--watch'],
        cwd=env_path / 'webpack'
    )
    assert plugin.webpack_process is mock_popen.return_value


def test_watcher_build_flags(plugin, env, mocker):
    mock_popen = mocker.patch("lektor_webpack_support.portable_popen")
    plugin.on_server_spawn(build_flags={"webpack": True})
    env_path = py.path.local(env.root_path)
    mock_popen.assert_any_call(
        ["npm", "install"],
        cwd=env_path / 'webpack'
    )
    mock_popen.assert_any_call(
        [env_path / 'webpack' / 'node_modules' / '.bin' / 'webpack', '--watch'],
        cwd=env_path / 'webpack'
    )
    assert plugin.webpack_process is mock_popen.return_value


def test_watcher_plugin_disabled(plugin, env, mocker):
    mock_popen = mocker.patch("lektor_webpack_support.portable_popen")
    plugin.on_server_spawn()
    mock_popen.assert_not_called()


def test_server_stop(plugin, mocker):
    plugin.webpack_process = mocker.Mock()
    plugin.on_server_stop()
    plugin.webpack_process.kill.assert_called_with()
