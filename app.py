from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/new", methods=["GET", "POST"])
def new():
    if request.method == "GET":
        return render_template("new.html")
    else:
        # do something
        return redirect("/")

app.run(debug=True)