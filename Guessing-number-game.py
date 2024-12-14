import random
import sqlite3
import time

def init_db():
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            guesses INTEGER NOT NULL,
            time_taken REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def save_result(name, guesses, time_taken):
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO results (name, guesses, time_taken) VALUES (?, ?, ?)', 
                   (name, guesses, time_taken))
    conn.commit()
    conn.close()

def get_best_score():
    conn = sqlite3.connect('game_results.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name, guesses, time_taken FROM results ORDER BY guesses + (time_taken * 10) LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result

# Game logic
def generate_number():
    digits = random.sample(range(10), 4)
    return ''.join(map(str, digits))

def evaluate_guess(secret, guess):
    plus = sum(1 for s, g in zip(secret, guess) if s == g)
    minus = sum(1 for g in guess if g in secret) - plus
    return '+' * plus + '-' * minus

def start_game():
    print("Welcome to the Guessing Number Game!")
    name = input("Enter your name: ")

    secret_number = generate_number()
    print("A 4-digit number has been generated. Start guessing!")
    
    guesses = 0
    start_time = time.time()

    while True:
        guess = input("Enter your guess (4 unique digits): ")
        if len(guess) != 4 or not guess.isdigit() or len(set(guess)) != 4:
            print("Invalid input. Make sure to enter 4 unique digits.")
            continue

        guesses += 1
        result = evaluate_guess(secret_number, guess)
        print(f"Result: {result}")

        if result == '++++':
            end_time = time.time()
            time_taken = round(end_time - start_time, 2)
            print(f"Congratulations, {name}! You guessed the number {secret_number} in {guesses} moves and {time_taken} seconds.")
            save_result(name, guesses, time_taken)
            break

def display_leaderboard():
    best = get_best_score()
    if best:
        name, guesses, time_taken = best
        print(f"Best Score: {name} - {guesses} guesses and {time_taken} seconds.")
    else:
        print("No scores recorded yet.")


def main():
    init_db()
    while True:
        print("\nMain Menu:")
        print("1. Start New Game")
        print("2. View Best Score")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            start_game()
        elif choice == '2':
            display_leaderboard()
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    

