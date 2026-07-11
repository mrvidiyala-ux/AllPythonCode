from tkinter import *
import random

# ---------------- GLOBAL VARIABLES ----------------
a = None
mode = "NORMAL"

player_score = 0
computer_score = 0
target = 0

# ---------------- RULE LOGIC ----------------
def is_out(bat, bowl):
    if mode == "NORMAL":
        return bat == bowl
    if mode == "CRAZY":
        return abs(bat - bowl) == 1
    if mode == "MAD":
        return bat + bowl == 11

def get_runs(bat, bowl):
    if bat == bowl:
        return bat * bat
    return bat

# ---------------- HOME FUNCTION ----------------
def go_home(win):
    win.destroy()
    s1()

# ---------------- START SCREEN ----------------
def s1():
    global s1_window
    s1_window = Tk()
    s1_window.title("HAND CRICKET 🏏")
    s1_window.geometry("500x400")
    s1_window.resizable(False, False)
    s1_window.config(bg="#222")

    Label(s1_window, text="HAND CRICKET GAME 🏏",
          font=("Algerian", 20), fg="white", bg="black").pack(pady=60)

    Button(s1_window, text="▶ PLAY", font=("Arial", 30),
           bg="red", fg="white", command=play).pack()

    s1_window.mainloop()

# ---------------- PLAY MENU ----------------
def play():
    s1_window.destroy()
    s2 = Tk()
    s2.title("Hand Cricket")
    s2.geometry("515x400")
    s2.resizable(False, False)
    s2.config(bg="#1eff00")

    Label(s2, text="Welcome to Hand Cricket 🏏",
          font=("Calibri", 20), fg="white", bg="black").pack(pady=20)

    Button(s2, text="PLAY", font=("Agency", 20),
           bg="blue", fg="white", width=12,
           command=lambda: [s2.destroy(), odd_even()]).pack(pady=10)

    Button(s2, text="RULES", font=("Agency", 20),
           bg="red", fg="white", width=12,
           command=lambda: rules_screen(s2)).pack(pady=10)

    s2.mainloop()

# ---------------- RULES SCREEN ----------------
def rules_screen(prev):
    prev.destroy()
    r = Tk()
    r.title("Game Rules")
    r.geometry("520x550")
    r.config(bg="#111")

    rules_text = """
NORMAL MODE:
• Same numbers → OUT
• Different numbers → batter scores his number
• When batter keeps 0, he gets the bowler score

CRAZY MODE:
• Adjacent numbers (4 & 5) → OUT
• Same numbers → Square runs (5×5 = 25)
• Else → Normal runs
• When batter keeps 0, he gets the bowler score

MAD MODE:
• Sum of numbers = 11 → OUT
• Same numbers → Square runs
• Else → Normal runs
• When batter keeps 0, he gets the bowler score

COMMON RULES:
• Numbers allowed: 1 to 10
• After batting → Target = Score + 1
• Chasing team must reach target
• When batter keeps 0, he gets the bowler score

HAVE FUN PLAYING! 🏏

"""

    Label(r, text="RULES 📜",
          font=("Calibri", 22, "bold"),
          fg="white", bg="#111").pack(pady=10)

    Label(r, text=rules_text,
          font=("Calibri", 14),
          fg="white", bg="#111", justify=LEFT).pack(padx=20)

    Button(r, text="BACK", font=("Arial", 14),
           command=lambda: [r.destroy(), play()]).pack(pady=20)

    r.mainloop()

# ---------------- ODD / EVEN ----------------
def odd_even():
    s3 = Tk()
    s3.title("Odd or Eve")
    s3.geometry("515x400")
    s3.config(bg="#1eff00")

    Label(s3, text="Choose ODD or EVE",
          font=("Calibri", 20), fg="white", bg="black").pack(pady=30)

    Button(s3, text="ODD", font=("Agency", 20),
           bg="red", fg="white", width=10,
           command=lambda: number_choice("odd", s3)).pack(pady=20)

    Button(s3, text="EVE", font=("Agency", 20),
           bg="blue", fg="white", width=10,
           command=lambda: number_choice("even", s3)).pack()

    s3.mainloop()

# ---------------- NUMBER PICK ----------------
def number_choice(choice, prev):
    global a
    prev.destroy()

    s4 = Tk()
    s4.title("Choose Number")
    s4.geometry("515x600")
    s4.config(bg="#ff8000")

    Label(s4, text="Choose a number (1–10)",
          font=("Calibri", 18), fg="white", bg="black").pack(pady=10)

    def result(num):
        global a
        s4.destroy()

        comp = random.randint(1, 10)
        total = num + comp

        if (total % 2 == 1 and choice == "odd") or (total % 2 == 0 and choice == "even"):
            a = "you"
            msg = "YOU WON THE TOSS 🎉"
        else:
            a = "bot"
            msg = "COMPUTER WON THE TOSS 🤖"

        s5 = Tk()
        s5.title("Toss Result")
        s5.geometry("515x400")
        s5.config(bg="#00ffff")

        Label(s5,
              text=f"You: {num}\nComputer: {comp}\nTotal: {total}\n\n{msg}",
              font=("Calibri", 18), bg="#00ffff").pack(pady=40)

        Button(s5, text="CONTINUE",
               font=("Arial", 14),
               command=lambda: [s5.destroy(), bat_or_ball()]).pack()

        s5.mainloop()

    for i in range(1, 11):
        Button(s4, text=str(i), font=("Arial", 16),
               width=3, command=lambda x=i: result(x)).pack(pady=2)

    s4.mainloop()

