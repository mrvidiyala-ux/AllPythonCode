from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("To-Do List App")
root.geometry("400x400")
root.config(bg="#f7f7f7")
root.resizable(False, False)

def add_task():
    task = task_entry.get()
    if task != "":
        listbox.insert(END, task)
        task_entry.delete(0, END)
    else:
        messagebox.showwarning("Warning", "Please enter a task!")

def delete_task():
    try:
        selected = listbox.curselection()
        listbox.delete(selected)
    except:
        messagebox.showwarning("Warning", "Please select a task to delete!")

def clear_all():
    listbox.delete(0, END)

heading = Label(root, text="📝 My To-Do List", font=("Arial", 16, "bold"), bg="#f7f7f7")
heading.pack(pady=10)

task_entry = Entry(root, width=30, font=("Arial", 12))
task_entry.pack(pady=5)

add_button = Button(root, text="Add Task", width=15, command=add_task, bg="#90EE90")
add_button.pack(pady=5)

listbox = Listbox(root, width=40, height=10, font=("Arial", 12))
listbox.pack(pady=10)

delete_button = Button(root, text="Delete Task", width=15, command=delete_task, bg="#FFB6C1")
delete_button.pack(pady=5)

clear_button = Button(root, text="Clear All", width=15, command=clear_all, bg="#FF6347", fg="white")
clear_button.pack(pady=5)

root.mainloop()