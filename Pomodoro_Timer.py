# ==================== IMPORT LIBRARIES ====================
# These libraries provide essential functionality for the application

import tkinter as tk  # Tkinter: GUI framework for creating windows and interactive widgets
from tkinter import messagebox  # messagebox: Display popup alerts and information dialogs
import threading  # threading: Run the timer in background without freezing the user interface
import pyttsx3  # pyttsx3: Text-to-speech library for voice announcements


# ==================== MAIN CLASS ====================
class PomodoroTimer:
    """
    A Pomodoro Timer Application using Tkinter GUI
    
    Features:
    - Customizable work and break durations
    - Voice announcements for session switches
    - Interactive buttons for control
    - Session counter to track productivity
    - Fixed window size that cannot be maximized
    """
    
    def __init__(self, root):
        """
        Initialize the Pomodoro Timer window and all UI components
        
        Args:
            root (tk.Tk): The main Tkinter window object
        """
        # ===== WINDOW SETUP =====
        self.root = root
        self.root.title("Pomodoro Timer")  # Set window title
        self.root.geometry("450x400")  # Set fixed window dimensions (width x height in pixels)
        self.root.resizable(False, False)  # PREVENT window from being resized or maximized
        self.root.config(bg="#2c3e50")  # Set dark blue background color
        
        # ===== TIMER VARIABLES =====
        # These variables store the state and timing information
        self.work_time = 25 * 60  # Work session duration: 25 minutes (converted to seconds)
        self.break_time = 5 * 60  # Break session duration: 5 minutes (converted to seconds)
        self.remaining_time = self.work_time  # Current countdown timer value
        self.is_running = False  # Boolean flag: True if timer is currently running
        self.is_work = True  # Boolean flag: True for work time, False for break time
        self.sessions = 0  # Counter: Number of completed work sessions
        
        # ===== TEXT-TO-SPEECH ENGINE =====
        # Initialize pyttsx3 for voice announcements
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Set speech speed (words per minute)
        
        # ===== UI COMPONENT 1: TITLE LABEL =====
        tk.Label(root, text="⏱ POMODORO TIMER", 
                font=("Arial", 14, "bold"),  # Font: Arial, size 14, bold
                bg="#2c3e50",  # Background color: dark blue
                fg="#ecf0f1"   # Foreground color: light gray
                ).pack(pady=10)  # Add padding on top and bottom
        
        # ===== UI COMPONENT 2: STATUS LABEL =====
        # This label shows whether it's WORK TIME or BREAK TIME
        self.status = tk.Label(root, 
                              text="WORK TIME", 
                              font=("Arial", 11, "bold"), 
                              bg="#2c3e50", 
                              fg="#3498db")  # Blue color for work time
        self.status.pack()
        
        # ===== UI COMPONENT 3: MAIN TIMER DISPLAY =====
        # Large timer display showing MM:SS format (e.g., "25:00")
        self.time_label = tk.Label(root, 
                                  text="25:00",  # Initial display
                                  font=("Arial", 50, "bold"),  # Very large font for visibility
                                  bg="#2c3e50", 
                                  fg="#3498db")  # Blue color
        self.time_label.pack(pady=15)  # Add vertical padding for spacing
        
        # ===== UI COMPONENT 4: SETTINGS PANEL =====
        # Container frame for customizable timer settings
        settings_frame = tk.Frame(root, bg="#34495e")  # Gray background container
        settings_frame.pack(padx=10, pady=10, fill="x")  # Fill horizontally with padding
        
        # Work time label
        tk.Label(settings_frame, text="Work (min):", 
                bg="#34495e", fg="#ecf0f1").grid(row=0, column=0, padx=5, sticky="w")
        
        # Work time input field (Entry widget for user to type)
        self.work_entry = tk.Entry(settings_frame, width=6, font=("Arial", 10))
        self.work_entry.insert(0, "25")  # Set default value to 25 minutes
        self.work_entry.grid(row=0, column=1, padx=5)
        
        # Break time label
        tk.Label(settings_frame, text="Break (min):", 
                bg="#34495e", fg="#ecf0f1").grid(row=0, column=2, padx=5, sticky="w")
        
        # Break time input field
        self.break_entry = tk.Entry(settings_frame, width=6, font=("Arial", 10))
        self.break_entry.insert(0, "5")  # Set default value to 5 minutes
        self.break_entry.grid(row=0, column=3, padx=5)
        
        # "Set" button - Apply custom timer values when clicked
        tk.Button(settings_frame, text="Set", command=self.set_times, 
                 bg="#3498db", fg="white", width=5).grid(row=0, column=4, padx=5)
        
        # ===== UI COMPONENT 5: CONTROL BUTTONS =====
        # Container frame for main control buttons
        btn_frame = tk.Frame(root, bg="#2c3e50")
        btn_frame.pack(pady=10)
        
        # START Button - Green color, begins the timer countdown
        tk.Button(btn_frame, text="Start", command=self.start, 
                 width=8, bg="#27ae60", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        
        # PAUSE Button - Orange color, pauses the running timer
        tk.Button(btn_frame, text="Pause", command=self.pause, 
                 width=8, bg="#f39c12", fg="white", font=("Arial", 10)).grid(row=0, column=1, padx=5)
        
        # RESET Button - Red color, resets timer to default work time
        tk.Button(btn_frame, text="Reset", command=self.reset, 
                 width=8, bg="#e74c3c", fg="white", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        
        # ===== UI COMPONENT 6: STATUS BAR =====
        # Shows session count and current timer state (Running/Paused)
        self.counter = tk.Label(root, text="Sessions: 0 | Status: Ready", 
                               font=("Arial", 10), bg="#2c3e50", fg="#95a5a6")
        self.counter.pack(pady=10)
        
        # ===== KEYBOARD SHORTCUT =====
        # Bind spacebar to Start/Pause functionality for quick control
        self.root.bind("<space>", lambda e: self.start() if not self.is_running else self.pause())
    
    # ==================== METHOD 1: UPDATE ====================
    def update(self):
        """
        Update the timer display with current remaining time in MM:SS format
        
        This method converts remaining seconds into minutes and seconds,
        then updates the label to show time in "25:30" format
        """
        m = self.remaining_time // 60  # Extract minutes (integer division)
        s = self.remaining_time % 60   # Extract seconds (modulo operation)
        self.time_label.config(text=f"{m:02d}:{s:02d}")  # Format as MM:SS with leading zeros
    
    # ==================== METHOD 2: SET_TIMES ====================
    def set_times(self):
        """
        Set custom work and break times from user input fields
        
        This method:
        1. Reads values from the input fields
        2. Validates they are numeric
        3. Converts minutes to seconds
        4. Resets the timer with new values
        5. Shows success/error popup message
        """
        try:
            # Get work time from input field and convert to seconds (multiply by 60)
            self.work_time = int(self.work_entry.get()) * 60
            # Get break time from input field and convert to seconds
            self.break_time = int(self.break_entry.get()) * 60
            
            # Reset timer with newly set values
            self.reset()
            
            # Show success popup message to confirm changes
            messagebox.showinfo("Success", "Timer settings updated!")
            
        except ValueError:
            # If user entered non-numeric value, show error popup
            messagebox.showerror("Error", "Enter valid numbers!")
    
    # ==================== METHOD 3: START ====================
    def start(self):
        """
        Start the timer if it's not already running
        
        This method:
        1. Checks if timer is already running
        2. Sets running flag to True
        3. Updates display status
        4. Launches timer in background thread
        """
        if not self.is_running:  # Only start if not already running
            self.is_running = True  # Set flag to indicate timer is active
            self.update_status()     # Update status label
            
            # Start timer in separate thread to prevent freezing the UI
            # daemon=True means thread will terminate when main program closes
            threading.Thread(target=self.run, daemon=True).start()
    
    # ==================== METHOD 4: RUN ====================
    def run(self):
        """
        Main timer loop - Runs in a separate background thread
        
        This method:
        1. Continuously decrements timer by 1 second
        2. Updates display after each decrement
        3. Waits 1 second before next iteration
        4. Calls switch() when timer reaches 0
        
        Running in a separate thread prevents the UI from freezing
        """
        while self.is_running and self.remaining_time > 0:
            self.remaining_time -= 1  # Decrease timer by 1 second
            self.update()              # Update timer display
            threading.Event().wait(1)  # Wait exactly 1 second before next iteration
        
        # When timer reaches 0, automatically switch to next session
        if self.remaining_time == 0 and self.is_running:
            self.switch()
    
    # ==================== METHOD 5: PAUSE ====================
    def pause(self):
        """
        Pause the running timer
        
        This method:
        1. Sets running flag to False to stop the timer loop
        2. Updates status label to show "Paused"
        """
        self.is_running = False  # Stop the timer loop
        self.update_status()      # Update status display
    
    # ==================== METHOD 6: RESET ====================
    def reset(self):
        """
        Reset timer to default work time
        
        This method:
        1. Stops the timer if running
        2. Sets back to work session
        3. Resets remaining time to full work duration
        4. Updates display colors and labels
        5. Updates status information
        """
        self.is_running = False            # Stop timer if running
        self.is_work = True                # Set to work session
        self.remaining_time = self.work_time  # Set to full work duration
        self.status.config(text="WORK TIME", fg="#3498db")  # Blue label for work
        self.time_label.config(fg="#3498db")  # Blue timer display
        self.update()                      # Refresh the timer display
        self.update_status()               # Refresh status bar
    
    # ==================== METHOD 7: UPDATE_STATUS ====================
    def update_status(self):
        """
        Update the status bar showing session count and current state
        
        This method updates the bottom label to show:
        - Total sessions completed
        - Current state (Running or Paused)
        """
        status = "Running" if self.is_running else "Paused"  # Determine current state
        self.counter.config(text=f"Sessions: {self.sessions} | Status: {status}")
    
    # ==================== METHOD 8: SWITCH ====================
    def switch(self):
        """
        Switch between work and break sessions
        
        This method:
        1. Checks if currently in work mode or break mode
        2. Switches to opposite mode
        3. Updates display colors (blue=work, red=break)
        4. Increments session counter when moving to work
        5. Gives voice announcement of session switch
        6. Updates display and status
        """
        if self.is_work:
            # ===== SWITCHING TO BREAK TIME =====
            self.is_work = False
            self.remaining_time = self.break_time  # Set break duration
            self.status.config(text="BREAK TIME", fg="#e74c3c")  # Red label for break
            self.time_label.config(fg="#e74c3c")  # Red timer display
            self.speak("Break time!")  # Voice announcement
            
        else:
            # ===== SWITCHING TO WORK TIME =====
            self.is_work = True
            self.remaining_time = self.work_time  # Set work duration
            self.sessions += 1  # Increment completed sessions counter
            self.status.config(text="WORK TIME", fg="#3498db")  # Blue label for work
            self.time_label.config(fg="#3498db")  # Blue timer display
            self.speak(f"Session {self.sessions} starting!")  # Voice announcement with session number
        
        # Stop timer and refresh displays
        self.is_running = False
        self.update()        # Refresh timer display
        self.update_status()  # Refresh status bar
    
    # ==================== METHOD 9: SPEAK ====================
    def speak(self, text):
        """
        Convert text to speech and play it as audio
        
        Args:
            text (str): The text message to be converted to speech and spoken aloud
        
        This method uses pyttsx3 to give voice feedback when sessions switch
        """
        self.engine.say(text)      # Queue the text to be spoken
        self.engine.runAndWait()   # Play the speech and wait for completion

# ==================== MAIN ENTRY POINT ====================
if __name__ == "__main__":
    """
    This code runs only when the script is executed directly (not imported)
    """
    root = tk.Tk()  # Create the main Tkinter window
    app = PomodoroTimer(root)  # Initialize the Pomodoro Timer application
    app.update()  # Display initial timer value
    root.mainloop()  # Start the GUI event loop and keep window open
