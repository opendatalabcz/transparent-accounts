import pytest
from app.fetcher.kb.utils import get_api_formatted_acc_num


@pytest.mark.parametrize('acc_num', ('123456-1234567890', '123-1234567890', '1234567890', '12345', '00-00', '1-123456'))
def test_get_fully_qualified_acc_num(acc_num):
    assert(get_api_formatted_acc_num('123456-1234567890') == '1234561234567890')
    assert (get_api_formatted_acc_num('123-1234567890') == '1231234567890')
    assert (get_api_formatted_acc_num('1234567890') == '1234567890')
    assert (get_api_formatted_acc_num('12345') == '12345')
    assert (get_api_formatted_acc_num('00-00') == '00')
    assert (get_api_formatted_acc_num('001-123456') == '1123456')
