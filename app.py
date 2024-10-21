from flask import Flask, render_template, request, redirect, url_for
import random
import requests

app = Flask(__name__)

words = ['python', 'flask', 'web', 'programming']

hidden_word = ''
guessed_letters = []
attempts = 0
remaining_hints = 3
@app.route('/')
def home():
    return redirect(url_for('hangman_game'))

@app.route('/hangman_game')
def hangman_game():
    global hidden_word, guessed_letters, attempts, remaining_hints
    words.extend(get_random_words(5,3))
    hidden_word = random.choice(words)
    print(f"word: {hidden_word}")
    guessed_letters = []
    attempts = 0
    remaining_hints = 3
    return render_template('hangman.html', word=get_display_word(), remaining_attempts=attempts)

# request for hints
@app.route('/hint', methods=['POST'])
def hint():
    global hidden_word, guessed_letters, remaining_hints

    if remaining_hints > 0:
        available_hint_letters = []

        for letter in hidden_word:
            if letter not in guessed_letters:
                available_hint_letters.append(letter)

        hint_letter = random.choice(available_hint_letters)
        remaining_hints -= 1

        response = {
            'success': True,
            'hint_letter': hint_letter,  # Devolver la letra de la pista
            'remaining_hints': remaining_hints
        }

        return response
    else:
        return {'success': False}


# TODO TASK 1
#  Implement logic that correctly processes the hidden_word and guessed_letters and
#  returns a string with letters revealed or hidden based on user guesses.
def get_display_word():
    global hidden_word, guessed_letters
    display_word = []
    for letter in hidden_word:
        if letter in guessed_letters:
            display_word.append(letter)
        else:
            display_word.append('_')
    return ' '.join(display_word)

# TODO TASK 2
#  Ensure that guesses are only added if they haven’t already been guessed.
def check_correct_guess(input_letter):
    global hidden_word
    input_letter = input_letter.lower()

    if input_letter in guessed_letters:
        return False

    guessed_letters.append(input_letter)
    if input_letter in hidden_word:

        return True
    else:
        return False


# TODO TASK 3
#  Implement the logic that tracks the number of attempts and determines if
#  the player has lost (attempts ≥ 6).
def check_lose():
    global attempts
    return attempts >= 6

# TODO TASK 4
#  Ensure that the function correctly checks if all letters in hidden_word are
#  in the guessed_letters.
def check_win():
    global hidden_word, guessed_letters
    for letter in hidden_word:
        if letter not in guessed_letters:
            return False
    return True


# get random words from the Random Word API https://random-word-api.herokuapp.com/home
def get_random_words(count_of_words, length):
    response = requests.get(f'https://random-word-api.herokuapp.com/word?number={count_of_words}&length={length}')
    if response.status_code == 200:
        return response.json()
    else:
        return []

@app.route('/guess', methods=['POST'])
def guess():
    global hidden_word, attempts

    guessed_letter = request.form['letter']

    if not check_correct_guess(guessed_letter):
        attempts += 1

    if check_lose():
        return render_template('lose.html', word=hidden_word)

    if check_win():
        return render_template('win.html', word=hidden_word)

    return render_template('hangman.html', word=get_display_word(), remaining_attempts=attempts)



if __name__ == '__main__':
    app.run(debug=True)
