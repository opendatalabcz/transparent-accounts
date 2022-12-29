import pytest
from app.utils import get_fully_qualified_acc_num


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
