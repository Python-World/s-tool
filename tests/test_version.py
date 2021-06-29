from s_tool import __version__


def test_version():
    # a dummy test, for setting up pytest, tox, and test on ci
    # will remove it after writing real test cases
    assert __version__.startswith("0")
