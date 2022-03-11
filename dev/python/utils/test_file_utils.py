from python.utils.file_utils import *

class TestGetFileVars:
    def test_get_file_vars(self):
        assert get_file_vars("abc.xyz") == ("abc",  ".xyz")
        
class TestGetFileName:
    def test_get_file_name(self):
        assert get_file_name("abc.xyz") == "abc"

class TestGetFileExt:
    def test_get_file_ext(self):
        assert get_file_ext("abc.xyz") == ".xyz"
