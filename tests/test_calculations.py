import pytest
from app.calculations import BankAccount

# fixtures runs before the test
@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account():
    return BankAccount(50)


def test_bank_set_initial_amount(bank_account):

    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):

    assert zero_bank_account.balance == 0


def test_bank_withdraw_amount(bank_account):
    bank_account.withdraw(10)

    assert bank_account.balance == 40


def test_bank_deposit_amount(bank_account):
    bank_account.deposit(10)

    assert bank_account.balance == 60


def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()

    assert round(bank_account.balance, 2) == 55


@pytest.mark.parametrize(
    "deposited, withdrew, balance", [(100, 50, 50), (200, 20, 180), (5, 10, -5)]
)
def test_bank_transaction(zero_bank_account, deposited, withdrew, balance):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)

    assert zero_bank_account.balance == balance
