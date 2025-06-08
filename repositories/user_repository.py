from data import db
class User:
    def __init__(self,id,name,email,password):
        self.userId=id
        self.username=name
        self.email=email
        self.password=password
    def __repr__(self):
        print(f" The object created for {self.username}")
    @staticmethod
    def createUser(username,email,password):
        db.execute_query("""CREATE TABLE IF NOT EXISTS USER (userId integer primary key autoincrement
                         ,username text
                         ,email text
                         ,password text)""",None,False,True)
        data=db.execute_query("select * from USER where email=?",(email,),True,False)
        print(data)
        if data:
            return False           
        if db.execute_query("""INSERT INTO USER (username,email,password) VALUES (?,?,?)""",(username,email,password),False,True):
            return True
        else:
            return False
        
    @staticmethod
    def login(email,password):
        data=db.execute_query("select * from USER where email=? and password=?",(email,password),True,False)
        return data
    @staticmethod
    def getUserById(userId):
        data=db.execute_query("select * from USER where userId=? ",(userId,),True,False)
        return data
        
        
        
    