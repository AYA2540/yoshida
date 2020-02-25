import mysql.connector
from flask import Flask, render_template, request, redirect, session
from datetime import datetime
from flask_bcrypt import Bcrypt
import string, secrets
import locale
# locale.setlocale(locale.LC_CTYPE, "Japanese_Japan.932")

app = Flask(__name__)
app.secret_key = "98jf93js9s5j9si9p"
bcrypt = Bcrypt(app)

def pass_gen(size=12):
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits + '%&$#()'
    return ''.join(secrets.choice(chars) for x in range(size))

@app.route("/wRqZejFP_8X")
def user_list():
    # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
    conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
    c = conn.cursor()
    c.execute("select id, name, flag from users")
    user_list = []
    for row in c.fetchall():
        user_list.append({"id":row[0], "name":row[1], "flag":row[2]})
    conn.close()
    return render_template("list.html" , user_list = user_list)

# 入店ボタンを押した時
@app.route("/S5D$7esCgLM(", methods=["POST"])
def enter_yes(id):
    guest = request.form.get("number")
    enter_time = datetime.now().strftime("%m/%d %H:%M")
    # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
    conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
    c = conn.cursor()
    c.execute("insert into times values(null,%s,null,%s,%s)" , (enter_time,id,guest))
    c.execute("update users set flag = 1 where id = %s" ,(id,))
    conn.commit()
    conn.close()
    return redirect("/S5D$7esCgLM(")

# 退店ボタンを押した時
@app.route("/YPk~v.rPh#v8/<int:id>")
def out_yes(id):
    out_time = datetime.now().strftime("%m/%d/ %H:%M")
    # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
    conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
    c = conn.cursor()
    c.execute("update users set flag = 0 where id = %s" ,(id,))
    c.execute("update times set out_time = %s where user_id = %s and out_time is null" ,(out_time ,id))
    conn.commit()
    conn.close()
    return redirect("/YPk~v.rPh#v8")

# ログイン
@app.route("/HBZT,+FQhi*", methods=["GET","POST"])
def login():
    if request.method == "GET":
        if "user_id" in session:
            return redirect("/SwWn#*CW*z/,")
        else:
            return render_template("login.html")
    else:
        name = request.form.get("name")
        # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
        conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
        c = conn.cursor()
        c.execute("select password from users where name = %s", (name,))
        password = c.fetchone()
        if password is None:
            return render_template("login.html")
        else:
            password = password[0]
        c.execute("select salt from users where name = %s" , (name,))
        salt = c.fetchone()[0]
        conn.close()

        result = bcrypt.check_password_hash(password, request.form.get("password") + salt)
        if result == True:
            # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
            conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
            c = conn.cursor()
            c.execute("select id from users where password = %s",(password,))
            user_id = c.fetchone()
            conn.close()
            print(type(user_id))
            if user_id is None:
                return render_template("login.html")
            else:
                session['user_id'] = user_id[0]
                return redirect("/SwWn#*CW*z/,")
        else:
            return render_template("login.html")

# 入店状況確認ページ
@app.route("/SwWn#*CW*z/,")
def enter():
    if "user_id" in session:
        # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
        conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
        c = conn.cursor()
        c.execute("select count(*) from users where flag = 1")
        member = c.fetchone()
        member = member[0]

        c.execute("select sum(guest) from times where out_time is null")
        guest = c.fetchone()
        guest = guest[0]
        if guest is not None:
            guest = guest
        else:
            guest = 0

        member = member + guest
        
        user_id = session["user_id"]

        c.execute("select users.id, users.name, times.enter_time , times.guest from users join times on users.id = times.user_id where users.flag = 1 and out_time is null group by users.name order by times.enter_time asc")
        user_list = []
        for row in c.fetchall():
            user_list.append({"id":row[0], "name":row[1], "enter_time":row[2] , "guest":row[3]})
        conn.close()
        return render_template("enter.html" , user_list = user_list , member = member , user_id = user_id)
    else:
        return redirect("/HBZT,+FQhi*")

@app.route("/DijdZbQFXcUf" ,methods=["GET"])
def welcome():
    return render_template("welcome.html")

@app.route("/)SdYMP/k)SDK" ,methods=["GET"])
def thanks():
    return render_template("thanks.html")

# オーナーページ
@app.route("/B8)$h9r|Zh6w")
def owner():
    if "user_id" in session:
        user_id = session["user_id"]
        if user_id == 1:
            # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
            conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
            c = conn.cursor()
            c.execute("select count(*) from users")
            member = c.fetchone()
            member = member[0]

            c.execute("select id, name from users")
            user_list = []
            for row in c.fetchall():
                user_list.append({"id":row[0], "name":row[1]})
            conn.close()
            return render_template("owner.html" , user_list = user_list , member = member)
        else:
            return redirect("/SwWn#*CW*z/,")
    else:
        return redirect("/HBZT,+FQhi*")

# 退会
@app.route("/uKd4NC3T*fcR/<int:id>")
def del_trash(id):
    # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
    conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
    c = conn.cursor()
    c.execute("delete from users where id = %s" , (id,))
    conn.commit()
    conn.close()
    return redirect("/B8)$h9r|Zh6w")

@app.route("/_WanMc2mx~3f", methods=["POST"])
def regist():
        name = request.form.get("name")
        salt = pass_gen()
        password = bcrypt.generate_password_hash(request.form.get("password") + salt).decode('utf-8')
        # conn = mysql.connector.connect(user='root',password='A7RmwDLh-Uci',host='127.0.0.1',database='yoshida')
        conn = mysql.connector.connect(user='be0df0a2c105ea',password='71cdc06b',host='us-cdbr-iron-east-04.cleardb.net',database='heroku_c42eab1ee628ff3')
        c = conn.cursor()
        c.execute("insert into users values(null,%s,%s,0,%s)",(name,password,salt))
        conn.commit()
        conn.close()
        return redirect("/B8)$h9r|Zh6w")

@app.route("/ihXW3ay/5CY")
def ownerregist():
        return render_template("ownerregist.html")

@app.route("/Av4|4cV+sRm9")
def logout():
    session.pop("user_id" ,None)
    return redirect("/HBZT,+FQhi*")

if __name__ == "__main__":
    app.run()