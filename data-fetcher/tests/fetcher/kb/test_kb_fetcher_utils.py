from app.fetcher.kb.utils import get_kb_formatted_acc_num


def test_get_kb_api_formatted_acc_num():
    assert get_kb_formatted_acc_num('123456-1234567890', True) == '1234561234567890'
    assert get_kb_formatted_acc_num('000456-1234567890', True) == '4561234567890'
    assert get_kb_formatted_acc_num('123456-0004567890', True) == '1234564567890'
    assert get_kb_formatted_acc_num('000456-0004567890', True) == '4564567890'
    assert get_kb_formatted_acc_num('000000-1234567890', True) == '1234567890'
    assert get_kb_formatted_acc_num('000000-0004567890', True) == '4567890'


def test_get_kb_formatted_acc_num():
    assert get_kb_formatted_acc_num('123456-1234567890', False) == '123456-1234567890'
    assert get_kb_formatted_acc_num('000456-1234567890', False) == '456-1234567890'
    assert get_kb_formatted_acc_num('123456-0004567890', False) == '123456-4567890'
    assert get_kb_formatted_acc_num('000456-0004567890', False) == '456-4567890'
    assert get_kb_formatted_acc_num('000000-1234567890', False) == '1234567890'
    assert get_kb_formatted_acc_num('000000-0004567890', False) == '4567890'
