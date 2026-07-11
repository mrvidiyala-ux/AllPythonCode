########  ######## ########                 ########    #####
                                   ##    ##  ##    ## ##    ##                       ##       ##
                                   ########  ## ##### ## #####      ###        ########       ##
                                   ##    ##  ##       ##                       ##             ##
                                   ##    ##  ##       ##                       ########    ########
                            # ----------------------------------------------------------------------#

                  ###################################################################################################          
                  ##                                    GOAL   FOR    APP-21                                       ##    
                  ##  ->  To create an account personalized to the user(student) and tries to support the child    ##           
                  ##                                                                                               ##
                  ###################################################################################################


# libraries
from tkinter import *
from tkinter import messagebox
users = {}

#Application GUI
root = Tk()
root.geometry("800x500")
root.title("StudySpark ⚡")


#Frame 2 GUI
def go_to_auth():
    screen1_frame.pack_forget()
    #2nd frame
    screen2_frame.pack(fill="both", expand=True)
    

    
def open_login():
    screen2_frame.pack_forget()
    screen4_frame.pack(fill="both", expand=True)   
    screen4_center_frame.pack(fill="both", expand=True)
    
def open_register():
    screen2_frame.pack_forget()
    screen3_frame.pack(fill="both", expand=True)
    screen3_center_frame.pack(fill="both", expand=True)



screen4_frame = Frame(root, bg="black")
screen4_center_frame= Frame(root, bg="black")


title = Label(screen4_center_frame, text="Log-In",font=("Arial",24,"bold"),fg="white",bg="black")
title.pack(pady=10)
usernamel = Label(screen4_center_frame,text="Enter your Username",font=("Arial",15),fg="white",bg='black')
usernamel.pack(pady=20)
username = Entry(screen4_center_frame,font=("Arial",15),fg="black",bg="white",width=30)
username.pack()
passwordl = Label(screen4_center_frame,text="Enter your Password",font=("Arial",15),fg="white",bg="black")
passwordl.pack(pady=20)
password = Entry(screen4_center_frame,font=("Arial",15),fg="black",bg="white",width=30)
password.pack()
top1_frame = Frame(screen4_frame, bg="black")
top1_frame.pack(fill="x")
def go_back_to_auth1():
    screen4_frame.pack_forget()
    screen4_center_frame.pack_forget()
    screen2_frame.pack(fill="both", expand=True)
back1 = Button(top1_frame, text="← Back", command=go_back_to_auth1)
back1.pack(anchor="w", padx=10, pady=10)
def do_login():
    user = username.get().strip()
    pwd = password.get().strip()

    if user not in users:
        messagebox.showerror("Error", "User not registered")
        return

    if users[user]["password"] != pwd:
        messagebox.showerror("Error", "Wrong password")
        return

    messagebox.showinfo("Success",f"Welcome {users[user]['name']} ({users[user]['role']})")
login = Button(screen4_center_frame,text="Login",font=("Arial",20),fg="black",bg="red",command=do_login)
login.pack(pady=30)



#1Frame1GUI


screen1_frame = Frame(root, bg="black")
screen1_frame.pack(fill="both", expand=True)
#2Framegui
screen2_frame = Frame(root, bg="black")
#3Framegui
screen3_frame = Frame(root, bg="black")

#screen 3 center gui

screen3_center_frame = Frame(screen3_frame, bg="black")
screen3_center_frame.pack(expand=True)

