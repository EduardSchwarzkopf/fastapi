import pytest
from app.calculations import BankAccount


def test_bank_set_initial_amount():
    bank_account = BankAccount(50)

    assert bank_account.balance == 50
