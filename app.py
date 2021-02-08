from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "its_a_secret!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

responses_key = "responses"
survey = surveys.get("satisfaction")


@app.route('/')
def root():
    """ The root page. """
    return render_template('start_page.html', survey=survey)

@app.route('/begin', methods=["POST"])
def begin_survey():
    """Begin the survey."""
    
    # Begin the session to store user answers. 
    session[responses_key] = []
    return redirect('/questions/0')


@app.route('/questions/<int:number>')
def show_questions(number):
    """ Begin asking the questions. """
    
    # What is the question # in the survey. 
    question = survey.questions[number]
    
    # Get the session that has the user's answers. 
    responses = session.get(responses_key)

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
    
    # Add the answer to the responses and rebind the session. 
    responses = session[responses_key]
    responses.append(choice)
    session[responses_key] = responses 

    # If they reached the end of the survey, else keep funneling questions. 
    if (len(responses) == len(survey.questions)):
        return redirect('confirmation')
    else:   
        return redirect(f'/questions/{len(responses)}')

@app.route('/confirmation')
def show_confirmation():
    """Confirmation Page for Survey Completion. """

    return render_template('confirmation.html')




