import pytest 

from asdparser.asd import AsdDB

def test_initialization_raise_file_exception():
    with pytest.raises(FileNotFoundError):
        db = AsdDB("")
