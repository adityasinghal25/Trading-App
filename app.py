from flask import Flask , render_template , request , session, send_file , url_for
import sqlite3
import requests
from datetime import datetime
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive Agg backend
import matplotlib.pyplot as plt
import io
import pytz

#initialising flask 
app = Flask(__name__)



#initialising sessions in FLASK
app.config['SECRET_KEY'] = 'your_secret_key'



#*********Start******** (with home page)



#initialising empty username1 for using it globally in homebuttons
Username1 = ""

# web app home page template
@app.route('/')
def nav():
    return render_template("index.html")
 
#login page template
@app.route('/login')
def log():
    return render_template('login.html')

#signup page template
@app.route('/signup')
def sign():
    return render_template('signup.html')

#response of login page
@app.route('/logcomplete',methods=["POST"])
#In Python, None is considered False in a boolean context, and any other value is considered True.
#cur.fetchone() retrieves the first row that matches the query. If no matching row is found, cur.fetchone() returns None.
#this(cur.fetchone) is stored in user , if user is none(false) that means no db match was found
def logcomplete():
      if request.method == "POST":
        Username1 = request.form.get("Username1")
        Password1 = request.form.get("Password1") 
        
        if not Username1 or not Password1:
            return "<h1>Invalid username or password</h1>"

        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT UserId, Username , Email, Password, Type, Address, PhoneNo FROM Users WHERE Username = ? AND Password = ?" , (Username1, Password1))
                row = cur.fetchone()
                
                if row:
                    #Use case of session :- Can be called globally(anywhere)
                    userid = row[0]
                    username = row[1]

                    #Here , unique UserID and Username is stored in session when a user/admin logs-in
                    session['UserId'] = userid
                    session['Username'] = username
                    
                    msg = "Login successful!"
                    # table headings are like elements of an array in database table where in this case type is at position 4
                    if(row[4]=="admin"):
                        #for badges on the menu (view users , view shares and inbox)
                        cur.execute('SELECT COUNT(*) FROM Users')
                        user = cur.fetchone()
                        users = user[0]
                        session['users'] = users
                        
                        cur.execute('SELECT COUNT(*) FROM Shares')
                        share = cur.fetchone()
                        shares = share[0]
                        session['shares'] = shares

                        cur.execute('SELECT COUNT(*) FROM Inbox_admin')
                        query = cur.fetchone()
                        queries = query[0]
                        session['queries'] = queries

                        return render_template ("adminlogin.html",users=users,shares=shares,queries=queries)
                    else:
                        #Getting the UserID via session
                        userid = session.get('UserId')

                        #for badge on usermenu(inbox notifications)
                        cur.execute("SELECT COUNT(*) FROM Inbox_user WHERE UserId=? OR Status='all'",(userid,))
                        tip = cur.fetchone()
                        tips = tip[0]
                        session['tips'] = tips

                        return render_template("userlogin.html", Username1=Username1,tips=tips)
                else:
                    msg = "Incorrect username or password!! . Please Sign-up first..."
        except Exception as e:
            msg = f"Error during login: {e}"
        
        return render_template("login.html", msg=msg)

#response of signup page
@app.route('/signcomplete',methods=["POST"])
def signcomplete():
    Username2 = request.form.get("Username2")
    Email2 = request.form.get("Email2")
    Password2 = request.form.get("Password2")
    
    if not Username2 or not Email2  or not Password2:
        return "<h1>Invalid username and password</h1>"

    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Users (Username, Email, Password) VALUES (?, ?, ?)", (Username2, Email2, Password2))
            con.commit()
            msg = "You have successfully signed up . Please proceed to login page"
    except Exception as e:
        msg = f"Error in the Insert: {e}"

    return render_template("result1.html", msg=msg)








# ******MAIN code******* (after logging in) 





#ADMIN PAGE



#go back (home) function for admin
@app.route('/home1')
def goback1():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    return render_template("adminlogin.html",users=users,shares=shares,queries=queries)

