from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "lol"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses = []
survey = surveys.get("satisfaction")


@app.route('/')
def root():
    """ The root page. """
    return render_template('start_page.html', survey=survey)

@app.route('/begin', methods=["POST"])
def begin_survey():
    """Begin the survey."""
    return redirect('/questions/0')


@app.route('/questions/<int:number>')
def show_questions(number):
    """ Begin asking the questions. """
    
    question = survey.questions[number]

    # Do not skip the start page 
    if (responses is None):
        return redirect("/")

    # User completed all questions, thank them. 
    if (len(responses) == len(survey.questions)):
        return redirect("/complete")

    # No skipping questions. 
    if (len(responses) != number):
        flash(f'Invalid Question Number: {number}.')
        return redirect(f'/questions/{len(responses)}')

    return render_template('questions.html', question_num=number, question=question)


@app.route('/answer', methods=["POST"])
def process_question():
    """Show the answer user has selected."""

    # Get the user answer choice for question. 
    choice = request.form['answer']
    responses.append(choice)

    # If they reached the end of the survey, else keep funneling questions. 
    if (len(responses) == len(survey.questions)):
        return redirect('confirmation')
    else:   
        return redirect(f'/questions/{len(responses)}')

@app.route('/confirmation')
def show_confirmation():
    """Confirmation Page for Survey Completion. """

    return render_template('confirmation.html')




