from flask import Flask, render_template, request, redirect, url_for, session
# Flask: main class to create web app
# render_template: converts HTML files to web pages
# request: access form data submitted by user
# redirect: send user to different page
# url_for: generate URLs for routes by name
# session: store data that persists across requests for each user

import secrets
from src.config import BullsAndCowsConfig
from src.bulls_and_cows_model import GameModel
from src.bulls_and_cows_solver import Solver
# secrets: Python library for generating secure random strings

app = Flask(__name__)
# Create a Flask application instance
# __name__ tells Flask where to find templates and static files

app.secret_key = secrets.token_hex(16)
# Generate a random 32-character hex string (16 bytes = 32 hex chars)
# This encrypts session cookies so users can't tamper with session data
# Without this, session won't work, and you'll get an error
# Example: "a1b2c3d4e5f6..." (random each time app starts)


config = BullsAndCowsConfig()

# Import your existing game classes
# We DON'T import the controller because we're replacing it!
# The Flask routes (functions below) ARE the new controller


def get_game_state():
    """Retrieve game state from session"""
    # Recreate the game objects from session data

    if not session.get('config'):
        return None

    config_data = session['config']
    # Get the config dictionary from session

    config = BullsAndCowsConfig(
        code_length=config_data['code_length'],
        colors=tuple(config_data['colors']),
        repeats_allowed=config_data['repeats_allowed'],
        human_opponent=config_data['human_opponent']
    )
    # Recreate the config object from saved data
    # TODO maybe to save config as dictionary in the session

    model = GameModel(config)
    # Create a new model instance

    # Restore the secret code (otherwise it would generate a new random one)
    # Only restore code if in bot mode (human mode has no code stored)
    if not config.human_opponent and session.get('code'):
        model.code = tuple(session['code'])

    solver = Solver(config, model)
    # Create solver with the model

    return config, model, solver
    # Return all three objects


@app.route('/')
# Decorator: tells Flask "when user visits /, run this function"
# @ is Python decorator syntax
# This is the ROOT URL: http://localhost:5000/
def home():
    """Home page - start a new game"""
    # This function handles GET requests to /

    return render_template('home.html',
                           code_length=config.code_length,
                           repeats_allowed=config.repeats_allowed,
                           human_opponent=config.human_opponent)
    # Find templates/home.html, convert to HTML, send to browser


@app.route('/new-game', methods=['POST'])
# This route only accepts POST requests (form submissions)
# GET = just viewing a page, POST = submitting data
def new_game():
    """Start a new game with selected configuration and store in session"""

    # Get configuration from form
    config.code_length = int(request.form.get('code_length', 4))
    # request.form is a dictionary of submitted form data
    # Get 'code_length' field, default to 4 if not found
    # Convert string to integer

    config.repeats_allowed = request.form.get('repeats_allowed') == 'on'
    # Checkboxes send 'on' when checked, None when unchecked
    # This converts to True/False

    config.human_opponent = True if request.form.get('opponent') == 'human' else False
    # A checkbox sends "on" only if checked, radio button always sends exactly one value from the group
    # This converts to True/False

    # Initialize game
    # Create model - this generates the secret code
    model = GameModel(config)
    # A solver is not created in "new_game" because it is only used in "play"

    # Store game state in session. Session is like a dictionary that persists between web requests
    # Save the secret code (tuple of colors)
    session['code'] = model.code if not config.human_opponent else None
    session['round_number'] = 0
    session['game_over'] = False
    # Save config as a dictionary (session can only store JSON-serializable data)
    session['config'] = {
        'code_length': config.code_length,
        'colors': config.colors,
        'repeats_allowed': config.repeats_allowed,
        'human_opponent': config.human_opponent
    }
    session['history'] = []
    # Empty list to store all guesses and results

    session['waiting_for_feedback'] = False
    session['current_guess'] = None

    return redirect(url_for('play'))
    # Redirect user to /play
    # url_for('play') generates the URL for the play() function
    # This is better than hardcoding '/play' because if you rename routes, it auto-updates


