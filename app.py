from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.before_request
def before_request():
    if 'user_total_score' not in session:
        session['user_total_score'] = 0
    if 'comp_total_score' not in session:
        session['comp_total_score'] = 0
    if 'ties_total' not in session:
        session['ties_total'] = 0

@app.route('/')
def index():
    if 'game_over' in session:
        return redirect(url_for('final_result'))
    else:
        return render_template('index.html')
    
    

@app.route('/play', methods=['POST'])
def play():
    user_choice = request.form.get('choice')
    choices = ['Rock', 'Paper', 'Scissor']
    comp_choice = random.choice(choices)

    result = ""

    if user_choice:
        if ((user_choice == 'Paper' and comp_choice == 'Rock') or
                (user_choice == 'Rock' and comp_choice == 'Scissor') or
                (user_choice == 'Scissor' and comp_choice == 'Paper')):
            result = "User Wins"
            session['user_total_score'] += 1
        elif ((user_choice == 'Paper' and comp_choice == 'Scissor') or
                (user_choice == 'Rock' and comp_choice == 'Paper') or
                (user_choice == 'Scissor' and comp_choice == 'Rock')):
            result = "Computer Wins"
            session['comp_total_score'] += 1
        else:
            result = "It's a Tie"
            session['ties_total'] += 1

    if request.form.get('quit'):
        session['game_over'] = True
        return redirect(url_for('final_result'))

    return render_template('result.html', user_choice=user_choice, comp_choice=comp_choice, result=result)

@app.route('/reset')
def reset():
    session.pop('game_over', None)  
    session['user_total_score'] = 0  
    session['comp_total_score'] = 0 
    session['ties_total'] = 0  
    return redirect(url_for('index'))

@app.route('/final_result')
def final_result():
    user_score = session.get('user_total_score', 0)
    comp_score = session.get('comp_total_score', 0)
    ties = session.get('ties_total', 0)
    session.pop('game_over', None)
    return render_template('final_result.html', user_score=user_score, comp_score=comp_score, ties=ties)

if __name__ == '__main__':
    app.run(debug=True)