#add compnay from page
@app.route('/addcompany')
def addcompany():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    return render_template("addcompany.html",users=users,shares=shares,queries=queries)

#response of add company
@app.route('/companycomplete',methods=["POST"])
def companycomplete():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    c_id = request.form.get("c_id")
    c_name = request.form.get("c_name")
    c_symbol = request.form.get("c_symbol")
    c_address = request.form.get("c_address")
    c_phoneno = request.form.get("c_phoneno")
    c_faxno = request.form.get("c_faxno")
    c_city = request.form.get("c_city")
    c_profile = request.form.get("c_profile")
    c_turnover = request.form.get("c_turnover")
    c_type = request.form.get("c_type")
    c_username = request.form.get("c_username")
    c_password = request.form.get("c_password")

    if not c_id or not c_name or not c_address or not c_phoneno or not c_faxno or not c_city or not c_profile or not c_turnover or not c_type or not c_username or not c_password:
        return "<h1>PLease enter all fields correctly</h1>"

    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Companies (CompanyId   ,CompanyName  ,Symbol ,CompanyAddress   ,CompanyPhoneNo   ,CompanyFaxNo   ,CompanyCity   ,CompanyProfile   ,CompanyTurnover   ,CompanyType   ,CompanyUsername   ,CompanyPassword   ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)", (c_id   ,c_name  ,c_symbol ,c_address   ,c_phoneno   ,c_faxno   ,c_city , c_profile   ,c_turnover   ,c_type   ,c_username   ,c_password))
            con.commit()
            msg = "Company data entered successfully"
    except Exception as e:
        msg = f"Error in the Insert: {e}"

    return render_template("resultadmin.html", msg=msg,users=users,shares=shares,queries=queries)

#add share form page  
@app.route('/addshare')
def addshare():
        #getting number of user and shares value for admin page
        users = session.get('users') 
        shares = session.get('shares')
        queries = session.get('queries')

       #Sending list of companies to Add Share select tag
        Companies = []
        try:
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT CompanyName FROM Companies")
                Companies = cur.fetchall()
                Companies = [company[0] for company in Companies]   #explain this step. Why and How tuple formation??
                #print(Companies)
                con.commit()
            return render_template("addshare.html",Companies=Companies,users=users,shares=shares,queries=queries)
        except Exception as e:
            msg = f"Error in the Insert: {e}"
        return render_template("adminlogin.html",users=users,shares=shares,queries=queries)

#response of add share
@app.route('/sharecomplete',methods=["POST"])
def sharecomplete():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    company_name = request.form.get("company_name")
    shares_id = request.form.get("shares_id")
    company_type = request.form.get("company_type")
    description = request.form.get("description")
    total = request.form.get("total")
    sold = request.form.get("sold")
    left = request.form.get("left")
    nav = request.form.get("nav")
    current_date = datetime.now().date()

    if not company_name or not shares_id or not company_type or not description or not total or not sold or not left or not nav or not current_date:
        return "<h1>PLease enter all fields correctly</h1>"
    
    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Shares (CompanyName  ,SharesId  ,CompanyType  ,SharesDescription  ,TotalShares  ,SharesSold  ,SharesLeft  ,StartNAV  ,date_share ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (company_name, shares_id, company_type, description, total, sold, left, nav, current_date))
            
            #updating session values
            shares=shares+1
            session['shares'] = shares
            shares = session.get('shares')

            con.commit()
            msg = "Share data entered successfully"
    except Exception as e:
        msg = f"Error in the Insert: {e}"

    return render_template("resultadmin.html", msg=msg,users=users,shares=shares,queries=queries)

#implementing View Shares normally
@app.route('/viewsharesadmin')
def viewsharesadmin():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        
        cur.execute('SELECT rowid,CompanyName,SharesId,CompanyType,SharesDescription,TotalShares,SharesSold,SharesLeft,StartNAV,date_share FROM Shares')
        rows = cur.fetchall()

        con.commit()
    return render_template("viewsharesadmin.html",rows=rows,shares=shares,users=users,queries=queries)

