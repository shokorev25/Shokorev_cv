import pytest
from special_hashmap import SpecialHashMap

@pytest.fixture
def map():
    m = SpecialHashMap()
    m.insert("1", 10)
    m.insert("2", 20)
    m.insert("3", 30)
    return m

def test_insert(map):
    map.insert("4", 40)
    assert map.get("4") == 40

def test_get(map):
    assert map.get("1") == 10
    with pytest.raises(KeyError):
        map.get("nonexistent")

def test_delete(map):
    map.delete("1")
    with pytest.raises(KeyError):
        map.get("1")

def test_iloc(map):
    assert map.iloc(0) == 10    
    assert map.iloc(2) == 30   
    with pytest.raises(IndexError):
        map.iloc(5)             

def test_ploc_simple_conditions(map):
    result = map.ploc(">=20")
    assert result == {"2": 20, "3": 30}

def test_ploc_invalid_conditions(map):
    with pytest.raises(ValueError):
        map.ploc(">>10")  

def test_ploc_no_match(map):
    result = map.ploc(">100")
    assert result == {}
