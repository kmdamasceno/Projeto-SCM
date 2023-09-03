from src.main import Account
import pytest

main.ACCOUNTS_DATA_PATH = "test_accounts.data"
main.NEW_ACCOUNTS_DATA_PATH = "test_new_accounts.data"


class TestAccount:
    def setup_class():
        global test_account
        test_account = main.Account()

    def test_createInstance(self):
        assert isinstance(test_account, main.Account) == True

    def test_createAccount(self):
        expected = (123, "Leopoldo", "S", 1000)
        inputs = iter(expected)
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        test_account.createAccount()
        monkeypatch.undo()
        actual = (test_account.accNo,
                  test_account.name,
                  test_account.type,
                  test_account.deposit)
        assert actual == expected

    @staticmethod
    def check_account_exists(num):
        file = main.pathlib.Path(main.ACCOUNTS_DATA_PATH)
        if file.exists():
            infile = open(main.ACCOUNTS_DATA_PATH, "rb")
            mylist = main.pickle.load(infile)
            infile.close()
            found = False
            for item in mylist:
                if item.accNo == num:
                    found = True
        return found

    def test_writeAccountsFile(self):
        main.writeAccountsFile(test_account)
        assert TestAccount.check_account_exists(test_account.accNo) == True

    @staticmethod
    def get_updated_deposit(num):
        file = main.pathlib.Path(main.ACCOUNTS_DATA_PATH)
        if file.exists():
            infile = open(main.ACCOUNTS_DATA_PATH, "rb")
            mylist = main.pickle.load(infile)
            infile.close()
            deposit = 0
            for item in mylist:
                if item.accNo == num:
                    deposit = item.deposit
        return deposit

    def test_depositAndWithdraw(self):
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr('builtins.input', lambda _: 500)
        main.depositAndWithdraw(test_account.accNo, 1)
        test_account.deposit = TestAccount.get_updated_deposit(test_account.accNo)
        assert test_account.deposit == 1500
        main.depositAndWithdraw(test_account.accNo, 2)
        test_account.deposit = TestAccount.get_updated_deposit(test_account.accNo)
        monkeypatch.undo()
        assert test_account.deposit == 1000

    def test_displaySp(self, capfd):
        main.displaySp(test_account.accNo)
        out, err = capfd.readouterr()
        assert out == f"\tYour account balance is =  {test_account.deposit}\n"
        