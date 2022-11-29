import pytest 
import os 

from asdparser.asd import AsdDB

DIR_PATH = os.path.dirname(os.path.realpath(__file__))
DIR_TEST_DATA = DIR_PATH + "/test_data" 

def test_initialization_raise_file_exception():
    with pytest.raises(FileNotFoundError):
        db = AsdDB("")

def test_initialization_raise_not_a_directory_exeption():
    with pytest.raises(NotADirectoryError):
        db = AsdDB(DIR_TEST_DATA + "/dummyfile")

def test_content_keys():
    db = AsdDB(DIR_TEST_DATA + "/asd")
    assert db.get('ASD02400000_12') is not None
    assert db.get('ASD17430000_1') is not None
    with pytest.raises(KeyError):
        db.get('ASDNOTEXISTING_KEY') is not None

def test_pdbs_included():
    db = AsdDB(DIR_TEST_DATA + "/asd")
    protein = db.get('ASD02400000_12')
    assert len(protein.pdbs) == 4
    assert [pdb.id for pdb in protein.pdbs ] == ['3TNP','4X6Q','3TNQ','4WBB']
    
def test_ptms_included():
    db = AsdDB(DIR_TEST_DATA + "/asd")
    protein = db.get('ASD02400000_12')
    assert len(protein.ptms) == 4
    assert [ptm.position for ptm in protein.ptms] == [85, 2, 83, 112]
    
def test_pdbs_included_no_url():
    db = AsdDB(DIR_TEST_DATA + "/asd")
    protein = db.get('ASD17430000_1')
    assert len(protein.pdbs) == 15