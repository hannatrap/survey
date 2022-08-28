from flask import Flask, request, render_template, redirect, flash, session

from flask_debugtoolbar import DebugToolbarExtension

from surveys import satisfaction_survey as survey


RESPONSES = "responses"

app = Flask(__name__)
app.config['SECRET_KEY'] = "never-tell!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)



@app.route('/')
def home_page():
    """Shows home page"""
  
    return render_template('home.html', survey=survey)


@app.route('/start', methods=["POST"])
def start_survey():
    session[RESPONSES] = []
        
    return redirect("/questions/0")


@app.route("/answer", methods=["POST"])
def handle_question():
    choice = request.form['answer']

    response = session[RESPONSES]
    response.append(choice)
    session[RESPONSES] = response

    if (len(response) == len(survey.questions)):
        return redirect("/done")

    else:
        return redirect(f"/questions/{len(response)}")





@app.route('/questions/<int:qid>')
def question_page(qid):
    """handles and displays questions"""
    response = session.get(RESPONSES)

    if (response is None):
        return redirect('/')

    if (len(response) == len(survey.questions)):
        return redirect("/done")

    if (len(response) != qid):

        flash(f"Invalid question id: {qid}.")
        return redirect(f"/questions/{len(response)}")

    question = survey.questions[qid]
    return render_template('questions.html', question_num=qid, question=question)


@app.route("/done")
def done():
    return render_template("done.html")