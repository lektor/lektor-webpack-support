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
    mock_popen.assert_any_call(["npm", "install"], cwd=env_path / "webpack")
    mock_popen.assert_any_call(
        [env_path / "webpack" / "node_modules" / ".bin" / "webpack"],
        cwd=env_path / "webpack",
    )
    assert plugin.webpack_process is None


def test_watcher(plugin, env, mocker):
    mock_popen = mocker.patch("lektor_webpack_support.portable_popen")
    plugin.on_server_spawn(extra_flags={"webpack": True})
    env_path = py.path.local(env.root_path)
    mock_popen.assert_any_call(["npm", "install"], cwd=env_path / "webpack")
    mock_popen.assert_any_call(
        [env_path / "webpack" / "node_modules" / ".bin" / "webpack", "--watch"],
        cwd=env_path / "webpack",
    )
    assert plugin.webpack_process is mock_popen.return_value


def test_watcher_build_flags(plugin, env, mocker):
    mock_popen = mocker.patch("lektor_webpack_support.portable_popen")
    plugin.on_server_spawn(build_flags={"webpack": True})
    env_path = py.path.local(env.root_path)
    mock_popen.assert_any_call(["npm", "install"], cwd=env_path / "webpack")
    mock_popen.assert_any_call(
        [env_path / "webpack" / "node_modules" / ".bin" / "webpack", "--watch"],
        cwd=env_path / "webpack",
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


def test_yarn_support(plugin, env, mocker):
    mock_popen = mocker.patch("lektor_webpack_support.portable_popen")

    mock_path_exists = mocker.patch("os.path.exists")
    mock_path_exists.return_value = True

    mock_locate_executable = mocker.patch("lektor_webpack_support.locate_executable")
    mock_locate_executable.return_value = "/usr/local/bin/yarn"

    env_path = py.path.local(env.root_path)
    plugin.install_node_dependencies()

    assert mock_path_exists.called
    assert mock_path_exists.call_args[0][0].endswith("yarn.lock")
    assert mock_locate_executable.called
    mock_locate_executable.assert_any_call("yarn")
    mock_popen.assert_any_call(["yarn", "install"], cwd=env_path / "webpack")
