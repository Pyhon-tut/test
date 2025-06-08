from data import db
import random

class account:
    def __init__(self,userId,accountType='sav',balance=0):
        self.accountnumber=random.sample(range(1,11),5)
        self.userId=userId
        self.accountType=accountType
        self.__balance=balance
    
    def getBalance(self):
        return self.__balance
    def setBalance(self,amount,Type="W"):
        if Type=="W":
            self.__balance-=amount
        else:
            self.__balance+=amount
        return self.__balance
    @staticmethod
    def createAccount(userId,accountType="sav",balance=0):
        db.execute_query("""CREATE TABLE IF NOT EXISTS ACCOUNT (id integer primary key AUTOINCREMENT,accountnumber text,userId integer,accounttype text,balance float)""",None,False,True)
        db.execute_query("""CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    accountnumber TEXT,
    type TEXT, 
    amount FLOAT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)""",None,False,True)
        #datacount=db.execute_query(f"select count(*) from ACCOUNT where userId={userId}",None,True,False)
        # if datacount > 4:
        #     return False
        account_number = ''.join(map(str, random.sample(range(0, 10), 10))) 

        db.execute_query("""insert into ACCOUNT (accountnumber,userId,accountType,balance) values (?,?,?,?)""",(account_number,userId,accountType,0),False,True)
        return True
    @staticmethod
    def getAllAccount(userId):
            datacount=db.execute_query(f"select * from ACCOUNT where userId={userId}",None,True,False)
            return datacount
    @staticmethod
    def getAccountInfo(accountNumber):
           datacount=db.execute_query(f"select * from ACCOUNT where accountnumber='{accountNumber}'",None,True,False)
           return datacount
    # In account_repository.py

    # @staticmethod
    # def withdraw(account_number, user_id, amount):
    #     # Fetch account
    #     account = db.execute_query("SELECT balance FROM account WHERE accountnumber = ? AND userId = ?", (account_number, user_id),True,False)
    #     if account and account[0][0] >= amount:
    #         new_balance = account[0][0] - amount
    #         db.execute_query("UPDATE account SET balance = ? WHERE accountnumber = ? AND userId = ?", (new_balance, account_number, user_id),False,True)
    #         return True
    #     return False

    @staticmethod
    def withdraw(account_number, user_id, amount):
        account = db.execute_query(
            "SELECT balance FROM account WHERE accountnumber = ? AND userId = ?",
            (account_number, user_id), True, False
        )
        if account and account[0][0] >= amount:
            new_balance = account[0][0] - amount
            db.execute_query(
                "UPDATE account SET balance = ? WHERE accountnumber = ? AND userId = ?",
                (new_balance, account_number, user_id), False, True
            )
                # Record transaction
            varlue='withdraw'
            db.execute_query(
                "INSERT INTO transactions (accountnumber, type, amount) VALUES (?, ?, ?)",
                (account_number,varlue , amount), False, True
            )
            return True
        return False



    # @staticmethod
    # def deposit(account_number, user_id, amount):
    #     # Fetch account
    #     account = db.execute_query("SELECT balance FROM account WHERE accountnumber = ? AND userId = ?", (account_number, user_id),True,False)
    #     if account:
    #         new_balance = account[0][0] + amount
    #         db.execute_query("UPDATE account SET balance = ? WHERE accountnumber = ? AND userId = ?", (new_balance, account_number, user_id),False,True)
    #         return True
    #     return False
    @staticmethod
    def deposit(account_number, user_id, amount):
        account = db.execute_query(
         "SELECT balance FROM account WHERE accountnumber = ? AND userId = ?",
            (account_number, user_id), True, False
        )
        if account:
            new_balance = account[0][0] + amount
            db.execute_query(
                    "UPDATE account SET balance = ? WHERE accountnumber = ? AND userId = ?",
                    (new_balance, account_number, user_id), False, True
                )
            # Record transaction
            valueDep="deposit"
            db.execute_query(
                "INSERT INTO transactions (accountnumber, type, amount) VALUES (?, ?, ?)",
                (account_number, valueDep, amount), False, True
            )
            return True
        return False
    @staticmethod
    def getTransactions(account_number):
        transactions = db.execute_query(
                "SELECT type, amount, timestamp FROM transactions WHERE accountnumber = ? ORDER BY timestamp DESC",
                (account_number,), True, False
            )
        return transactions


    @staticmethod
    def deleteAccount(account_number, user_id):
        # Delete the account only if it belongs to the user
        result = db.execute_query(
            "SELECT * FROM account WHERE accountnumber = ? AND userId = ?",
            (account_number, user_id), True, False
        )
        if result:
            db.execute_query(
                "DELETE FROM account WHERE accountnumber = ? AND userId = ?",
                (account_number, user_id), False, True
            )
            db.execute_query(  # Optionally delete associated transactions
                "DELETE FROM transactions WHERE accountnumber = ?",
                (account_number,), False, True
            )
            return True
        return False


