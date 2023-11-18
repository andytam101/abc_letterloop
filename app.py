from flask import Flask, g, render_template, request, redirect, jsonify, session
from datetime import datetime
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
        
    issue = get_latest_issue(Issue.a_dl)
    # if issue.a_dl >= datetime.now():
    #     return render_template("index.html", logged_in=logged_in, name=name,valid=False)
    
    qs = get_questions(issue.issueId)
    questions = []
    for q in qs:
        this_ans = []
        for a in get_answers(q.quesId):
            this_ans.append({"name": get_user(a.userId).name, "content": a.content})
        questions.append({
            "name": get_user(q.userId).name,
            "content": q.content,
            "answers": this_ans 
        })
    
    return render_template("index.html", logged_in=logged_in, name=name,valid=True,
                            questions=questions, theme=issue.theme, username=issue.name, date=issue.date.strftime("%Y-%m-%d"),
                            issueId=issue.issueId, issueName=issue.name
                           )

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


def get_latest_issue(date):
    return db.session.query(Issue).order_by(date.desc()).first()

def get_user(userId):
    return db.session.query(User).filter(User.userId == userId).first()

def get_questions(issueId):
    return db.session.query(Question).filter(Question.issueId == issueId).all()

def get_answers(quesId):
    return db.session.query(Answer).filter(Answer.quesId == quesId).all()


@app.route("/new", methods=["GET", "POST"])
@login_required
def new():
    d = get_latest_issue(Issue.q_dl)
    if request.method == "GET":
        new_issue = not (d is not None and datetime.now() < d.q_dl)
        return render_template("new.html", new_issue=new_issue)
    else:
        # do something  
        try:
            if d is not None and datetime.now() < d.q_dl:
                return jsonify({"message": "ongoing"})
            
            form = request.form                  
            ques_dl = datetime.strptime(form.get("q-dl"), '%Y-%m-%d')
            ans_dl = datetime.strptime(form.get("a-dl"), '%Y-%m-%d')
            
            if(not (datetime.now() < ques_dl < ans_dl)):
                return jsonify({"message": "dates"})
            
            # validate dates here
            new_issue = Issue(
                name = form.get("name"),
                theme = form.get("theme"),
                q_dl = ques_dl,
                a_dl = ans_dl,
                userId = g.user.userId
            )    
            
            db.session.add(new_issue)

            users = db.query(User).all()
            for user in users:
                user.answered = False
            
            db.session.commit()
            message = "success"
        except Exception as e:
            print(e)
            message = "fail"
        
        return jsonify({
            "message": message
        })


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
        issue_info = get_latest_issue(Issue.q_dl)
        user = get_user(issue_info.userId)
        if issue_info is None or issue_info.q_dl < datetime.now():
            return render_template("ask.html", valid=False)
        return render_template("ask.html",
                               valid=True, name=issue_info.name, 
                               theme=issue_info.theme, issueId=issue_info.issueId,
                               username=user.name, date=issue_info.date.strftime("%Y-%m-%d"), 
                               q_dl=issue_info.q_dl.strftime("%Y-%m-%d")
                               )
    else:
        # do something  
        try: 
            jsonData = request.json  
            questions = jsonData["questions"]      
            issueId = jsonData["issueId"]
            userId = g.user.userId
            
            if db.session.query(Issue.q_dl).filter(Issue.issueId == issueId).scalar() < datetime.now():
                return jsonify({
                    "message": "deadline"
                })
            else:
                for q in questions:
                    if q.strip() == "":
                        continue
                    new_q = Question(
                        content = q.strip(),
                        issueId = issueId,
                        userId = userId
                    )
                    db.session.add(new_q)
            
                db.session.commit()
                message = "success"
        except Exception as e:
            print(e)
            message = "fail"
              
        return jsonify({
            "message": message
        })
    

@app.route("/reply", methods=["GET", "POST"])
@login_required
def reply():    
    if request.method == "GET":
        # get db for all questions in latest issue
        issue_info = get_latest_issue(Issue.a_dl)
        # if issue_info is not None and (issue_info.a_dl < datetime.now() or issue_info.q_dl > datetime.now()):
        #     return render_template("reply.html", valid=False)

        questions_db = get_questions(issue_info.issueId)
        questions = []
        for q in questions_db:
            questions.append({
                "quesId": q.quesId,
                "username": get_user(q.userId).name,
                "content": q.content
            })
        
        return render_template("reply.html", valid=True, questions=questions, issueId=issue_info.issueId,
                                a_dl=issue_info.a_dl.strftime("%Y-%m-%d"), date=issue_info.date.strftime("%Y-%m-%d"), username=get_user(issue_info.userId).name,
                                issueName=issue_info.name, theme=issue_info.theme
                                )
    else:
        try:
            for key, value in request.form.items():
                value = value.strip()
                if value == "":
                    continue
                quesId = int(key[2:])
                new_ans = Answer(
                    content = value,
                    userId = g.user.userId,
                    quesId = quesId
                )
                db.session.add(new_ans)
            db.session.commit()
            message = "success"
        
        except Exception as e:
            print(e)
            message = "fail"

        return jsonify({
            "message": message
        })


@app.route("/previous", methods=["GET"])
def previous():
    # get db
    return render_template("previous.html")


db.init_app(app)
with app.app_context():
    db.create_all()


app.run(debug=True)