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
