import tkinter as tk
from tkinter import simpledialog
import time


def set_timer():
    global focus_time, short_break_time, long_break_time, completed_cycles
    focus_time = simpledialog.askinteger("Input", "Focus time in minutes:", parent=root, minvalue=1, maxvalue=60)
    short_break_time = simpledialog.askinteger("Input", "Short break time in minutes:", parent=root, minvalue=1, maxvalue=15)
    long_break_time = simpledialog.askinteger("Input", "Long break time in minutes:", parent=root, minvalue=15, maxvalue=60)
    completed_cycles = 0
    update_timer(focus_time * 60)
    update_cycles()


def update_cycles():
    cycles_var.set(f"Completed Cycles: {completed_cycles}")


def countdown(t):
    global running, completed_cycles
    minutes, seconds = divmod(t, 60)
    timer_var.set(f"{minutes:02d}:{seconds:02d}")
    if running:
        if t > 0:
            root.after(1000, countdown, t-1)
        else:
            if completed_cycles % 4 == 0 and completed_cycles > 0:
                update_timer(long_break_time * 60)
                completed_cycles += 1
            elif focus:
                update_timer(short_break_time * 60)
                completed_cycles += 1
            else:
                update_timer(focus_time * 60)
            focus_switch()
            update_cycles()


def start_timer():
    global running, focus
    running = True
    focus = True
    countdown(focus_time * 60)


def pause_timer():
    global running
    if running:
        running = False
        start_button.config(command=rescue_timer, text='Resume')


def rescue_timer():
    global running
    running = True
    start_button.config(command=pause_timer, text='Pause')
    countdown(int(timer_var.get().split(':')[0]) * 60 + int(timer_var.get().split(':')[1]))


def reset_timer():
    global running
    running = False
    update_timer(focus_time * 60)


def update_timer(sec):
    minutes, seconds = divmod(sec, 60)
    timer_var.set(f"{minutes:02d}:{seconds:02d}")


def focus_switch():
    global focus
    focus = not focus


# Initialize variables
running = False
focus = True
focus_time = 25  # default focus time in minutes
short_break_time = 5  # default short break time in minutes
long_break_time = 15  # default long break time in minutes
completed_cycles = 0

# GUI setup
root = tk.Tk()
root.title("Pomodoro Timer")

timer_var = tk.StringVar()
timer_var.set(f"{focus_time:02d}:00")
cycles_var = tk.StringVar()
cycles_var.set(f"Completed Cycles: {completed_cycles}")

label_timer = tk.Label(root, textvariable=timer_var, font=("Arial", 30))
label_timer.pack()

label_cycles = tk.Label(root, textvariable=cycles_var, font=("Arial", 14))
label_cycles.pack()

frame = tk.Frame(root)
frame.pack()

start_button = tk.Button(frame, text="Start", command=start_timer)
start_button.pack(side=tk.LEFT)

pause_button = tk.Button(frame, text="Pause", command=pause_timer)
pause_button.pack(side=tk.LEFT)

reset_button = tk.Button(frame, text="Reset", command=reset_timer)
reset_button.pack(side=tk.LEFT)

set_timer_button = tk.Button(frame, text="Set Timer", command=set_timer)
set_timer_button.pack(side=tk.LEFT)

root.mainloop()