@app.route('/play')
def play():
    """Main game page"""

    game_state = get_game_state()
    # Recreate game objects from session

    # If no game exists, send user back to home page
    if not game_state:
        return redirect(url_for('home'))

    # Unpack the tuple returned by get_game_state()
    config, model, solver = game_state

    # Get history list from session, default to empty list if not found
    history = session.get('history', [])

    waiting_for_feedback = session.get('waiting_for_feedback', False)
    current_guess = session.get('current_guess', None)

    # Render template and pass variables to it.
    # In the HTML, you can access these as {{ config }}, {{ history }}, etc.
    return render_template('play.html',
                           config=config,
                           history=history,
                           round_number=session['round_number'],
                           game_over=session.get('game_over', False),
                           waiting_for_feedback=waiting_for_feedback,
                           current_guess=current_guess)


@app.route('/make-guess', methods=['POST'])
def make_guess():
    """Generate a new guess from the solver"""
    game_state = get_game_state()

    if not game_state or session.get('game_over'):
        return redirect(url_for('home'))
    # If no game or game is over, go home

    config, model, solver = game_state

    # Reconstruct solver state from history
    # Problem: Solver loses its state between requests
    # Solution: Replay all previous guesses to get solver back to current state
    history = session.get('history', [])
    for entry in history:
        solver.last_guess = tuple(entry['guess'])
        # Restore the guess

        solver.remove_incompatible_options(tuple(entry['feedback']))
        # Process the feedback to eliminate impossible codes

    # Get new guess from solver
    session['round_number'] += 1
    # Increment round counter

    guess = solver.get_guess()
    # Solver picks a random guess from remaining possibilities

    number_options = solver.get_number_options()
    # How many possibilities remain

    if config.human_opponent:
        # Human opponent mode: wait for user to provide feedback
        session['waiting_for_feedback'] = True
        session['current_guess'] = guess
        session['current_options'] = number_options
        # We RETURN here so we don't hit the 'bulls' check below
        return redirect(url_for('play'))

    else:
        # Bot opponent mode: evaluate automatically
        feedback = model.evaluate_guess(model.code, guess)
        bulls, cows = feedback

        # Add to history
        history.append({
            'round': session['round_number'],
            'guess': guess,
            'feedback': feedback,
            'bulls': bulls,
            'cows': cows,
            'options': number_options
        })
        session['history'] = history

        # Check win condition
        if bulls == config.code_length:
            session['game_over'] = True

        return redirect(url_for('play'))


@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    """Handle manual feedback from human user"""
    game_state = get_game_state()
    if not game_state:
        return redirect(url_for('home'))

    config, model, solver = game_state

    # 1. Get the manual feedback from the form
    try:
        bulls = int(request.form.get('bulls'))
        cows = int(request.form.get('cows'))
    except (ValueError, TypeError):
        # basic error handling if inputs are empty
        return redirect(url_for('play'))

    # 2. Retrieve the guess we are providing feedback for
    current_guess = session.get('current_guess')
    current_options = session.get('current_options')

    # 3. Update History
    history = session.get('history', [])
    history.append({
        'round': session['round_number'],
        'guess': current_guess,
        'feedback': (bulls, cows),
        'bulls': bulls,
        'cows': cows,
        'options': current_options
    })
    session['history'] = history

    # 4. Check Win Condition
    if bulls == config.code_length:
        session['game_over'] = True

    # 5. Clear the waiting state
    session['waiting_for_feedback'] = False
    session['current_guess'] = None

    return redirect(url_for('play'))


if __name__ == '__main__':
    # This runs only if you execute this file directly (python app.py)
    # Not if you import it

    app.run(debug=True)
    # Start the Flask web server
    # debug=True means:
    #   - Auto-reload when you change code
    #   - Show detailed error messages
    #   - DON'T use debug=True in production!
