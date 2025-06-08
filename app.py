from flask import Flask, render_template, request, redirect, url_for,session
from repositories import user_repository
from repositories import account_repository
app = Flask(__name__)
app.secret_key = '@dfsdas1d%' 
userId=0
result=None


@app.route('/')
def index():
    return render_template("register.html")
@app.route('/register', methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["mail"]
        password = request.form["password"]
        confirmpassword = request.form["confirmPassword"]
        
        # Check if the passwords match
        if password == confirmpassword:
            success = user_repository.User.createUser(username, email, password)
            if success:
                return render_template('registrationsuccess.html', value=True)
            else:
                return render_template('registrationsuccess.html', value=False)
        else:
            return render_template('registrationsuccess.html', value=False)
    return render_template("register.html")





@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        
        # Verify if the user exists and the password matches
        data = user_repository.User.login(email, password)
        

        if data and len(data) > 0:
            result=[user_repository.User(row[0], row[1], row[2], row[3]) for row in data]
            session["userId"]=result[0].userId
            accounts = account_repository.account.getAllAccount(result[0].userId)
            return render_template("dashboard.html",user=result,accounts=accounts)
        else:
            return render_template("login.html", error="Invalid email or password")
    
    return render_template("login.html")






@app.route("/createaccount", methods=["GET", "POST"])
def create_account():
    if request.method == "POST":
        accountType = request.form["accountType"]
        balance = float(request.form["balance"])
        userId = session["userId"]  # Replace with session user ID in real app
        success = account_repository.account.createAccount(userId, accountType, balance)
        return redirect("/dashboard")
    return render_template("create_account.html")





@app.route("/dashboard")
def dashboard():
    userId = session.get("userId")
    if userId is None:
        return redirect(url_for('login'))  # User not logged in

    user = user_repository.User.getUserById(userId)
    result=[user_repository.User(row[0], row[1], row[2], row[3]) for row in user]

    accounts = account_repository.account.getAllAccount(userId)

    return render_template("dashboard.html", user=result, accounts=accounts)







@app.route("/view_balance/<int:account_number>")
def viewbalance(account_number):
    accounts = account_repository.account.getAccountInfo(account_number)
    return f'Balance is {accounts[0][4]}'


@app.route('/delete/<int:account_number>', methods=["GET", "POST"])
def delete(account_number):
    user_id = session.get("userId")
    if not user_id:
        return redirect(url_for('login'))
    success = account_repository.account.deleteAccount(account_number, user_id)
    if success:
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for('login')) 

@app.route("/withdraw/<int:account_number>", methods=["GET", "POST"])
def withdraw(account_number):
    user_id = session.get("userId")
    if not user_id:
        return redirect(url_for('login'))

    if request.method == "POST":
        amount = float(request.form["amount"])
        success = account_repository.account.withdraw(account_number, user_id, amount)
        if success:
            return redirect(url_for("dashboard"))
        else:
            return render_template("withdraw.html", error="Insufficient funds or error occurred.", account_number=account_number)

    return render_template("withdraw.html", account_number=account_number)







@app.route("/deposit/<int:account_number>", methods=["GET", "POST"])
def deposit(account_number):
    user_id = session.get("userId")
    if not user_id:
        return redirect(url_for('login'))

    if request.method == "POST":
        amount = float(request.form["amount"])
        success = account_repository.account.deposit(account_number, user_id, amount)
        if success:
            return redirect(url_for("dashboard"))
        else:
            return render_template("deposit.html", error="Deposit failed.", account_number=account_number)

    return render_template("deposit.html", account_number=account_number)


@app.route('/logout',methods=["GET","POST"])
def logout():
    session["userId"]=0
    session.clear()
    return render_template('login.html')



@app.route("/transactions/<string:account_number>")
def transaction_history(account_number):
    user_id = session.get("userId")
    if not user_id:
        return redirect(url_for("login"))

    transactions = account_repository.account.getTransactions(account_number)
    return render_template("transactions.html", transactions=transactions, account_number=account_number)


if __name__ == '__main__':
    app.run(debug=True)
