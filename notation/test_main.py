import pytest
from main import prefix_to_infix

def test_valid_expressions():
    assert prefix_to_infix("+ - 13 4 55") == "((13 - 4) + 55)"
    assert prefix_to_infix("+ 2 * 2 - 2 1") == "(2 + (2 * (2 - 1)))"
    assert prefix_to_infix("+ + 10 20 30") == "((10 + 20) + 30)"
    assert prefix_to_infix("- - 1 2 3") == "((1 - 2) - 3)"
    assert prefix_to_infix("/ + 3 10 * + 2 3 - 3 5") == "((3 + 10) / ((2 + 3) * (3 - 5)))"

def test_invalid_expressions():
    with pytest.raises(ValueError, match="Выражение не должно быть пустым"):
        prefix_to_infix("")
    with pytest.raises(ValueError, match="Недостаточно операндов для оператора"):
        prefix_to_infix("+ 1")
    with pytest.raises(ValueError, match="Недопустимый символ: x"):
        prefix_to_infix("+ 1 x")
    with pytest.raises(ValueError, match="Некорректное выражение: проверьте баланс операторов и операндов"):
        prefix_to_infix("+ 1 2 3")
