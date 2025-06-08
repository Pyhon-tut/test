import sqlite3

DATABASENAME="BankSystem.db"

def execute_query(query,para=None,fetch=False,commit=False):
    data=None
    conn=None
    try:
        conn=sqlite3.connect(DATABASENAME)
        cursor=conn.cursor()
        if para:
            cursor.execute(query,para)
        else:
            cursor.execute(query)
        if commit:
            conn.commit()
        if fetch:
            data=cursor.fetchall()
            if data and len(data) > 0:
                return data
            else:
                return False
        else:
            return True
        

    except Exception as e:
        print(f"The connecting error is {e}")
        return False
    

    
    finally:
        if conn:
            conn.close()        