# ---------------- BAT OR BALL ----------------
def bat_or_ball():
    s6 = Tk()
    s6.title("Bat or Ball")
    s6.geometry("515x400")
    s6.config(bg="#ffcc00")

    if a == "you":
        Label(s6, text="You won the toss!\nChoose BAT or BALL",
              font=("Calibri", 20), fg="white", bg="black").pack(pady=40)

        Button(s6, text="BAT", font=("Agency", 20),
               bg="red", fg="white", width=10,
               command=lambda: mode_select("bat", s6)).pack(pady=10)

        Button(s6, text="BALL", font=("Agency", 20),
               bg="blue", fg="white", width=10,
               command=lambda: mode_select("bowl", s6)).pack()
    else:
        choice = random.choice(["bat", "bowl"])
        Label(s6, text=f"Computer won toss!\nComputer chose to {choice.upper()}",
              font=("Calibri", 20), fg="white", bg="black").pack(pady=60)
        s6.after(2000, lambda: mode_select(choice, s6))

    s6.mainloop()

# ---------------- MODE SELECTION ----------------
def mode_select(play_type, prev):
    prev.destroy()
    s7 = Tk()
    s7.title("Select Mode")
    s7.geometry("515x400")
    s7.config(bg="#ffcc00")

    Label(s7, text="Select Mode",
          font=("Calibri", 20), fg="white", bg="black").pack(pady=30)

    for m, c in [("NORMAL", "red"), ("CRAZY", "blue"), ("MAD", "green")]:
        Button(s7, text=m, font=("Agency", 20),
               bg=c, fg="white", width=15,
               command=lambda x=m: start_game(play_type, x, s7)).pack(pady=8)

    s7.mainloop()

# ---------------- START GAME ----------------
def start_game(play_type, selected_mode, prev):
    global mode, player_score, computer_score, target
    mode = selected_mode
    player_score = 0
    computer_score = 0
    target = 0
    prev.destroy()

    batting_game() if play_type == "bat" else bowling_game()

# ---------------- BATTING ----------------
def batting_game():
    global player_score, target
    w = Tk()
    w.title(f"Batting - {mode}")
    w.geometry("515x650")
    w.config(bg="#ffcc00")

    Label(w, text="YOU ARE BATTING 🏏",
          font=("Calibri", 18), bg="black", fg="white").pack()

    score_lbl = Label(w, text="Score: 0",
                      font=("Calibri", 16), bg="#ffcc00")
    score_lbl.pack()

    result_lbl = Label(w, font=("Calibri", 16), bg="#ffcc00")
    result_lbl.pack()

    Button(w, text="HOME", font=("Arial", 12),
           command=lambda: go_home(w)).pack(pady=5)

    def play(n):
        global player_score, target
        comp = random.randint(1, 10)

        if is_out(n, comp):
            target = player_score + 1
            result_lbl.config(text=f"You: {n} | Computer: {comp}\nOUT ❌\nTarget: {target}")
            w.after(1500, lambda: [w.destroy(), bowling_game()])
        else:
            runs = get_runs(n, comp)
            player_score += runs
            score_lbl.config(text=f"Score: {player_score}")
            result_lbl.config(text=f"You: {n} | Computer: {comp}\nRuns: {runs}")

    for i in range(1, 11):
        Button(w, text=str(i), font=("Arial", 16),
               width=3, command=lambda x=i: play(x)).pack(pady=2)

    w.mainloop()

# ---------------- BOWLING ----------------
def bowling_game():
    global computer_score
    w = Tk()
    w.title(f"Bowling - {mode}")
    w.geometry("515x650")
    w.config(bg="#00ffff")

    Label(w, text="YOU ARE BOWLING 🎯",
          font=("Calibri", 18), bg="black", fg="white").pack()

    score_lbl = Label(w, text="Computer: 0",
                      font=("Calibri", 16), bg="#00ffff")
    score_lbl.pack()

    target_lbl = Label(w, text=f"Target: {target}",
                       font=("Calibri", 16), bg="#00ffff")
    target_lbl.pack()

    result_lbl = Label(w, font=("Calibri", 16), bg="#00ffff")
    result_lbl.pack()

    Button(w, text="HOME", font=("Arial", 12),
           command=lambda: go_home(w)).pack(pady=5)

    def play(n):
        global computer_score
        comp = random.randint(1, 10)

        if is_out(n, comp):
            result_lbl.config(text="COMPUTER OUT!\nYOU WIN 🎉")
            return

        runs = get_runs(comp, n)
        computer_score += runs
        score_lbl.config(text=f"Computer: {computer_score}")

        if computer_score >= target:
            result_lbl.config(text="COMPUTER WON 😢")
        else:
            result_lbl.config(text=f"You: {n} | Computer: {comp}\nRuns: {runs}")

    for i in range(1, 11):
        Button(w, text=str(i), font=("Arial", 16),
               width=3, command=lambda x=i: play(x)).pack(pady=2)

    w.mainloop()

# ---------------- RUN ----------------
s1()