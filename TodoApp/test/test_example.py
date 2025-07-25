import pytest

def test_equal_or_not_equal():
    assert 1 == 1
    assert 3 != 1
    
def test_is_instance():
    assert isinstance('this is a string', str)
    assert not isinstance('10', int)
    
def test_boolean():
    validated = True
    assert validated is True
    assert ('hello' == 'world') is False
    
def test_type():
    assert type('Hello' is str)
    assert type('Hello'is not int)
    
def test_greater_or_less_than():
    assert 10 > 1
    assert 10 < 20
    assert 10 <= 10
    assert 10 >= 10
    
def test_list():
    num_list = [1, 2, 3, 4, 5]
    any_list = [False, False]
    
    assert 1 in num_list
    assert 7 not in num_list
    assert all(num_list)
    assert not any(any_list)
    

class Student:
    def __init__(self, first_name: str, last_name: str, major: str, years: int):
        self.first_name = first_name
        self.last_name = last_name
        self.major = major
        self.years = years

@pytest.fixture
def student() :
    return Student('John', 'Doe', 'Computer Science', 4)

def test_person_initialization(student):
    assert student.first_name == 'John', 'First name should be John'
    assert student.last_name == 'Doe', 'Last name should be Doe'
    assert student.major == 'Computer Science', 'Major should be Computer Science'
    assert student.years == 4, 'Years should be 4'
    
    

        
        
        