#add user form page
@app.route('/adduser')
def adduser():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')
    
    return render_template("adduser.html",users=users,shares=shares,queries=queries)

#response of adding user
@app.route('/usercomplete',methods=["POST"])
def usercomplete():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    au_username = request.form.get("au_username")
    au_email = request.form.get("au_email")
    au_password = request.form.get("au_password")
    au_type = request.form.get("au_type")
    au_address = request.form.get("au_address")
    au_phoneno = request.form.get("au_phoneno")
    
    if not au_username or not au_email or not au_password or not au_type or not au_address or not au_phoneno:
        return "<h1>PLease enter all fields correctly</h1>"

    try:
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Users (Username, Email, Password, Type, Address, PhoneNo) VALUES (?, ?, ?, ?, ?, ?)", (au_username  , au_email  , au_password  , au_type  , au_address  , au_phoneno))
            con.commit()

            #updating session values
            users=users+1
            session['users'] = users
            users = session.get('users') 

            msg = "User Data was added... Try Logging in now!!"
    except Exception as e:
        msg = f"Error in the Insert: {e}"

    return render_template("resultadmin.html", msg=msg,users=users,shares=shares,queries=queries)





#implementing view user with actions column in TABLE
@app.route('/viewuser')
def viewuser():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('SELECT rowid, Username, Email, Type , Address, PhoneNo FROM Users')
        rows = cur.fetchall()
        con.commit()
        return render_template("viewuser.html",rows=rows,users=users,shares=shares,queries=queries)


#editing and deleting table data

#1-> taking selected row to edit-form page using hidden row-id(initialised by defualt in db when creating table)
@app.route('/edit',methods=["POST","GET"])
def edit():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    rows = []
    if request.method == "POST":
        try:
            id = request.form.get("id")
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('SELECT rowid, Username, Email, Type , Address, PhoneNo FROM Users WHERE rowid ='+ id)
                rows = cur.fetchall()
                con.commit()
        except Exception as e:
            msg = f"Error in the Insert: {e}"
        return render_template("edit.html",rows=rows,users=users,shares=shares,queries=queries)

#2-> bringing new value through form and getting them into the database
@app.route('/editrec',methods=["POST","GET"])
def editrec():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    if request.method == "POST":
        try:
            id = request.form.get("id")
            au_username = request.form.get("au_username")
            au_email = request.form.get("au_email")
            au_type = request.form.get("au_type")
            au_address = request.form.get("au_address")
            au_phoneno = request.form.get("au_phoneno")
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('UPDATE Users SET Username=?,Email=?,Type=?,Address=?,PhoneNo=? WHERE rowid='+ id ,(au_username  , au_email , au_type  , au_address  , au_phoneno))
                con.commit()
                msg = "All changes were recorded"
        except Exception as e:
            msg = f"Error in the Insert: {e}"
        return render_template("resultadmin.html",msg=msg,users=users,shares=shares,queries=queries)

#3-> deleting selected data using hidden row-id(initialised by defualt in db when creating table)
@app.route('/deleterec',methods=["POST","GET"])
def deleterec():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')
    id = request.form.get('id')

    if request.method == "POST":
        try:
            
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('DELETE FROM Users WHERE rowid ='+ id)
                con.commit()

                #updating session values
                users=users-1
                session['users'] = users
                users = session.get('users')

                msg = "The desired row was deleted from database"
        except Exception as e:
            msg = f"Error in the Insert: {e}"
        return render_template("resultadmin.html", msg=msg,users=users,shares=shares,queries=queries)


#implementing table that shows inbox to admin containing queries from users
@app.route('/inboxadmin')
def inboxadmin():
    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('SELECT rowid, "From" , Feedback FROM Inbox_admin')
        rows = cur.fetchall()
        con.commit()
        return render_template("viewadmininbox.html",rows=rows,users=users,shares=shares,queries=queries)

