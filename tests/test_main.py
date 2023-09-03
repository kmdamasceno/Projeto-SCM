import src.main as main
import pytest

main.ACCOUNTS_DATA_PATH = "tests/test_accounts.data"
main.NEW_ACCOUNTS_DATA_PATH = "tests/test_new_accounts.data"


class TestAccount:
    def setup_class():
        # Creating instance of Account class.
        global test_account
        test_account = main.Account()
        # Reseting accounts data file.
        file = main.pathlib.Path(main.ACCOUNTS_DATA_PATH)
        if file.exists():
            main.os.remove(main.ACCOUNTS_DATA_PATH)
        newfile = open(main.ACCOUNTS_DATA_PATH, "wb")
        main.pickle.dump([], newfile)
        newfile.close()

    @staticmethod
    def change_accounts_file_name():
        main.ACCOUNTS_DATA_PATH = "tests/no_exist.data"
        main.NEW_ACCOUNTS_DATA_PATH = "tests/new_no_exist.data"

    @staticmethod
    def delete_no_exist_file():
        file = main.pathlib.Path(main.ACCOUNTS_DATA_PATH)
        if file.exists():
            main.os.remove(main.ACCOUNTS_DATA_PATH)

    @staticmethod
    def unchange_accounts_file_name():
        main.ACCOUNTS_DATA_PATH = "tests/test_accounts.data"
        main.NEW_ACCOUNTS_DATA_PATH = "tests/test_new_accounts.data"

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

    @staticmethod
    def get_updated_attributes(num):
        file = main.pathlib.Path(main.ACCOUNTS_DATA_PATH)
        if file.exists():
            infile = open(main.ACCOUNTS_DATA_PATH, "rb")
            mylist = main.pickle.load(infile)
            infile.close()
            deposit = 0
            for item in mylist:
                if item.accNo == num:
                    name = item.name
                    type = item.type
                    deposit = item.deposit
        return name, type, deposit

    def test_writeAccount(self):
        expected = (123, "Leopoldo", "S", 1000)
        inputs = iter(expected)
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        main.writeAccount()
        monkeypatch.undo()
        test_account.accNo = expected[0]
        test_account.name, test_account.type, test_account.deposit = TestAccount.get_updated_attributes(test_account.accNo)
        actual = (test_account.accNo,
                  test_account.name,
                  test_account.type,
                  test_account.deposit)
        assert isinstance(test_account, main.Account) == True
        assert actual == expected
        assert TestAccount.check_account_exists(test_account.accNo) == True

    def test_writeAccountsFile_fileDontExist(self):
        TestAccount.change_accounts_file_name()
        main.writeAccountsFile(test_account)
        assert TestAccount.check_account_exists(test_account.accNo) == True
        TestAccount.delete_no_exist_file()
        TestAccount.unchange_accounts_file_name()

    @pytest.mark.parametrize('amount, option, expected', [(500, 1, 1500),
                                                          (500, 2, 1000)])
    def test_depositAndWithdraw_regularOperation(self, amount, option, expected):
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr('builtins.input', lambda _: amount)
        main.depositAndWithdraw(test_account.accNo, option)
        monkeypatch.undo()
        test_account.deposit = TestAccount.get_updated_attributes(test_account.accNo)[2]
        assert test_account.deposit == expected

    def test_depositAndWithdraw_largerAmount(self, capfd):
        expected = '\tYou cannot withdraw larger amount.\n'
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr('builtins.input', lambda _: 2000)
        main.depositAndWithdraw(test_account.accNo, 2)
        monkeypatch.undo()
        out, err = capfd.readouterr()
        assert out == expected

    def test_depositAndWithdraw_fileDontExist(self, capfd):
        expected = '\tNo records to search.\n'
        TestAccount.change_accounts_file_name()
        main.depositAndWithdraw(test_account.accNo, 1)
        TestAccount.delete_no_exist_file()
        TestAccount.unchange_accounts_file_name()
        out, err = capfd.readouterr()
        assert out == expected

    def test_displaySp_regularOperation(self, capfd):
        expected = f'\tYour account balance is =  {test_account.deposit}\n'
        main.displaySp(test_account.accNo)
        out, err = capfd.readouterr()
        assert out == expected

    def test_displaySp_unexistingRecord(self, capfd):
        expected = '\tNo existing record with this number.\n'
        main.displaySp(321)
        out, err = capfd.readouterr()
        assert out == expected

    def test_displaySp_fileDontExist(self, capfd):
        expected = '\tNo records to search.\n'
        TestAccount.change_accounts_file_name()
        main.displaySp(test_account.accNo)
        TestAccount.delete_no_exist_file()
        TestAccount.unchange_accounts_file_name()
        out, err = capfd.readouterr()
        assert expected in out

    def test_displayAll(self, capfd):
        expected = f"\t {test_account.accNo}   {test_account.name}   {test_account.type}   {test_account.deposit}\n"
        main.displayAll()
        out, err = capfd.readouterr()
        assert out == expected

    def test_displayAll_fileDontExist(self, capfd):
        expected = f"\tNo records to display.\n"
        TestAccount.change_accounts_file_name()
        main.displayAll()
        TestAccount.delete_no_exist_file()
        TestAccount.unchange_accounts_file_name()
        out, err = capfd.readouterr()
        assert out == expected
    
    def test_modifyAccount(self):
        expected = ("Motta", "C", 2000)
        inputs = iter(expected)
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        main.modifyAccount(test_account.accNo)
        monkeypatch.undo()
        test_account.name, test_account.type, test_account.deposit = TestAccount.get_updated_attributes(test_account.accNo)
        actual = (test_account.name,
                  test_account.type,
                  test_account.deposit)
        assert actual == expected

    def test_deleteAccount(self):
        test_account_2 = main.Account()
        entry = (321, "Leopoldo", "S", 1000)
        inputs = iter(entry)
        monkeypatch = pytest.MonkeyPatch()
        monkeypatch.setattr('builtins.input', lambda _: next(inputs))
        test_account_2.createAccount()
        main.writeAccountsFile(test_account_2)
        monkeypatch.undo()
        main.deleteAccount(test_account.accNo)
        assert TestAccount.check_account_exists(test_account.accNo) == False
        assert TestAccount.check_account_exists(test_account_2.accNo) == True
