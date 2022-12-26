from app.fetcher.kb.utils import get_api_formatted_acc_num, get_html_formatted_acc_num


def test_get_api_formatted_acc_num():
    assert get_api_formatted_acc_num('123456-1234567890') == '1234561234567890'
    assert get_api_formatted_acc_num('000456-1234567890') == '4561234567890'
    assert get_api_formatted_acc_num('123456-0004567890') == '1234564567890'
    assert get_api_formatted_acc_num('000456-0004567890') == '4564567890'
    assert get_api_formatted_acc_num('000000-1234567890') == '1234567890'
    assert get_api_formatted_acc_num('000000-0004567890') == '4567890'


def test_get_html_formatted_acc_num():
    assert get_html_formatted_acc_num('123456-1234567890') == '123456-1234567890'
    assert get_html_formatted_acc_num('000456-1234567890') == '456-1234567890'
    assert get_html_formatted_acc_num('123456-0004567890') == '123456-4567890'
    assert get_html_formatted_acc_num('000456-0004567890') == '456-4567890'
    assert get_html_formatted_acc_num('000000-1234567890') == '1234567890'
    assert get_html_formatted_acc_num('000000-0004567890') == '4567890'