#Query solution by admin (buttons resolve and reject)
@app.route('/userquery',methods=["POST"])
def userquery():
    id = request.form.get('id')

    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM Inbox_admin WHERE rowid=?',(id,))
        
        #updating session values
        queries = queries - 1
        session['queries'] = queries
        queries = session.get('queries')

        msg = "ADMIN dealt with User query"
        con.commit()
        return render_template("resultadmin.html",msg=msg,users=users,shares=shares,queries=queries)



#implementing send message form from admin to user
@app.route('/sendtippage')
def sendtippage():
    Customers = []

    #getting number of user and shares value for admin page
    users = session.get('users') 
    shares = session.get('shares')
    queries = session.get('queries')

    with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute("SELECT Username FROM Users WHERE Type=?",("customer",))
                Customers = cur.fetchall()
                Customers = [Customer[0] for Customer in Customers]   
                con.commit()
    return render_template('sendtip.html',users=users,shares=shares,queries=queries,Customers=Customers)


@app.route('/tipsent', methods=["POST"])
def tipsent():
    # Getting number of user and shares value for admin page
    users = session.get('users')
    shares = session.get('shares')
    queries = session.get('queries')

    selected_user = request.form.get('selected_user')
    tip = request.form.get('tip')

    if not tip:
        msg = "Please enter a tip."
        return render_template('resultadmin.html', msg=msg, users=users, shares=shares, queries=queries)

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()

        #print(selected_user)
        if selected_user == "all":
            status = "all"
            userid = 0
        else:
            status = "unique"
            cur.execute('SELECT UserId FROM Users WHERE Username=?', (selected_user,))
            userid = cur.fetchone()
            userid = userid[0]
        # Sending message to a specific or all user
        cur.execute('INSERT INTO Inbox_user (Message, UserId, Status) VALUES (?, ?, ?)', (tip, userid, status))
        con.commit()
        msg = "Your tip was sent successfully."

    return render_template('resultadmin.html', msg=msg, users=users, shares=shares, queries=queries)





# CUSTOMER PAGE
# Normally means without 'Action' buttons like edit,delete,etc


#go back (home) function for customer
@app.route('/home2')
def goback2():

    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    return render_template("userlogin.html",Username1=Username1,tips=tips)



#implementing view portfolio normally
@app.route('/viewportfolio')
def viewportfolio():

    #Getting the UserID via session
    userid = session.get('UserId')
    #print(userid)

    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('SELECT rowid, PortfolioId , CompanyName , SharesId , NetAssetValue , Units , Amount , date_buyshare , Exchange FROM BuyShares WHERE UserID=?',(userid,))
        rows = cur.fetchall()
        cur.execute('SELECT SUM(Amount) FROM BuyShares WHERE UserID=?',(userid,))
        sum1 = cur.fetchone()
        con.commit()
        return render_template("viewportfolio.html",rows=rows,sum1=sum1,Username1=Username1,tips=tips)


#add funds on customer login
@app.route('/fundsadded',methods=["POST"])
def fundsadded():
    funds = request.form.get("funds")

    #Getting the UserID via session
    userid = session.get('UserId')
    
    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    try:
        funds = float(funds)
        with sqlite3.connect('database.db') as con:
            cur = con.cursor()
            #IMP- QWhy did we put comma after funds: When you pass a single value to a parameterized query, it should still be in the form of a tuple. In Python, a single-element tuple is defined by placing a comma after the element inside parentheses.
            #print('UPDATE Users SET Funds=Funds+? WHERE rowid=?',(funds,rowid))
            cur.execute('UPDATE Users SET Funds=Funds+? WHERE UserId=?',(funds,userid))
            con.commit()
            msg = "Funds were added successfully to your trading account"
    except Exception as e:
        msg = f"Error in the Update: {e}"

    return render_template("resultuser.html", msg=msg,Username1=Username1,tips=tips)


