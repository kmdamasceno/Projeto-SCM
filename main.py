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
            pass
        elif ch == "2":
            num = int(input("\n\tEnter the account number: "))
            pass
        elif ch == "3":
            num = int(input("\n\tEnter the account number: "))
            pass
        elif ch == "4":
            num = int(input("\n\tEnter the account number: "))
            pass
        elif ch == "5":
            print("\n")
            pass
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
