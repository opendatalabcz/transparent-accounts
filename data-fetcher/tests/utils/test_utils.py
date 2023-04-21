import pytest

from app.utils import convert_to_searchable, float_from_cz, get_fully_qualified_acc_num


def test_convert_to_searchable():
    assert convert_to_searchable(None) is None
    assert convert_to_searchable('') == ''
    assert convert_to_searchable('Hello World') == 'hello world'
    assert convert_to_searchable('Hélló Wórld') == 'hello world'
    assert convert_to_searchable('HĚLLÓ WORLD') == 'hello world'
    assert convert_to_searchable(' Testing  123 ') == 'testing 123'
    assert convert_to_searchable('Testing, 123') == 'testing 123'
    assert convert_to_searchable('Testing @#^$^&* 123') == 'testing @#^$^&* 123'


def test_float_from_cz():
    assert float_from_cz('1,2') == 1.2
    assert float_from_cz('1 000') == 1000
    assert float_from_cz('1 000') == 1000
    assert float_from_cz('1 000 000') == 1_000_000
    assert float_from_cz('-8 000,088') == -8000.088
    with pytest.raises(ValueError):
        float_from_cz('a')


@pytest.mark.parametrize('acc_num', ('123456-1234567890', '123-1234567890', '1234567890', '12345', '00-00', '1-123456'))
def test_get_fully_qualified_acc_num_valid(acc_num):
    fq = get_fully_qualified_acc_num(acc_num)

    tokens = fq.split('-')
    assert len(tokens[0]) == 6
    assert len(tokens[1]) == 10


@pytest.mark.parametrize('acc_num', ('', '-1234567890', '12345678901', '1234567-1234567890', '1-1-1', 'A', 'abc-def'))
def test_get_fully_qualified_acc_num_invalid(acc_num):
    with pytest.raises(ValueError):
        get_fully_qualified_acc_num(acc_num)
