import pytest
from app.calculations import BankAccount


def test_bank_set_initial_amount():
    bank_account = BankAccount(50)

    assert bank_account.balance == 50


def test_bank_default_amount():
    bank_account = BankAccount()

    assert bank_account.balance == 0


def test_bank_withdraw_amount():
    bank_account = BankAccount(50)
    bank_account.withdraw(10)

    assert bank_account.balance == 40


def test_bank_deposit_amount():
    bank_account = BankAccount(50)
    bank_account.deposit(10)

    assert bank_account.balance == 60


def test_bank_collect_interest():
    bank_account = BankAccount(50)
    bank_account.collect_interest()

    assert round(bank_account.balance, 2) == 55
