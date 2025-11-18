import os
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session
import time

app = Flask(__name__)

# In order to use "sessions",you need a "secret key".
# This is something random you generate.  
# For more info see: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY

app.secret_key=os.environ["SECRET_KEY"]; #This is an environment variable.  
                                     #The value should be set on the server. 
                                     #To run locally, set in env.bat (env.sh on Macs) and include that file in gitignore so the secret key is not made public.

start = None
end = None

@app.route('/')
def renderMain():
    return render_template('home.html')

@app.route('/startOver')
def startOver():
    session.clear() #clears variable values and creates a new session
    return redirect(url_for('renderMain')) # url_for('renderMain') could be replaced with '/'

@app.route('/page1')
def renderPage1():
    global start
    start = time.time()
    if "year2000" not in session:
        return render_template('page1.html')
    else:
        return redirect(url_for('renderPage2'))

@app.route('/page2',methods=['GET','POST'])
def renderPage2():
    if "gravity" not in session:
        if "year2000" not in session:
            session["year2000"]=request.form['year2000']
        return render_template('page2.html')
    else:
        return redirect(url_for('renderPage3'))

@app.route('/page3',methods=['GET','POST'])
def renderPage3():
    if "joker" not in session:
        if "gravity" not in session:
            session["gravity"]=request.form['gravity']
        return render_template('page3.html')
    else:
        return redirect(url_for('renderPage4'))

@app.route('/page4',methods=['GET','POST'])
def renderPage4():
    if "elements" not in session:
        if "joker" not in session:
            session["joker"]=request.form['joker']
        return render_template('page4.html')
    else:
        return redirect(url_for('renderPage5'))

@app.route('/page5',methods=['GET','POST'])
def renderPage5():
    if "australia" not in session:
        if "elements" not in session:
            session["elements"]=request.form['elements']
        return render_template('page5.html')
    else:
        return redirect(url_for('page6.html'))
        
@app.route('/page6',methods=['GET','POST'])
def renderPage6():
    if "swallow" not in session:
        if "australia" not in session:
            session["australia"]=request.form['australia']
        return render_template('page6.html')
    else:
        return redirect(url_for('renderScore'))

@app.route('/score',methods=['GET','POST'])
def renderScore():
    global end
    end = time.time()
    if "swallow" not in session:
        session["swallow"]=request.form['swallow']
    qs1 = get_question_status()[0]
    qs2 = get_question_status()[1]
    qs3 = get_question_status()[2]
    qs4 = get_question_status()[3]
    qs5 = get_question_status()[4]
    qs6 = get_question_status()[5]
    print(end-start)
    tm = end-start
    t = round(tm, 2)
    return render_template('score.html', questionStatus1 = qs1, questionStatus2 = qs2, questionStatus3 = qs3, questionStatus4 = qs4, questionStatus5 = qs5, questionStatus6 = qs6, score = get_score(), time = str(t))

def get_question_status():
    questionStatus = []
    correctAnswers = ["366", "-9.8", "zach galifianakis", "118", "john howard", "20.1"]
    questions = ["year2000", "gravity", "joker", "elements", "australia", "swallow"]
    x = 0
    for ans in correctAnswers:
        qs = ""
        if session[questions[x]].lower() == ans:
            qs = "Correct"
        else:
            qs = "Incorrect"
        questionStatus.append(qs)
        x = x + 1
    return questionStatus

def get_score():
    questionStatuses = get_question_status()
    numCorrect = 0
    numTotal = 0
    for qs in questionStatuses:
        if qs == "Correct":
            numCorrect = numCorrect + 1
            numTotal = numTotal + 1
        else:
            numTotal = numTotal + 1
    score = numCorrect / numTotal
    score = score * 100
    return score
    

if __name__=="__main__":
    app.run(debug=False)