#implementing View Company normally
@app.route('/viewcompany')
def viewcompany():

    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('SELECT rowid,  CompanyId   ,CompanyName   ,CompanyAddress   ,CompanyPhoneNo   ,CompanyFaxNo   ,CompanyCity   ,CompanyProfile   ,CompanyTurnover   ,CompanyType    FROM Companies')
        rows = cur.fetchall()
        con.commit()
        return render_template("viewcompany.html",rows=rows,Username1=Username1,tips=tips)


#implementing View Shares normally
@app.route('/viewshares')
def viewshares():
    #Getting the UserID via session
    userid = session.get('UserId')
    
    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        ####VERY IMPORTANT QUERY
        cur.execute('SELECT Shares.rowid, Shares.CompanyName , IFNULL(BuyShares.Units, 0) as OwnedUnits , Shares.SharesId, Shares.CompanyType, Shares.SharesDescription, Shares.StartNAV FROM Shares LEFT JOIN BuyShares ON Shares.SharesId = BuyShares.SharesId AND BuyShares.UserId = ?', (userid,))
        rows = cur.fetchall()
        con.commit()
        return render_template("viewshares.html",rows=rows,Username1=Username1,tips=tips)


#implementing View Funds normally
@app.route('/viewfunds')
def viewfunds():
    #Getting the UserID via session
    userid = session.get('UserId')
    
    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('SELECT Funds FROM Users WHERE UserId=?',(userid,))
        row = cur.fetchone()
        con.commit()
        return render_template("viewfunds.html",row=row,Username1=Username1,tips=tips)


#implementing 'BUY' Button on View Shares
@app.route('/buynew',methods=['POST','GET'])
def buynew():
    rows = []
    
    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    if request.method == "POST":
        try:
            id = request.form.get("id")
            #print(id)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('SELECT ROWID,CompanyName,SharesId,CompanyType,SharesDescription,StartNAV FROM Shares WHERE ROWID=?',(id,))
                rows = cur.fetchall()
                con.commit()
        except Exception as e:
            msg = f"Error in the Insert: {e}"
        #print(rows)
    return render_template("bnew.html",rows=rows,Username1=Username1,tips=tips)


#managing Buy-Order coming from Buy button
@app.route('/editbnew',methods=["POST","GET"])
def editbnew():

    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    if request.method == "POST":
        try:
            # id = request.form.get("id")
            quan = request.form.get("quantity")
            val = request.form.get("value")
            share_id = request.form.get("share_id")
            company_name1 = request.form.get("company_name1")

            #Getting the UserID via session
            userid = session.get('UserId')
            
            #changing datatypes for multiplication
            quantity = int(quan)
            value = float(val)

            # Get the current date and time
            current_date = datetime.now()

            #calculating amount (in Rs) of shares bought
            amount = quantity*value

            with sqlite3.connect('database.db') as con:
                cur = con.cursor()

                # Check if user has sufficient funds
                cur.execute('SELECT Funds FROM Users WHERE UserId = ?', (userid,))
                result1 = cur.fetchone()

                if not result1:
                    msg = "User not found"
                    return render_template("resultuser.html", msg=msg)

                funds = result1[0]

                if funds < float(amount):
                    msg = "Insufficient Funds!! Please Add Funds and try again"
                    return render_template("resultuser.html", msg=msg)


                # Retrieve PortfolioID using UserID
                cur.execute('SELECT PortfolioID FROM Portfolio WHERE UserId = ?', (userid,))
                result3 = cur.fetchone()

                if not result3:
                    # Generate new PortfolioID if it doesn't exist
                    cur.execute('INSERT INTO Portfolio (UserId) VALUES (?)', (userid,))
                    cur.execute('SELECT last_insert_rowid()')
                    result3 = cur.fetchone()

                portfolio_id = result3[0]

                # Check if the user already has shares of the same type
                cur.execute('SELECT SharesId FROM BuyShares WHERE UserId = ? AND SharesId = ?', (userid, share_id))
                result2 = cur.fetchone()

                if result2:
                    # User already owns shares of this type, update existing entry
                    cur.execute('UPDATE BuyShares SET Units = Units + ?, Amount = Amount + ? , date_buyshare = ? WHERE UserId = ? AND SharesId = ?', (quantity, amount , current_date , userid, share_id))
                else:
                    # Insert new entry in BuyShares
                    cur.execute("INSERT INTO BuyShares ( PortfolioId ,CompanyName, SharesId, NetAssetValue, Units, Amount , date_buyshare , UserId) VALUES (?, ?, ?, ?, ?, ?, ? ,?)", (portfolio_id,company_name1, share_id, value, quantity, amount, current_date , userid))

                # Update Shares table
                cur.execute('UPDATE Shares SET SharesSold = SharesSold + ?, SharesLeft = SharesLeft - ? WHERE SharesId = ?', (quantity, quantity, share_id))

                # Update user's funds
                cur.execute('UPDATE Users SET Funds = Funds - ? WHERE UserId = ?', (amount, userid))

                con.commit()
                msg = "BuyShare data entered successfully. Shares Data and Users Data were also updated."
        except Exception as e:
            msg = f"Error in the Insert or Update: {e}"
    return render_template("resultuser.html", msg=msg,Username1=Username1,tips=tips)


