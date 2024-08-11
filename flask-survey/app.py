from flask import Flask, request, render_template, redirect, session, flash
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config["SECRET_KEY"] = "secreter"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

ANSWERS = 'answers'

@app.route('/')
def go_start_page():
  """page to initiate survey"""
  return render_template("start_page.html", survey = survey)

@app.route('/begin', methods=["POST"])
def setup_question():
  """clear responses"""
  session[ANSWERS] = []
  return redirect("/questions/0")

@app.route('/questions/<int:qkey>')
def go_question(qkey):
  """display next question"""

  answers = session[ANSWERS]
  if answers is None:
    return redirect('/')
  if (len(answers) == len(survey.questions)):
    return redirect('survey_done')
  if (len(answers) != qkey):
    flash(f"Incorrect question key: {qkey}")
    return redirect(f"/question/{len(answers)}")
  
  question = survey.questions[qkey]
  return render_template("question.html",
                         query_key = qkey,
                         question = question)

@app.route('/answer', methods=["POST"])
def answer_query():
  """save answer and continue to next question"""
  choice = request.form['answer']
  
  answers = session[ANSWERS]
  answers.append(choice)

  session[ANSWERS] = answers

  if (len(answers) == len(survey.questions)):
    return redirect("/survey_done")
  else:
    return redirect(f"/questions/{len(answers)}")
  
@app.route('/survey_done')
def finished():
  """show finished survey page."""
  answers = session[ANSWERS]

  return render_template("finished.html", 
                         answers = answers,
                         survey = survey)