import tkinter as tk
import random
from tkinter import messagebox

def check_guess():
    try:
        guess = int(entry.get())
        if guess == number:
            messagebox.showinfo("Correct!", f"🎉 You guessed it! The number was {number}.")
            reset_game()
        elif guess < number:
            messagebox.showinfo("Try Again", "Too low! Guess higher.")
        else:
            messagebox.showinfo("Try Again", "Too high! Guess lower.")
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid number.")

def reset_game():
    global number
    number = random.randint(1, 100)
    entry.delete(0, tk.END)

root = tk.Tk()
root.title("Number Guessing Game")
root.geometry("350x250")
root.resizable(False, False)

number = random.randint(1, 100)

tk.Label(root, text="Guess a number between 1 and 100", font=("Arial", 12)).pack(pady=10)

entry = tk.Entry(root, font=("Arial", 14))
entry.pack(pady=5)

tk.Button(root, text="Check", command=check_guess, width=10, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="New Game", command=reset_game, width=10, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Exit", command=root.quit, width=10, font=("Arial", 12)).pack(pady=5)

root.mainloop()
