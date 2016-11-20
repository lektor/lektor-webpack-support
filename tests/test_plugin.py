def test_disabled_by_default(plugin):
    extra_flags = {}
    assert not plugin.is_enabled(extra_flags)

def test_enabled_with_webpack_flag(plugin):
    extra_flags = {"webpack": True}
    assert plugin.is_enabled(extra_flags)
