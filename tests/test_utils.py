"""
Test related to utilities 
"""
import os

from s_tool.utils import is_local


def test_local_path():
    """test local file path or URL"""
    URL_PATH = "http://www.google.com"
    URL_PATH1 = "www.google.com"
    LOCAL_PATH = "tests/index.html"

    assert URL_PATH == is_local(URL_PATH)
    assert "file" in is_local(os.path.abspath(LOCAL_PATH))
    assert URL_PATH1 == is_local(URL_PATH1)