#implementing 'SELL' Button on View Shares
@app.route('/sellnew',methods=['POST','GET'])
def sellnew():
    rows = []
    
    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    if request.method == "POST":
        try:
            id = request.form.get("id")
            #print(id)
            with sqlite3.connect('database.db') as con:
                cur = con.cursor()
                cur.execute('SELECT ROWID,CompanyName,SharesId,CompanyType,SharesDescription,StartNAV FROM Shares WHERE ROWID=?',(id,))
                rows = cur.fetchall()
                con.commit()
        except Exception as e:
            msg = f"Error in the Insert: {e}"
        #print(rows)
    return render_template("snew.html",rows=rows,Username1=Username1,tips=tips)


#managing Sell-Order coming from Sell button
@app.route('/editsnew',methods=["POST","GET"])
def editsnew():
        #Getting Username from session
        Username1 = session.get('Username')
        #Getting Tips from session
        tips = session.get('tips')

        if request.method == "POST":
            try:
                share_id = request.form.get("share_id")
                quan = request.form.get("quantity")
                val = request.form.get("value")
                company_name1 = request.form.get("company_name1")

                # Getting the UserID via session
                userid = session.get('UserId')

                # Changing datatypes for multiplication
                quantity = int(quan)
                value = float(val)

                # Get the current date
                current_date = datetime.now()

                # Calculating amount (in Rs) of shares sold
                amount = quantity * value

                with sqlite3.connect('database.db') as con:
                    cur = con.cursor()

                    # Check if the user owns enough shares to sell
                    cur.execute('SELECT Units, Amount FROM BuyShares WHERE UserId = ? AND SharesId = ?', (userid, share_id))
                    result1 = cur.fetchone()

                    if not result1 or result1[0] < quantity:
                        msg = "Insufficient shares to sell!"
                        return render_template("resultuser.html", msg=msg)

                    owned_units = result1[0]
                    owned_amount = result1[1]

                    # Retrieve PortfolioID using UserID
                    cur.execute('SELECT PortfolioID FROM Portfolio WHERE UserId = ?', (userid,))
                    result2 = cur.fetchone()

                    if not result2:
                        msg = "Portfolio not found for the user!"
                        return render_template("resultuser.html", msg=msg)

                    portfolio_id = result2[0]

                    # Update BuyShares table (deletes row if units=0)
                    new_units = owned_units - quantity
                    new_amount = owned_amount - amount

                    if new_units > 0:
                        cur.execute('UPDATE BuyShares SET Units = ?, Amount = ?, date_buyshare = ? WHERE UserId = ? AND SharesId = ?', (new_units, new_amount, current_date, userid, share_id))
                    else:
                        cur.execute('DELETE FROM BuyShares WHERE UserId = ? AND SharesId = ?', (userid, share_id))

                    # Update Shares table
                    cur.execute('UPDATE Shares SET SharesSold = SharesSold - ?, SharesLeft = SharesLeft + ? WHERE SharesId = ?', (quantity, quantity, share_id))

                    # Update user's funds
                    cur.execute('UPDATE Users SET Funds = Funds + ? WHERE UserId = ?', (amount, userid))

                    con.commit()
                    msg = "SellShare data entered successfully. Shares Data and Users Data were also updated."
            except Exception as e:
                msg = f"Error in the Insert or Update: {e}"
        return render_template("resultuser.html", msg=msg,Username1=Username1)






