import pytest

def test_add():
    assert 1 + 2 == 3


@pytest.mark.xfail(reason='This test is expected to fail')
def test_subtract():
    assert 2 - 1 == 0


@pytest.mark.skipif(True, reason='This test is skipped')
def test_multiply():
    assert 2 * 2 == 5
