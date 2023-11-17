from flask import Flask, g, render_template, request, redirect, jsonify, session
import functools

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/login")
        return view(**kwargs)
    
    return wrapped_view


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
        return jsonify({
            "message": "success"
        })
    

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    else:
        # do something
        return jsonify({
            "message": "success"
        })


@app.route("/ask", methods=["GET", "POST"])
def ask():    
    if request.method == "GET":
        return render_template("ask.html", name="Test", theme="test2", issueID="t")
    else:
        # do something
        print(request.json)
        return jsonify({
            "message": "success"
        })
    

@app.route("/reply", methods=["GET", "POST"])
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

app.run(debug=True)