# Global Values
API_KEY = 'XEP3D98IECUX0TCL'
IST = pytz.timezone('Asia/Kolkata')

# Real-time stock data function
def fetch_stock_data(symbol, interval, api_key):
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval={interval}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    time_series = data.get(f'Time Series ({interval})')
    
    if not time_series:
        raise ValueError("Error fetching data from Alpha Vantage API")
    
    times = []
    prices = []
    for time, price_data in time_series.items():
        #for Converting the time to datetime object in ET
        time_et = datetime.strptime(time, '%Y-%m-%d %H:%M:%S')
        #for Converting ET time to IST
        time_ist = time_et.replace(tzinfo=pytz.timezone('US/Eastern')).astimezone(IST)
        times.append(time_ist)
        prices.append(float(price_data['1. open']))
    times.reverse()
    prices.reverse()
    return times, prices

# Plotting the real-time data by calling the fetch_stock function
@app.route('/trends', methods=["POST"])
def trends():
    rowid = request.form.get("id")

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('SELECT CompanyName, Symbol FROM Companies WHERE rowid=?', (rowid,))
        result = cur.fetchone()

    if not result:
        return "<h1>Company not found</h1>"
    
    company_name, symbol = result
    
    if not symbol:
        return "<h1>No symbol found for this company</h1>"
    
    # Fetching the real-time stock data
    try:
        times, prices = fetch_stock_data(symbol, '1min', API_KEY)
    except Exception as e:
        return f"<h1>Error fetching data: {str(e)}</h1>"
    
    # Plotting the data
    plt.figure(figsize=(20, 10))  
    plt.plot(times, prices, marker='o', linestyle='-', color='b', label='Stock Price')
   
    # Adding labels and title
    plt.xlabel('Date-Time (IST)')
    plt.ylabel('Price ($)')
    plt.title(f'Real-Time Stock Prices for {company_name}')
    plt.xticks(rotation=45)  
    plt.grid(True)
    plt.legend()
    
    # Save the plot to a BytesIO object
    img = io.BytesIO()  # Create an in-memory bytes buffer
    plt.savefig(img, format='png')  # Save the plot to the buffer in PNG format
    img.seek(0)  # Rewind the buffer's file pointer to the beginning
    plt.close()  # Close the plot to free up memory

    return send_file(img, mimetype='image/png')



#change pw for customer
@app.route('/changepassword')
def changepassword():

    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    # Getting the UserID via session
    userid = session.get('UserId')

    return render_template('changepassword.html',Username1=Username1,userid=userid,tips=tips)

@app.route('/changecomplete', methods=["POST"])
def changecomplete():

    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    userid = request.form.get('userid')
    currentpw = request.form.get('currentpw')
    newpw = request.form.get('newpw')
    Confirmpw = request.form.get('Confirmpw')
    
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Users WHERE UserId=? AND Password=?', (userid, currentpw))
        row = cur.fetchone()
        
        # Check if the new password is the same as the current password
        if currentpw == newpw:
            msg = "You can't use your current password as your new password. Please try again."
            return render_template('changepassword.html', msg=msg ,Username1=Username1,tips=tips)
        
        # Check if the new password and confirmation password match
        if newpw != Confirmpw:
            msg = "The new password and confirmation password do not match. Please try again."
            return render_template('changepassword.html', msg=msg ,Username1=Username1,tips=tips)
        
        # Check if the current password is correct
        if not row:
            msg = "The current password you entered is incorrect. Please try again."
            return render_template('changepassword.html', msg=msg ,Username1=Username1,tips=tips)

        # Update the password
        cur.execute('UPDATE Users SET Password=? WHERE UserId=?', (newpw, userid))
        con.commit()
        msg = "Your password has been successfully changed!"
        
    return render_template("resultuser.html", msg=msg ,Username1=Username1,tips=tips)


