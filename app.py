from flask import Flask, g, render_template, request, redirect, jsonify, session
from db import db, User, Issue, Question, Answer
import functools

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SECRET_KEY"] = "8bc7016d5fdffa0d7b4826cac7b94a29"

class EmailException(Exception):
    pass

@app.route("/", methods=["GET"])
def main():
    if g.user is None:
        logged_in = False
        name = None
    else:
        logged_in = True
        name = g.user.name
    return render_template("index.html", logged_in=logged_in, name=name)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/login")
        return view(**kwargs)
    
    return wrapped_view


@app.before_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.query(User).filter(User.userId == user_id).first()


@app.route("/latest", methods=["GET"])
def latest():
    # lookup db
    # return a dictionary with following keys:
    # title, theme, created_by, questions, replies
    # questions :: [String]
    # replies :: [(String, String)]; first string is name, second is the answer
    
    return jsonify({
        
    })


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    if request.method == "GET":
        return render_template("new.html")
    else:
        # do something
        return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        # do something
        try:
            emails = db.session.query(User.email).all()
            for email in emails:
                if email[0] == request.form.get("email"):
                    raise EmailException
                    
            new_user = User(
                name = request.form.get("name"),
                email = request.form.get("email"),
                password = request.form.get("pw"),
                replied = False
            )
            
            db.session.add(new_user)
            db.session.commit()
            
            message = "success"
        except EmailException:
            message = "email"
        except Exception as e:
            print(e)
            message = "fail"
        
        return jsonify({
            "message": message
        })
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # do something
        userId = None
        try:
            email = request.form.get("email")
            password = request.form.get("pw")
            user_info = db.session.query(User.userId, User.password).filter(User.email == email).first()
            userId, real_pw = user_info
            if real_pw is None:
                raise EmailException
            elif password != real_pw:
                message = "password"
            else:
                session.clear()
                session["user_id"] = userId
                message = "success"
        except EmailException:
            message = "email"
        except Exception as e:
            message = "fail"
            print(e)
        return jsonify({
            "message": message,
            "userId": userId
        })


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect('/')


@app.route("/ask", methods=["GET", "POST"])
@login_required
def ask():    
    if request.method == "GET":
        return render_template("ask.html", name="Test", theme="test2", issueID="t")
    else:
        # do something
        return jsonify({
            "message": "success"
        })
    

@app.route("/reply", methods=["GET", "POST"])
@login_required
def reply():    
    if request.method == "GET":
        # get db for all questions in latest issue
        return render_template("reply.html")
    else:
        # do something
        return jsonify({
            "message": "success"
        })


@app.route("/previous", methods=["GET"])
def previous():
    # get db
    return render_template("previous.html")


db.init_app(app)
with app.app_context():
    db.create_all()


app.run(debug=True)