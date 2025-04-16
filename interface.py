import tkinter as tk
from tkinter import ttk

def show_frame(frame):
    frame.tkraise()

root= tk.Tk()
#the title show on the top
root.title("MMU Study Buddy")
# the size of whole window show
root.geometry("1920x1080")

#show the frame at the top
top_frame = tk.Frame(root, bg="dark blue", height=50)
top_frame.pack(side="top", fill="x")

# show the searchbar in the frame
search_entry = tk.Entry(top_frame, width=50, font=('Aptos', 15))
search_entry.place(relx=0.5, rely=0.5, anchor="center")

# show the sidebar
sidebar = tk.Frame(root, width=120, bg="white")
sidebar.pack(side="left", fill="y")

content_area = tk.Frame(root, bg="white")
content_area.pack(expand=True, fill="both")

# Create different frames for each own section
home_frame = tk.Frame(content_area, bg="white")
timer_frame = tk.Frame(content_area, bg="white")
calendar_frame = tk.Frame(content_area, bg="white")
todolist_frame = tk.Frame(content_area, bg="white")

for frame in (home_frame, timer_frame, calendar_frame, todolist_frame):
    frame.place(relwidth=1, relheight=1)

#Buttons for Navigation
nav_buttons = [
    ("Home", home_frame),
    ("Timer", timer_frame),
    ("Calendar", calendar_frame),
    ("To-do-list", todolist_frame)
]
    #button features
for text, frame in nav_buttons:
    btn = tk.Button(sidebar, text=text, fg="black", bg="white", font=('Aptos', 15),
                    anchor="w", relief="flat", command=lambda f=frame: show_frame(f))
    btn.pack(fill="x", padx=10, pady=20)

timer_lbl= tk.Label(timer_frame, text="Timer Section", font=("Arial", 30), bg="white")
timer_lbl.place(x=0,y=0)

#show the location and the feature of the fonts showed
lbl= tk.Label(home_frame, text="Home",bg="white",font=('Arial',30),anchor="w")
lbl.place(x=0,y=0)

root.mainloop()