#manage profile for customer
@app.route('/manageprofile')
def manageprofile():

    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    # Getting the UserID via session
    userid = session.get('UserId')

    #LEts get data from database using userid
    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM Users WHERE UserId=?',(userid,))
        rows = cur.fetchall()
        #print(rows)
        con.commit()
    return render_template('manageprofile.html',Username1=Username1,userid=userid,rows=rows,tips=tips)


@app.route('/managecomplete',methods=["POST"])
def managecomplete():
    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    newemail = request.form.get('newemail')
    newaddress = request.form.get('newaddress')
    newphoneno = request.form.get('newphoneno')
    userid = request.form.get('userid')


    if not newemail or not newaddress or not newphoneno:
        msg="You cant leave any fields empty"
        return render_template('manageprofile.html',msg=msg,Username1=Username1,tips=tips)

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('UPDATE Users SET Email=? , Address=? , PhoneNO=? WHERE UserId=?',(newemail,newaddress,newphoneno,userid))
        con.commit()
        msg = "Your profile was updated successfully"

    return render_template('resultuser.html',msg=msg,Username1=Username1,tips=tips)

#implementing feedback from user to admin inbox
@app.route('/sendfeedbackpage')
def sendfeedbackpage():
    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    return render_template('sendfeedback.html',Username1=Username1,tips=tips)

#sending feedback to database (admin_inbox table)
@app.route('/feedbacksent',methods=["POST"])
def feedbacksent():
    #Getting Username from session
    Username1 = session.get('Username')
    #Getting Tips from session
    tips = session.get('tips')

    # Getting the UserID via session
    userid = session.get('UserId')
    
    feedback = request.form.get('feedback')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()

        cur.execute('INSERT INTO Inbox_admin ("From", Feedback, UserId) VALUES (?, ?, ?)', (Username1, feedback, userid))
        con.commit()
        msg = "Your query was sent successfully"
    return render_template('resultuser.html',msg=msg,Username1=Username1,tips=tips)    


#implementing table that shows inbox to user containing tips from admin
@app.route('/inboxuser')
def inboxuser():
    #Getting Username from session
    Username1 = session.get('Username')
    # Getting the UserID via session
    userid = session.get('UserId')
    #Getting Tips from session
    tips = session.get('tips')
    

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("SELECT rowid, Message FROM Inbox_user WHERE UserId=? OR Status='all'",(userid,))
        rows = cur.fetchall()
        con.commit()
        return render_template("viewuserinbox.html",rows=rows,Username1=Username1,tips=tips)


#Admin tip/message handling (buttons mark as seen)
@app.route('/admintips',methods=["POST"])
def admintips():
    id = request.form.get('id')

    #Getting Username from session
    Username1 = session.get('Username')

    #getting number of tips for users page
    tips = session.get('tips')

    with sqlite3.connect('database.db') as con:
        cur = con.cursor()
        cur.execute('DELETE FROM Inbox_user WHERE rowid=?',(id,))
        
        #updating session values 
        tips = tips - 1
        session['tips'] = tips
        tips = session.get('tips')

        msg = "You have marked the message as read"
        con.commit()
        return render_template("resultuser.html",msg=msg,Username1=Username1,tips=tips)



#######-------------------Common Part for both Admins and Users----------------------#######

#logout (going back to Site Home page)
@app.route('/',methods=["POST"])
def logout1():
    return render_template("index.html")

#driver function
if __name__ == '__main__':
        app.run(debug=True)