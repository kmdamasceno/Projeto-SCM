import pickle
import os
import pathlib


ACCOUNTS_DATA_PATH = "src/accounts.data"
NEW_ACCOUNTS_DATA_PATH = "src/new_accounts.data"


class Account:
    def __init__(self):
        self.accNo = 0
        self.name = ""
        self.deposit = 0
        self.type = ""

    def createAccount(self):
        self.accNo = int(input("\n\tEnter the account number: "))
        self.name = input("\tEnter the account holder name: ")
        self.type = input("\tEnter the type of account [C/S]: ")
        self.deposit = int(
            input("\tEnter the initial amount (>=500 for Saving and >=1000 for current): "))
        print("\n\n\n\tAccount Created.")


def writeAccount():
    account = Account()
    account.createAccount()
    writeAccountsFile(account)

def writeAccountsFile(account):
    file = pathlib.Path(ACCOUNTS_DATA_PATH)
    if file.exists():
        infile = open(ACCOUNTS_DATA_PATH, "rb")
        oldlist = pickle.load(infile)
        oldlist.append(account)
        infile.close()
        os.remove(ACCOUNTS_DATA_PATH)
    else:
        oldlist = [account]
    outfile = open(NEW_ACCOUNTS_DATA_PATH, "wb")
    pickle.dump(oldlist, outfile)
    outfile.close()
    os.rename(NEW_ACCOUNTS_DATA_PATH, ACCOUNTS_DATA_PATH)

def depositAndWithdraw(num1, num2):
    file = pathlib.Path(ACCOUNTS_DATA_PATH)
    mylist = []
    if file.exists():
        infile = open(ACCOUNTS_DATA_PATH, "rb")
        mylist = pickle.load(infile)
        infile.close()
        os.remove(ACCOUNTS_DATA_PATH)
        for item in mylist:
            if item.accNo == num1:
                if num2 == 1:
                    amount = int(input("\tEnter the amount to deposit: "))
                    item.deposit += amount
                    print("\tYour account is updated.")
                elif num2 == 2:
                    amount = int(input("\tEnter the amount to withdraw: "))
                    if amount <= item.deposit:
                        item.deposit -= amount
                    else:
                        print("\tYou cannot withdraw larger amount.")
    else:
        print("\tNo records to search.")
    outfile = open(NEW_ACCOUNTS_DATA_PATH, "wb")
    pickle.dump(mylist, outfile)
    outfile.close()
    os.rename(NEW_ACCOUNTS_DATA_PATH, ACCOUNTS_DATA_PATH)

def displaySp(num):
    file = pathlib.Path(ACCOUNTS_DATA_PATH)
    found = False
    if file.exists():
        infile = open(ACCOUNTS_DATA_PATH, "rb")
        mylist = pickle.load(infile)
        infile.close()
        for item in mylist:
            if item.accNo == num:
                print("\tYour account balance is = ", item.deposit)
                found = True
    else:
        print("\tNo records to search.")
    if not found:
        print("\tNo existing record with this number.")

def displayAll():
    file = pathlib.Path(ACCOUNTS_DATA_PATH)
    if file.exists():
        infile = open(ACCOUNTS_DATA_PATH, "rb")
        mylist = pickle.load(infile)
        for item in mylist:
            print("\t", item.accNo, " ", item.name, " ", item.type, " ", item.deposit)
        infile.close()
    else:
        print("\tNo records to display.")


if __name__ == "__main__":
    print("\n")
    print("\t========================")
    print("\t BANK MANAGEMENT SYSTEM")
    print("\t========================")
    ch = ""
    num = 0
    while ch != 8:
        print("\n")
        print("\tMAIN MENU")
        print("\t1. NEW ACCOUNT")
        print("\t2. DEPOSIT")
        print("\t3. WITHDRAW")
        print("\t4. BALANCE")
        print("\t5. DISPLAY ACCOUNT LIST")
        print("\t6. CLOSE ACCOUNT")
        print("\t7. MODIFY ACCOUNT")
        print("\t8. EXIT")
        ch = input("\tSelect your option (1-8): ")

        if ch == "1":
            print("\n")
            writeAccount()
        elif ch == "2":
            num = int(input("\n\tEnter the account number: "))
            depositAndWithdraw(num, 1)
        elif ch == "3":
            num = int(input("\n\tEnter the account number: "))
            depositAndWithdraw(num, 2)
        elif ch == "4":
            num = int(input("\n\tEnter the account number: "))
            displaySp(num)
        elif ch == "5":
            print("\n")
            displayAll()
        elif ch == "6":
            num = int(input("\n\tEnter the account number: "))
            pass
        elif ch == "7":
            num = int(input("\n\tEnter the account number: "))
            pass
        elif ch == "8":
            print("\n\tThanks for using Bank Management System.")
            break
        else:
            print("\nPlease, select a valid option.")