title = Label(screen3_center_frame,text="Register a User",font=("Arial",30,"bold"),fg="white",bg="black")
title.pack(pady=5)
nameh = Label(screen3_center_frame,text="Name:",font=("Calibri",13),fg="white",bg="black")
nameh.pack(pady=10)
namei = Entry(screen3_center_frame,font=("Arial",12),width=40,fg="black",bg="white")
namei.pack(pady=20)
emailh = Label(screen3_center_frame,text="Email:",font=("Calibri",13),fg="white",bg="black")
emailh.pack(pady=10)
emaili = Entry(screen3_center_frame,font=("Arial",12),width=40,fg="black",bg="white")
emaili.pack(pady=20)
passwordh = Label(screen3_center_frame,text="User Password:",font=("Calibri",13),fg="white",bg="black")
passwordh.pack(pady=10)
passwordi = Entry(screen3_center_frame,show="*",font=("Arial",12),width=40,fg="black",bg="white")
passwordi.pack(pady=20)
genderh = Label(screen3_center_frame,text="Gender (M/F/prefer not to say):",font=("Calibri",13),fg="white",bg="black")
genderh.pack(pady=10)
genderi = Entry(screen3_center_frame,font=("Arial",12),width=40,fg="black",bg="white")
genderi.pack(pady=20)
roleh = Label(screen3_center_frame,text="Role (Student/Teacher/Parent/Other):",font=("Calibri",13),fg="white",bg="black")
roleh.pack(pady=10)
rolei = Entry(screen3_center_frame,font=("Arial",12),width=40,fg="black",bg="white")
rolei.pack(pady=20)
def create_account():
    name = namei.get().strip()
    email = emaili.get().strip()
    password = passwordi.get().strip()
    gender = genderi.get().strip()
    role = rolei.get().strip()

    if name == "" or email =="" or password ==  "" or gender =="" or role == "":
        messagebox.showerror("Error", "Fill all fields")
    elif "@" not in email or "." not in email and email.count("@")!= 1:
        messagebox.showerror("Error", "Give correct email")
    else:
        messagebox.showinfo("Success", "Account created")

    
    if name in users:
        messagebox.showerror("Error", "User already exists")
        return

    users[name] = {
        "name": name,
        "password": password,
        "gender": gender,
        "email": email,
        "role": role
    }

    messagebox.showinfo("Success", "Account created")
def go_back_to_auth():
    screen3_frame.pack_forget()
    screen3_center_frame.pack_forget()
    #2nd frame
    screen2_frame.pack(fill="both", expand=True)

create = Button(screen3_center_frame,text="Create account",font=("Arial",20,"bold"),fg="black",bg="red",width=30,height=1,command=create_account)
create.pack()
top_frame = Frame(screen3_frame, bg="black")
top_frame.pack(fill="x")
back = Button(top_frame, text="← Back", command=go_back_to_auth)
back.pack(anchor="w", padx=10, pady=10)



#screen 2 center gui
screen2_center_frame= Frame(screen2_frame, bg="black")
screen2_center_frame.pack(expand=True)
title = Label(screen2_center_frame,text="Authentication",font=("Arial",30,"bold"),fg="white",bg="black")
title.pack()
title1 = Label(screen2_center_frame,text="Screen",font=("Arial",30,"bold"),fg="white",bg="black")
title1.pack()
login = Button(screen2_center_frame,text="Login",font=("Arial",20),width=10,height=1,fg="white",bg="red",command=open_login)
login.pack(pady=20)
register =Button(screen2_center_frame,text="Register",font=("Arial",20),width=10,height=1,fg="white",bg="blue",command=open_register)
register.pack(pady=20)

#screen 1 center gui
screen1_center_frame= Frame(screen1_frame, bg="black")
title = Label(screen1_center_frame, text="StudySpark ⚡", font=("Arial",30,"bold"),fg="white",bg="black")
title.pack(pady=10)
note= Label(screen1_center_frame,text="Ignite Your Learning Journey", font=("Calibri",15),fg="grey",bg="black")
note.pack(pady=10)
start = Button(screen1_center_frame,text="Enter StudySpark ⚡",font=("Arial",25,"bold"),width=20,height=1,fg="black",bg="yellow",command=go_to_auth)
start.pack(pady=70)
screen1_center_frame.pack(expand=True)

#run theapp
root.mainloop()
print(users) 