from app.utils import convert_to_searchable, generalize_query


def test_convert_to_searchable():
    assert convert_to_searchable(None) is None
    assert convert_to_searchable('') == ''
    assert convert_to_searchable('Hello World') == 'hello world'
    assert convert_to_searchable('Hélló Wórld') == 'hello world'
    assert convert_to_searchable('HĚLLÓ WORLD') == 'hello world'
    assert convert_to_searchable(' Testing  123 ') == 'testing 123'
    assert convert_to_searchable('Testing, 123') == 'testing 123'
    assert convert_to_searchable('Testing @#^$^&* 123') == 'testing @#^$^&* 123'


def test_generalize_query():
    assert generalize_query('Testovací uživatel') == 'testovaci uzivatel'
    assert generalize_query('Jakub Janeček ') == 'jakub janecek'
    assert generalize_query('1234567890/1234') == '1234567890'
    assert generalize_query('123-1234567890') == '123-1234567890'
    assert generalize_query('123-1234567890/0100') == '123-1234567890'
    assert generalize_query(' 123-1234567890/0100 ') == '123-1234567890'
    assert generalize_query('123-1234567890/200') == '123-1234567890/200'
    assert generalize_query('123-1234567890/0100 a text') == '123-1234567890/0100 a text'
    assert generalize_query(None) is None
