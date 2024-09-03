# Import modules
import os  
from tkinter import *  
from tkinter import messagebox  
import time  

# Constants  
BACKGROUND = "#f0f0f0"  
HIGH_SCORE_FILE = "high_score.txt"  

# Load high score from a file  
def load_high_score():  
    if os.path.exists(HIGH_SCORE_FILE):  
        with open(HIGH_SCORE_FILE, 'r') as file:  
            return float(file.read().strip())  
    return 0.0  

# Save high score to a file  
def save_high_score(new_high_score):  
    with open(HIGH_SCORE_FILE, 'w') as file:  
        file.write(f"{new_high_score:.2f}")  

# Clear high score  
def reset_high_score():  
    global high_score  
    high_score = 0.0  
    save_high_score(high_score)  
    high_score_label.config(text=f"High Score: {high_score:.2f} characters per minute")  

# Calculate typing speed  
def calculate_typing_speed(typed_text, elapsed_time):  
    num_chars = len(typed_text)  
    speed = (num_chars / elapsed_time) * 60  # Convert to characters per minute  
    return speed  

# Start the typing test  
def start_typing_test():  
    input_box.delete("1.0", "end")  # Clear the text box  
    input_box.config(state=NORMAL)  # Enable the input box  
    score_label.config(text="Typing speed: 0.00 characters per minute")  # Reset score display  

    countdown_timer.reset()  # Reset the countdown timer  
    countdown_timer.start_countdown(5)  # Start the countdown  

# Calculate and display speed  
def calculate_speed():  
    typed_text = input_box.get("1.0", "end-1c")  
    elapsed_time = 30  # Duration of the typing test  
    speed = calculate_typing_speed(typed_text, elapsed_time)  
    score_label.config(text=f"Typing speed: {speed:.2f} characters per minute")  
    update_high_score(speed)  

# Update high score if applicable  
def update_high_score(speed):  
    global high_score  
    if speed > high_score:  
        high_score = speed  
        save_high_score(high_score)  
        high_score_label.config(text=f"High Score: {high_score:.2f} characters per minute")  

# Countdown timer
class CountdownTimer: 
    # Constructor 
    def __init__(self, master):  
        self.master = master
        self.input_box = input_box
        self.label = Label(master, text="5", font=("Arial", 24), bg=BACKGROUND)
        self.label.pack()
        self.time = 5
        self.typing_time = 30  # Duration of the typing test
        self.is_typing = False

    # Start the countdown
    def start_countdown(self, start_time):  
        self.time = start_time  
        self.update_timer()  
    
    # Reset the timer
    def reset(self):  
        self.is_typing = False  
        self.label.config(text="5")  # Reset to the countdown ready state  

    # Update the timer
    def update_timer(self):  
        if self.time > 0:  
            self.label.config(text=str(self.time))  
            self.time -= 1  
            self.master.after(1000, self.update_timer)  
        else:  
            if not self.is_typing:  # Start the 30-second typing test  
                self.is_typing = True  
                self.typing_time = 30  
                self.input_box.config(state=NORMAL)  # Enable the input box for typing  
                self.update_typing_timer()  
            else:  
                calculate_speed()  # End the test and calculate speed  

    # Update the typing timer
    def update_typing_timer(self):
        if self.typing_time > 0:
            self.label.config(text=f"Time left: {self.typing_time}")
            self.typing_time -= 1
            self.time = self.typing_time
            self.master.after(1000, self.update_typing_timer)
        else:
            calculate_speed() # End the test and calculate speed  

# Confirmation prompt for resetting high score  
def confirm_reset_high_score():  
    if messagebox.askyesno("Confirm Reset", "Are you sure you want to reset the high score?"):  
        reset_high_score()  

        

# Main function
def main():  
    global input_box, score_label, high_score_label, high_score, countdown_timer  

    high_score = load_high_score()  

    # Create the main window
    root = Tk()  
    root.title("Typing Speed Test")  
    root.configure(background=BACKGROUND)  
    root.minsize(400, 550)  
    root.maxsize(400, 550)
    root.overrideredirect(True)  # Removes the window frame
    root.attributes("-topmost", True)  # Keeps the widget on top of other windows
    def move_window(event):
        root.geometry(f'+{event.x_root}+{event.y_root}')
    root.bind('<B1-Motion>', move_window)  # Bind the left mouse button drag to moving the window  

    # Create the widgets
    title_label = Label(root, text="Typing Speed Test", bg=BACKGROUND, font=("Arial", 24, "bold"))  
    title_label.pack()  

    score_label = Label(root, text="Typing speed: 0.00 characters per minute", bg=BACKGROUND, font=("Arial", 20), wraplength=350)  
    score_label.pack(pady=20)  

    high_score_label = Label(root, text=f"High Score: {high_score:.2f} characters per minute", bg=BACKGROUND, font=("Arial", 20), wraplength=350)  
    high_score_label.pack(pady=10)  

    input_box = Text(root, width=40, height=10)  
    input_box.pack(pady=10)  

    start_button = Button(root, text="Start", command=start_typing_test)  # Start the game or restart it  
    start_button.pack(pady=5)  

    reset_button = Button(root, text="Reset High Score", command=confirm_reset_high_score)  # Reset high score  
    reset_button.pack(pady=5)

    exit_button = Button(root, text="X", command=root.quit, bg="red", fg="white")
    exit_button.place(x=370, y=10)  # Adjust placement according to your UI  

    countdown_timer = CountdownTimer(root)  

    root.mainloop()  

if __name__ == "__main__":  
    main()