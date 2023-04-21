from datetime import datetime, timedelta

from flexmock import flexmock

import app.utils as utils
from app.models import Account, AccountUpdate, Bank, UpdateStatus


def test_convert_to_searchable():
    assert utils.convert_to_searchable(None) is None
    assert utils.convert_to_searchable('') == ''
    assert utils.convert_to_searchable('Hello World') == 'hello world'
    assert utils.convert_to_searchable('Hélló Wórld') == 'hello world'
    assert utils.convert_to_searchable('HĚLLÓ WORLD') == 'hello world'
    assert utils.convert_to_searchable(' Testing  123 ') == 'testing 123'
    assert utils.convert_to_searchable('Testing, 123') == 'testing 123'
    assert utils.convert_to_searchable('Testing @#^$^&* 123') == 'testing @#^$^&* 123'


def test_generalize_query():
    assert utils.generalize_query('Testovací uživatel') == 'testovaci uzivatel'
    assert utils.generalize_query('Jakub Janeček ') == 'jakub janecek'
    assert utils.generalize_query('1234567890/1234') == '1234567890'
    assert utils.generalize_query('123-1234567890') == '123-1234567890'
    assert utils.generalize_query('123-1234567890/0100') == '123-1234567890'
    assert utils.generalize_query(' 123-1234567890/0100 ') == '123-1234567890'
    assert utils.generalize_query('123-1234567890/200') == '123-1234567890/200'
    assert utils.generalize_query('123-1234567890/0100 a text') == '123-1234567890/0100 a text'
    assert utils.generalize_query(None) is None


def test_is_updatable_never_updated():
    # Test that an account that has never been updated is updatable.
    acc = Account(number='123456-1234567890', bank=Bank.CSAS, archived=False, last_updated=None)
    flexmock(utils).should_receive('find_updates').and_return([])
    assert utils.is_updatable(acc) is True


def test_is_updatable_last_update_not_today():
    # Test that an account that has been updated, but not today, is updatable.
    last_update = AccountUpdate(status=UpdateStatus.SUCCESS, started=datetime.now() - timedelta(days=1), account_number='123456-1234567890', account_bank=Bank.CSAS)
    acc = Account(number='123456-1234567890', bank=Bank.CSAS, archived=False, last_updated=last_update)
    flexmock(utils).should_receive('find_updates').and_return([last_update])
    assert utils.is_updatable(acc) is True


def test_is_updatable_last_update_pending_for_one_hour():
    # Test that an account that has an update pending for more than one hour is updatable.
    last_update = AccountUpdate(status=UpdateStatus.PENDING, started=datetime.now() - timedelta(hours=2), account_number='123456-1234567890', account_bank=Bank.CSAS)
    acc = Account(number='123456-1234567890', bank=Bank.CSAS, archived=False, last_updated=last_update)
    flexmock(utils).should_receive('find_updates').and_return([last_update])
    assert utils.is_updatable(acc) is True


def test_is_updatable_last_update_failed():
    # Test that an account that has a failed update is updatable.
    last_update = AccountUpdate(status=UpdateStatus.FAILURE, started=datetime.now() - timedelta(hours=1), ended=datetime.now(), account_number='123456-1234567890', account_bank=Bank.CSAS)
    acc = Account(number='123456-1234567890', bank=Bank.CSAS, archived=False, last_updated=last_update)
    flexmock(utils).should_receive('find_updates').and_return([last_update])
    assert utils.is_updatable(acc) is True


def test_is_updatable_last_update_today():
    # Test that an account that has been updated today is not updatable.
    last_update = AccountUpdate(status=UpdateStatus.SUCCESS, started=datetime.now(), account_number='123456-1234567890', account_bank=Bank.CSAS)
    acc = Account(number='123456-1234567890', bank=Bank.CSAS, archived=False, last_updated=last_update)
    flexmock(utils).should_receive('find_updates').and_return([last_update])
    assert utils.is_updatable(acc) is False


def test_is_updatable_archived():
    # Test that an archived account is not updatable.
    acc = Account(number='123456-1234567890', bank=Bank.CSAS, archived=True, last_updated=None)
    assert utils.is_updatable(acc) is False
