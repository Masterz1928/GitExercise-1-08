import tkinter as tk
from calendar import calendar
from tkinter import ttk

def show_frame(frame):
    frame.tkraise()

root= tk.Tk()
#the title show on the top
root.title("MMU Study Buddy")
# the size of whole window show
root.state("zoomed")

#show the frame at the top
top_frame = tk.Frame(root, bg="dark blue", height=50)
top_frame.pack(side="top", fill="x")

# show the searchbar in the frame
search_entry = tk.Entry(top_frame, width=50, font=('Aptos', 15))
search_entry.place(relx=0.5, rely=0.5, anchor="center")

# show the sidebar
sidebar = tk.Frame(root, width=120, bg="#f1efec")
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
    ("Note", home_frame),
    ("Timer", timer_frame),
    ("Calendar", calendar_frame),
    ("To-do-list", todolist_frame)
]
    #button features
for text, frame in nav_buttons:
    btn = tk.Button(sidebar, text=text,
    font=("Segoe UI", 12, "bold"),  # System-like font
    bg="#1d72e8",  # Primary blue
    fg="white",  # White text
    activebackground="#155cc1",  # Pressed color
    activeforeground="white",
    relief="flat",  # Flat, modern look
    padx=20,
    pady=10,
    bd=0 ,command=lambda f=frame: show_frame(f))
    btn.pack(fill="x", padx=20, pady=20, ipady="15")

timer_lbl= tk.Label(timer_frame, text="Timer Section", font=("Arial", 30), bg="white")
timer_lbl.place(x=0,y=0)


##section note
#show the location and the feature of the fonts showed
note_lbl= tk.Label(home_frame, text="All Note",bg="white",font=('Arial',30))
note_lbl.place(x=15,y=0)

#use treeview to build a box to show the file we already created in this window
tree = ttk.Treeview(home_frame, columns=("Name",), show="headings", height=15)
tree.heading("Name", text="File Name",)
tree.column("Name", width=1325)
tree.place(x=20, y=60)

# as a sample that show the file how to shown in the window if there has any things i will add it
#f, is a tuple/tk.END is insert the files from the back
files = ["Note 1", "Note 2", "Homework.docx", "TodoList.txt"]
for f in files:
    tree.insert('', tk.END, values=(f,))

btn_new = tk.Button(home_frame, text="New", font=20,relief="flat",width=30, height=5)
btn_new.place(x=50, y=400)

btn_open = tk.Button(home_frame, text="Open",font=20, relief="flat",width=30, height=5)
btn_open.place(x=500, y=400)

btn_delete = tk.Button(home_frame, text="Delete",font=20,relief="flat",width=30, height=5)
btn_delete.place(x=950, y=400)

pinnednote_lbl= tk.Label(home_frame, text="Pinned Note",bg="white",font=('Arial',25))
pinnednote_lbl.place(x=15,y=550)

tree = ttk.Treeview(home_frame, columns=("Name",), show="headings", height=15)
tree.heading("Name", text="File Name",)
tree.column("Name", width=1325)
tree.place(x=20, y=600)


calendar_lbl= tk.Label(calendar_frame,text="Calendar",bg="white",font=('Arial',30))
calendar_lbl.place(x=0,y=0)

todolist_lbl= tk.Label(todolist_frame,text="To- Do-List",bg="white", font=('Arial',30))
todolist_lbl.place(x=0,y=0)


show_frame(home_frame)






root.mainloop()


