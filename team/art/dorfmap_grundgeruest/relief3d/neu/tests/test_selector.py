from neu.selector import new_pipeline_enabled


def test_relief_neu_is_opt_in():
    assert new_pipeline_enabled({}) is False
    assert new_pipeline_enabled({"RELIEF_NEU": "0"}) is False
    assert new_pipeline_enabled({"RELIEF_NEU": "1"}) is True
