# ...existing code...
import tkinter as tk
import tkinter.font as tkfont
import time
import math
import ast
import sys
import traceback

PROMPT = ">>> "

class TkConsole:
    def __init__(self, master):
        self.master = master
        master.title("Tkinter Console")
        font = tkfont.Font(family="Courier", size=11)

        self.text = tk.Text(master, wrap="word", undo=True, font=font)
        self.text.pack(fill="both", expand=True, padx=4, pady=4)
        self.text.configure(bg="black", fg="white", insertbackground="white")

        # make text widget behave like a console
        self.text.bind("<Return>", self.on_enter)
        self.text.bind("<BackSpace>", self.on_backspace)
        self.text.bind("<Key>", self.on_key)
        self.text.bind("<Control-c>", self.copy)
        self.text.bind("<Control-C>", self.copy)

        self.text.tag_configure("stdout", foreground="#a6e22e")
        self.text.tag_configure("stderr", foreground="#f92672")
        self.text.tag_configure("prompt", foreground="#66d9ef", font=font)

        self.insert_welcome()
        self.insert_prompt()

    def insert_welcome(self):
        self.write("Simple Tkinter console (text-based). Type 'help' for commands.\n\n")

    def insert_prompt(self):
        self.text.configure(state="normal")
        self.text.insert("end", PROMPT, ("prompt",))
        self.text.mark_set("input_start", "insert")
        self.text.see("end")
        self.text.configure(state="normal")
        self.text.focus_set()

    def get_input_range(self):
        start = self.text.index("input_start")
        end = self.text.index("end-1c")
        return start, end

    def read_input(self):
        start, end = self.get_input_range()
        return self.text.get(start, end)

    def on_enter(self, event=None):
        cmd = self.read_input()
        # move to next line so user sees their command
        self.text.insert("end", "\n")
        self.process_command(cmd.strip())
        self.insert_prompt()
        return "break"

    def on_backspace(self, event):
        # prevent deleting the prompt
        cur = self.text.index("insert")
        if self.text.compare(cur, "<=", "input_start"):
            return "break"
        # allow normal backspace
        return None

    def on_key(self, event):
        # prevent moving cursor before prompt with clicks/keys
        try:
            cur = self.text.index("insert")
            if self.text.compare(cur, "<", "input_start"):
                self.text.mark_set("insert", "end-1c")
        except tk.TclError:
            pass
        return None

    def copy(self, event=None):
        try:
            self.master.clipboard_clear()
            selection = self.text.selection_get()
            self.master.clipboard_append(selection)
        except Exception:
            pass
        return "break"

    def write(self, data, tag="stdout"):
        self.text.configure(state="normal")
        self.text.insert("end", str(data), (tag,))
        self.text.see("end")
        self.text.configure(state="normal")

    def write_err(self, data):
        self.write(data, tag="stderr")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="normal")

    def process_command(self, cmd):
        if cmd == "":
            return
        parts = cmd.split()
        cmd0 = parts[0].lower()

        if cmd0 in ("help", "?"):
            self.write("Commands:\n")
            self.write("  help, ?       show this help\n")
            self.write("  clear         clear the console\n")
            self.write("  echo <text>   print text\n")
            self.write("  time          show current time\n")
            self.write("  exit, quit    close the console\n")
            self.write("You can also enter simple Python expressions (e.g. 2+2, math.sin(1)).\n")
            return

        if cmd0 == "clear":
            self.clear()
            return

        if cmd0 == "echo":
            self.write(" ".join(parts[1:]) + "\n")
            return

        if cmd0 == "time":
            self.write(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            return

        if cmd0 in ("exit", "quit"):
            self.master.quit()
            return

        # try to evaluate as a Python expression (safe-ish)
        try:
            # parse to ensure it's an expression, not statements
            node = ast.parse(cmd, mode="eval")
            code = compile(node, "<input>", "eval")
            safe_globals = {"__builtins__": None, "math": math}
            result = eval(code, safe_globals, {})
            self.write(repr(result) + "\n")
        except Exception as e:
            # if not an expression try as a statement (limited)
            try:
                node2 = ast.parse(cmd, mode="exec")
                code2 = compile(node2, "<input>", "exec")
                safe_globals = {"__builtins__": None, "math": math}
                exec(code2, safe_globals, {})
                self.write("\n")
            except Exception:
                tb = traceback.format_exc()
                self.write_err(tb + "\n")

def main():
    root = tk.Tk()
    root.geometry("700x400")
    app = TkConsole(root)
    root.mainloop()

if __name__ == "__main__":
    main()

# filepath: c:\Users\Maniram.LAPTOP-2J12BJKB\PYTHON7\Console.py
# ...existing code...
import tkinter as tk
import tkinter.font as tkfont
import time
import math
import ast
import sys
import traceback

PROMPT = ">>> "

class TkConsole:
    def __init__(self, master):
        self.master = master
        master.title("Tkinter Console")
        font = tkfont.Font(family="Courier", size=11)

        self.text = tk.Text(master, wrap="word", undo=True, font=font)
        self.text.pack(fill="both", expand=True, padx=4, pady=4)
        self.text.configure(bg="black", fg="white", insertbackground="white")

        # make text widget behave like a console
        self.text.bind("<Return>", self.on_enter)
        self.text.bind("<BackSpace>", self.on_backspace)
        self.text.bind("<Key>", self.on_key)
        self.text.bind("<Control-c>", self.copy)
        self.text.bind("<Control-C>", self.copy)

        self.text.tag_configure("stdout", foreground="#a6e22e")
        self.text.tag_configure("stderr", foreground="#f92672")
        self.text.tag_configure("prompt", foreground="#66d9ef", font=font)

        self.insert_welcome()
        self.insert_prompt()

    def insert_welcome(self):
        self.write("Simple Tkinter console (text-based). Type 'help' for commands.\n\n")

    def insert_prompt(self):
        self.text.configure(state="normal")
        self.text.insert("end", PROMPT, ("prompt",))
        self.text.mark_set("input_start", "insert")
        self.text.see("end")
        self.text.configure(state="normal")
        self.text.focus_set()

    def get_input_range(self):
        start = self.text.index("input_start")
        end = self.text.index("end-1c")
        return start, end

    def read_input(self):
        start, end = self.get_input_range()
        return self.text.get(start, end)

    def on_enter(self, event=None):
        cmd = self.read_input()
        # move to next line so user sees their command
        self.text.insert("end", "\n")
        self.process_command(cmd.strip())
        self.insert_prompt()
        return "break"

    def on_backspace(self, event):
        # prevent deleting the prompt
        cur = self.text.index("insert")
        if self.text.compare(cur, "<=", "input_start"):
            return "break"
        # allow normal backspace
        return None

    def on_key(self, event):
        # prevent moving cursor before prompt with clicks/keys
        try:
            cur = self.text.index("insert")
            if self.text.compare(cur, "<", "input_start"):
                self.text.mark_set("insert", "end-1c")
        except tk.TclError:
            pass
        return None

    def copy(self, event=None):
        try:
            self.master.clipboard_clear()
            selection = self.text.selection_get()
            self.master.clipboard_append(selection)
        except Exception:
            pass
        return "break"

    def write(self, data, tag="stdout"):
        self.text.configure(state="normal")
        self.text.insert("end", str(data), (tag,))
        self.text.see("end")
        self.text.configure(state="normal")

    def write_err(self, data):
        self.write(data, tag="stderr")

    def clear(self):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.configure(state="normal")

    def process_command(self, cmd):
        if cmd == "":
            return
        parts = cmd.split()
        cmd0 = parts[0].lower()

        if cmd0 in ("help", "?"):
            self.write("Commands:\n")
            self.write("  help, ?       show this help\n")
            self.write("  clear         clear the console\n")
            self.write("  echo <text>   print text\n")
            self.write("  time          show current time\n")
            self.write("  exit, quit    close the console\n")
            self.write("You can also enter simple Python expressions (e.g. 2+2, math.sin(1)).\n")
            return

        if cmd0 == "clear":
            self.clear()
            return

        if cmd0 == "echo":
            self.write(" ".join(parts[1:]) + "\n")
            return

        if cmd0 == "time":
            self.write(time.strftime("%Y-%m-%d %H:%M:%S") + "\n")
            return

        if cmd0 in ("exit", "quit"):
            self.master.quit()
            return

        # try to evaluate as a Python expression (safe-ish)
        try:
            # parse to ensure it's an expression, not statements
            node = ast.parse(cmd, mode="eval")
            code = compile(node, "<input>", "eval")
            safe_globals = {"__builtins__": None, "math": math}
            result = eval(code, safe_globals, {})
            self.write(repr(result) + "\n")
        except Exception as e:
            # if not an expression try as a statement (limited)
            try:
                node2 = ast.parse(cmd, mode="exec")
                code2 = compile(node2, "<input>", "exec")
                safe_globals = {"__builtins__": None, "math": math}
                exec(code2, safe_globals, {})
                self.write("\n")
            except Exception:
                tb = traceback.format_exc()
                self.write_err(tb + "\n")

def main():
    root = tk.Tk()
    root.geometry("700x400")
    app = TkConsole(root)
    root.mainloop()

if __name__ == "__main__":
    main()