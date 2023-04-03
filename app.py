from flask import Flask, render_template, request, session, redirect, json
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "secre"
app.permanent_session_lifetime = timedelta(days=7)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///sign.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Sign(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(120), nullable=False)
    Password = db.Column(db.String(120), nullable=False)

with open("config.json", "r") as f:
    credential = json.load(f)['user_details']

def mi():
    if "ema" in session:
        b = "g"
    else:
        b = "d"
    return render_template("mains.html", a=b)

@app.route("/")
def home():
    if "ema" in session:
        b = "g"
    else:
        b = "d"
    return render_template("index.html", a=b)

@app.route("/signup", methods=['GET', "POST"])
def signin():
    if "ema" in session:
        b = "g"
    else:
        b = "d"

    n = "s"

    if "ema" in session:
        return redirect("/Logout")

    if request.method == "POST":
        nam = request.form['full-name']
        ema = request.form['email']
        passs = request.form['pass']
        sin = Sign(name=nam, Email=ema, Password=passs)
        find_user = Sign.query.filter_by(name=nam).first()
        found_email = Sign.query.filter_by(Email=ema).first()
        if find_user or found_email:
            print("please go on login")
        else:
            db.session.add(sin)
            db.session.commit()

            session.permanent = True
            session['ema'] = ema

            alsl = Sign.query.all()
            print(alsl)
            return redirect("/Logout")
    return render_template("Signup.html", a=b, m=n)

@app.route("/Login", methods=['GET', "POST"])
def Login():
    if "ema" in session:
        b = "g"
    else:
        b = "d"

    n = "l"
    if "ema" in session:
        return redirect("/Logout")

    if request.method == "POST":
        nam = request.form['full-name']
        ema = request.form['email']
        passs = request.form['pass']
        found_user = Sign.query.filter_by(name=nam).first()
        found_email = Sign.query.filter_by(Email=ema).first()
        found_pass = Sign.query.filter_by(Password=passs).first()
        if found_user and found_email and found_pass:
            session["ema"] = found_user.Email
            session.permanent = True
            session['ema'] = ema

            alsl = Sign.query.all()
            print(alsl)
            return redirect("/Logout")
        else:
            print("please signup")
    return render_template("Signup.html", a=b, m=n)

@app.route("/Logout", methods=['GET', 'POST'])
def logout():
    if "ema" in session:
        b = "g"
    else:
        b = "d"

    if request.method == "POST":
        session.pop("ema")
        return redirect("/")
    return render_template("Logout.html", a=b)

@app.route("/service/<name>", methods=['GET', 'POST'])
def serve(name):
    if "ema" in session:
        b = "g"
    else:
        b = "d"

    print(name)
    if name == "Annually":
        c = "a"

    else:
        c = "m"
    return render_template("services.html", c=c, a=b)

@app.route("/pay")
def pay():
    return render_template("pay.html")

@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/about")
def about():
    if "ema" in session:
        b = "g"
    else:
        b = "d"

    return render_template("about.html", a=b)

@app.route("/view", methods=["GET", "POST"])
def users():
    if "ema" in session:
        b = "g"
    else:
        b = "d"

    if request.method == "POST":
        emai = request.form["emaill"]
        pasd = request.form["pas"]
        
        if credential["email"] == emai and credential["password"] == pasd:
            session["emai"] = emai
            return render_template("view.html", user=Sign.query.all(), a=b)

    if "emai" in session and session['emai'] == credential["email"]:
        return render_template("view.html", user=Sign.query.all(), a=b)
    
    return render_template("o.html")

@app.route("/b")
def de():
    session.pop("emai")
    return redirect("/")

@app.route("/delete/<int:sno>")
def delet(sno):
    user_detail = Sign.query.filter_by(sno=sno).first()
    db.session.delete(user_detail)
    db.session.commit()
    return redirect("/view")

if __name__ == "__main__":
    # db.create_all()
    app.run(debug=True)