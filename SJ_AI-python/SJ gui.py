from tkinter import *
from tkinter import filedialog
from gpt4all import GPT4All
import threading, time, json, os
from reportlab.pdfgen import canvas as pdf_canvas

# ---------------- MODEL SEARCH ----------------
CONFIG_FILE = "model_path.json"

def find_model():
    if os.path.exists(CONFIG_FILE):
        data = json.load(open(CONFIG_FILE))
        if os.path.exists(data["path"]):
            return data["path"]

    path = filedialog.askopenfilename(
        title="Select GPT4All model (.gguf)",
        filetypes=[("GGUF Model", "*.gguf")]
    )

    if not path:
        raise Exception("Model not selected!")

    json.dump({"path": path}, open(CONFIG_FILE, "w"))
    return path

MODEL_PATH = find_model()

model = GPT4All(
    model_name=os.path.basename(MODEL_PATH),
    model_path=os.path.dirname(MODEL_PATH),
    device="cpu"
)

# ---------------- THEMES ----------------
themes = {
    "dark": {"bg":"#1e1e1e","user":"#4caf50","ai":"#333333","text":"white"},
    "light":{"bg":"#f5f5f5","user":"#4caf50","ai":"#dddddd","text":"black"}
}
current_theme="dark"

CHAT_FILE="chat.json"

# ---------------- SAVE CHAT ----------------
def save_chat(role,text):
    data=[]
    if os.path.exists(CHAT_FILE):
        data=json.load(open(CHAT_FILE))
    data.append({"role":role,"text":text,"time":time.strftime("%H:%M")})
    json.dump(data,open(CHAT_FILE,"w"))

# ---------------- EXPORT PDF ----------------
def export_pdf():
    if not os.path.exists(CHAT_FILE): return
    data=json.load(open(CHAT_FILE))
    c=pdf_canvas.Canvas("chat_export.pdf")
    y=800
    for msg in data:
        line=f'{msg["time"]} {msg["role"].upper()}: {msg["text"]}'
        c.drawString(40,y,line)
        y-=20
        if y<40:
            c.showPage()
            y=800
    c.save()

# ---------------- SPLASH SCREEN ----------------
def show_splash():
    splash=Toplevel()
    splash.overrideredirect(True)
    splash.geometry("400x200+400+250")
    Label(splash,text="🚀 SJ Meta AI",font=("Arial",24,"bold")).pack(expand=True)
    splash.after(2000,splash.destroy)

# ---------------- MESSAGE CARD ----------------
def add_message(text,sender):   
    theme=themes[current_theme]

    container=Frame(chat_frame,bg=theme["bg"],pady=6)

    avatar="🙂" if sender=="user" else "🤖"
    name="You" if sender=="user" else "AI"
    timestamp=time.strftime("%H:%M")

    card=Frame(container,
               bg=theme["user"] if sender=="user" else theme["ai"],
               padx=10,pady=8,
               bd=0)

    header_frame=Frame(card,bg=card["bg"])
    header_frame.pack(fill=X)

    header=Label(header_frame,
        text=f"{avatar} {name}   {timestamp}",
        font=("Arial",10,"bold"),
        bg=card["bg"],
        fg="white" if current_theme=="dark" else "black")
    header.pack(side=LEFT)

    def copy_text():
        root.clipboard_clear()
        root.clipboard_append(text)

    Button(header_frame,text="📋",
        command=copy_text,
        bg=card["bg"],bd=0).pack(side=RIGHT)

    body=Label(card,
        text=text,
        font=("Arial",12),
        bg=card["bg"],
        fg="white" if current_theme=="dark" else "black",
        wraplength=340,
        justify=LEFT,
        anchor="w")
    body.pack(fill=X,pady=(4,0))

    card.pack(fill=X,padx=15)
    container.pack(fill=X)

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

    # Animated emoji reaction
    if sender=="ai":
        animate_emoji(container)

    return body

# ---------------- ANIMATED EMOJI ----------------
def animate_emoji(frame):
    emoji=Label(frame,text="🤖",font=("Arial",20))
    emoji.place(x=360,y=0)
    dy=-2
    def move():
        nonlocal dy
        y=emoji.winfo_y()+dy
        if y<0: dy=2
        if y>20: dy=-2
        emoji.place(y=y)
        frame.after(100,move)
    move()

# ---------------- TYPING EFFECT ----------------
def typing(label,text,i=0):
    if i==0:
        label.config(text="")
    if i<len(text):
        label.config(text=text[:i+1])
        root.after(8,typing,label,text,i+1)

# ---------------- AI ----------------
def ask_ai(event=None):
    user=user_input.get().strip()
    if not user: return
    user_input.delete(0,END)

    add_message(user,"user")
    save_chat("user",user)

    thinking=add_message("🤖 thinking...","ai")

    threading.Thread(
        target=generate,
        args=(user,thinking),
        daemon=True
    ).start()

def generate(prompt,label):
    try:
        with model.chat_session():
            response=model.generate(prompt,max_tokens=200,temp=0.7)

        save_chat("ai",response)
        root.after(0,lambda:typing(label,response))

    except Exception as e:
        root.after(0,lambda:label.config(text=f"Error: {e}"))

# ---------------- THEME TOGGLE ----------------
def toggle_theme():
    global current_theme
    current_theme="light" if current_theme=="dark" else "dark"
    theme=themes[current_theme]

    root.configure(bg=theme["bg"])
    canvas.configure(bg=theme["bg"])
    chat_frame.configure(bg=theme["bg"])
    title.config(bg=theme["bg"],fg=theme["text"])

# ---------------- WINDOW ----------------
root=Tk()
root.title("SJ Meta AI 🤖")
root.geometry("420x700")

show_splash()  # splash screen at start

title=Label(root,text="SJ Meta AI 🤖",font=("Arial",18,"bold"))
title.pack(pady=5)

Button(root,text="Toggle Theme",command=toggle_theme).pack()
Button(root,text="Export PDF",command=export_pdf).pack(pady=3)

canvas=Canvas(root,highlightthickness=0)
scroll=Scrollbar(root,command=canvas.yview)
chat_frame=Frame(canvas)

canvas.configure(yscrollcommand=scroll.set)
scroll.pack(side=RIGHT,fill=Y)
canvas.pack(fill=BOTH,expand=True)
canvas.create_window((0,0),window=chat_frame,anchor="nw")

chat_frame.bind("<Configure>",
lambda e:canvas.configure(scrollregion=canvas.bbox("all")))

user_input=Entry(root,font=("Arial",14))
user_input.pack(fill=X,padx=10,pady=10)
user_input.bind("<Return>",ask_ai)

Button(root,text="Send 🚀",
font=("Arial",14,"bold"),
bg="#4caf50",fg="white",
command=ask_ai).pack(pady=5)

toggle_theme()
root.mainloop()
