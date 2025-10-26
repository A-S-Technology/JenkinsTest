import pytest
from src.app import add, subtract, divide

class TestMath:
    def test_add(self):
        assert add(2, 3) == 5
        assert add(-1, 1) == 0
    
    def test_subtract(self):
        assert subtract(5, 3) == 2
        assert subtract(0, 5) == -5
    
    def test_divide(self):
        assert divide(10, 2) == 5
        assert divide(7, 2) == 3.5
    
    def test_divide_by_zero(self):
        with pytest.raises(ValueError):
            divide(10, 0)