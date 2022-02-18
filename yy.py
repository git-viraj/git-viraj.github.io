from flask import Flask, abort,request, session
from flask import render_template
import json

f= open('books.json')
d = json.load(f)
q=open('users.json')
users=json.load(q)


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/')
def index():
    if 'username' in session:
        return f"<h1> Welcome to my bookstore</h1> <br><br>logged in as {session['username']}"
    return 'You are not logged in <br><br><a href="/login">Click </a> here to login<br> New user can <a href="/reg">Register </a>here. '


@app.route('/books')
def books():
    if 'username' in session:
        return d
    return 'You are not logged in <br><br><a href="/login">Click </a> here to login<br> New user can <a href="/reg">Register </a>here. '

@app.route('/status')
def status():
    if 'username' in session:
        d={"status":"OK"}
        return d
    return 'You are not logged in <br><br><a href="/login">Click </a> here to login<br> New user can <a href="/reg">Register </a>here. '

@app.route('/books/<id>')
def book(id):
    if 'username' in session:
        for entry in d["data"]:
            if  str(entry["id"])==str(id):
                return entry
        abort(404)
    return 'You are not logged in <br><br><a href="/login">Click </a> here to login<br> New user can <a href="/reg">Register </a>here. '

@app.route('/add',methods=['POST'])
def add():
    if 'username' in session:
        request_data = request.get_json()
        dict=request_data

        if "id" in dict and "name" in dict and "type" in dict and "available" in dict:
            d["data"].append(dict)

            json_obj=json.dumps(d)
            with open("books.json", "w") as outfile:
                outfile.write(json_obj)
            return "successfully added book"
        return "{Fill correct details}"
    return 'You are not logged in <br><br><a href="/login">Click </a> here to login<br> New user can <a href="/reg">Register </a>here. '

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form:
            if request.form['username'] not in users :
                return "Wrong pass or username, try again " \
                       '''
                               <form method="post">
                                   <p> Username <input type=text name=username>
                                   <p> Password <input type=text name=password>
                                   <p><input type=submit value=Login>
                               </form>
                           '''
            if request.form['password']!=users[request.form['username']]["password"]:
                return "Wrong pass or username, try again " \
                       '''
                               <form method="post">
                                   <p> Username <input type=text name=username>
                                   <p> Password <input type=text name=password>
                                   <p><input type=submit value=Login>
                               </form>
                           '''

            session['username'] = request.form['username']
            session['password']= request.form['password']

        elif request.get_json():
            print(request.get_json())
            if request.get_json()['username'] not in users:

                return "Wrong pass or username, try again " \
                       '''
                               <form method="post">
                                   <p> Username <input type=text name=username>
                                   <p> Password <input type=text name=password>
                                   <p><input type=submit value=Login>
                               </form>
                           '''
            if request.get_json()['password'] != users[request.get_json()['username']]["password"]:
                return "Wrong pass or username, try again " \
                       '''
                               <form method="post">
                                   <p> Username <input type=text name=username>
                                   <p> Password <input type=text name=password>
                                   <p><input type=submit value=Login>
                               </form>
                           '''

            session['username'] = request.get_json()['username']
            session['password'] = request.get_json()['password']

        else:
            return "please pass username and password"

        return index()

    if request.method == 'GET':

        if 'username' in session:
            return index();

        return '''
            <form method="post">
                <p> Username <input type=text name=username>
                <p> Password <input type=text name=password>
                <p><input type=submit value=Login>
            </form>
        '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    session.pop('password', None)

    return index()

@app.route('/reg' , methods =['POST', 'GET'])
def reg():
    if 'username' in session:
        return f"you are already registered as {session['username']}"

    if request.method == 'GET':
        return '''
            <form method="post">
                <p> Username <input type=text name=username>
                <p> Email <input type=text name=email>
                <p> Contact No <input type=text name=contact>
                <p> Password <input type=text name=password>
                <p><input type=submit value=Register>
            </form>
                '''
    else:
        if request.get_json():
            request_data = request.get_json()
            dict = request_data
            print(request_data)
            if "username" in dict and "email" in dict and "contact" in dict and "password" in dict:
                users[dict['username']]={ "passwor":dict["password"], "email":dict["email"], "contact": dict["contact"]}

                json_obj = json.dumps(users)
                with open("users.json", "w") as outfile:
                    outfile.write(json_obj)

                session['username'] = dict['username']
                session['password'] = dict["password"]
                return index()
            return "{Fill all details correct}"

        if request.form:
            print(request.form)
            if request.form["username"] and request.form["email"] and request.form["password"] and request.form["contact"]:
                users[request.form["username"]] = {"passwor": request.form["password"], "email": request.form["email"],
                                           "contact": request.form["contact"]}

                json_obj = json.dumps(users)
                with open("users.json", "w") as outfile:
                    outfile.write(json_obj)

                session['username'] = request.form['username']
                session['password'] = request.form['password']
                return index()
            return "{Fill all details correct }"

        return " cant fill empty values"

app.run(debug=True)