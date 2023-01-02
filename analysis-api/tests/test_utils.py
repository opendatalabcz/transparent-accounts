from app.utils import object_encode, generalize_query


def test_object_encode():
    pass


def test_generalize_query():
    assert generalize_query('1234567890/1234') == '1234567890'
    assert generalize_query('Testovaci uzivatel') == 'Testovaci uzivatel'
    assert generalize_query('123-1234567890') == '123-1234567890'
    assert generalize_query('123-1234567890/0100') == '123-1234567890'
    assert generalize_query(' 123-1234567890/0100 ') == '123-1234567890'
    assert generalize_query('123-1234567890/200') == '123-1234567890/200'
    assert generalize_query('123-1234567890/0100 a text') == '123-1234567890/0100 a text'
    assert generalize_query(None) is None

