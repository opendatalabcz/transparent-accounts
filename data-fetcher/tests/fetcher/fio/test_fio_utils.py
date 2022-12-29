import pytest

from app.fetcher.fio.utils import get_fio_formatted_acc_num


@pytest.mark.parametrize('acc_num', ('000000-1234567890', '123456-1234567890'))
def test_get_fio_formatted_acc_num(acc_num):
    fio_acc_num = get_fio_formatted_acc_num(acc_num)

    assert len(fio_acc_num) == 10
    assert fio_acc_num.isnumeric()
