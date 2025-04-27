import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk,messagebox,colorchooser
import os
from datetime import date

def show_frame(frame):
    frame.tkraise()
#show the search bar only appear when it changes to the note_frame
    if frame == home_frame:
        search_entry.place(relx=0.5, rely=0.5, anchor="center")
    else:
        search_entry.place_forget()


def update_file_list():
    file_listbox.delete(0, tk.END)
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    for file in files:
        file_listbox.insert(tk.END, file)

#function for listbox
def show_listbox_menu(event):
    try:
        # Select the item under mouse
        file_listbox.selection_clear(0, tk.END)# clear selection if choose other things
        file_listbox.selection_set(file_listbox.nearest(event.y))#find item nearest to where you clicked.
        listbox_menu.post(event.x_root, event.y_root)# the menu show at mouse screen position
    finally:
        listbox_menu.grab_release()#prevent the menu freeze the app until you click

def pin_selected_note():
    selected = file_listbox.curselection()
    if selected:
        file_name = file_listbox.get(selected)
        if file_name not in pinned_files:
            confirm = messagebox.askyesno("Pin", f"Do you want to pin '{file_name}'?")
            if confirm:
                pinned_files.append(file_name)
                tree.insert("", tk.END, values=(file_name,))
                messagebox.showinfo("Info", f"Pinned '{file_name}' successfully!")
                save_pinned_notes()
        else:
            messagebox.showinfo("Info", "This note is already pinned.")



def unpin_selected_note():
    selected = file_listbox.curselection()
    if selected:
        file_name = file_listbox.get(selected)
        if file_name in pinned_files:
            confirm = messagebox.askyesno("Unpin", f"Do you want to unpin '{file_name}'?")
            if confirm:
                pinned_files.remove(file_name)
                # Remove from treeview
                for item in tree.get_children():
                    if tree.item(item, "values")[0] == file_name:
                        tree.delete(item)
                        break
                messagebox.showinfo("Info", f"Unpinned '{file_name}' successfully!")
        else:
            messagebox.showinfo("Remind", "This note is not pinned yet.")
    else:
        messagebox.showinfo("Remind", "Please select a note first.")




# function for treeview
def show_tree_menu(event):
    try:
        # Select the item under the mouse
        tree.selection_remove(tree.selection())
        tree.selection_set(tree.identify_row(event.y))#find item nearest you clicked.
        tree_menu.post(event.x_root, event.y_root)
    finally:
        tree_menu.grab_release()#prevent menu freeze the app until you click


def unpin_from_tree():
    selected = tree.selection()
    if selected:
        file_name = tree.item(selected[0], "values")[0]
        confirm = messagebox.askyesno("Unpin", f"Do you want to unpin '{file_name}'?")
        if confirm:
            if file_name in pinned_files:
                pinned_files.remove(file_name)
            tree.delete(selected[0])
            messagebox.showinfo("Info", f"Unpinned '{file_name}' successfully!")
    else:
        messagebox.showinfo("Remind", "Please select a pinned note first.")

def save_pinned_notes():
    with open("pinned_notes.txt", "w") as f:# create a file if the specified file does not exist
        for note in pinned_files:
            f.write(note + "\n")#open if exist ,,,if no ,create a new file



def load_pinned_notes():
    if os.path.exists("pinned_notes.txt"):
        with open("pinned_notes.txt", "r") as f:
            for line in f:
                note = line.strip()
                pinned_files.append(note)
                tree.insert("", tk.END, values=(note,))



# In your calendar section:
def setup_calendar():
    global cal
    today = date.today()  # Get today's date
    cal = Calendar(
        calendar_frame,
        selectmode='day',
        font=("Arial", 16),  # Make text bigger
        cursor="hand1"  # Change cursor when hover
    )
    cal.pack(padx=(0,50),pady=(80,90), expand=True, fill="both")  # Expand to fill available space

def choose_calendar_color():
    color = colorchooser.askcolor(title="Choose Calendar Color")[1]  # Open color picker and get HEX color
    if color:
        cal.config(
            background=color,
            disabledbackground=color,
            normalbackground=color,
            weekendbackground=color,
            selectbackground=color,
            selectforeground="white",
        )

def apply_theme(choice):
    if choice == "Custom":
        choose_calendar_color()
    elif choice == "Pink":
        cal.config(
            background="#FFE4E1",
            disabledbackground="#FFE4E1",
            normalbackground="#FFE4E1",
            weekendbackground="#FFD1DC",
            selectbackground="#FF69B4",
            selectforeground="white",
        )
    elif choice == "Blue":
        cal.config(
            background="#E0FFFF",
            disabledbackground="#E0FFFF",
            normalbackground="#E0FFFF",
            weekendbackground="#ADD8E6",
            selectbackground="#00BFFF",
            selectforeground="white",
        )
    elif choice == "Purple":
        cal.config(
            background="#E6E6FA",
            disabledbackground="#E6E6FA",
            normalbackground="#E6E6FA",
            weekendbackground="#D8BFD8",
            selectbackground="#9370DB",
            selectforeground="white",
        )


root= tk.Tk()
#the title show on the top
root.title("MMU Study Buddy")
# the size of whole window show
root.state("zoomed")


pinned_files = []
folder_path = "C:/Notes"



# Create a menu for right-click (context menu)
listbox_menu = tk.Menu(root, tearoff=0)# tear off is the dash line in the menu list
listbox_menu.add_command(label="Pin", command=lambda: pin_selected_note())
listbox_menu.add_command(label="Unpin", command=lambda: unpin_selected_note())



#show the frame at the top
top_frame = tk.Frame(root, bg="dark blue", height=50)
top_frame.pack(side="top", fill="x")

# show the searchbar in the frame
search_entry = tk.Entry(top_frame, width=50, font=('Aptos', 15))

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




##section note
#show the location and the feature of the fonts showed
note_lbl= tk.Label(home_frame, text="All Note",font=('Arial',30))
note_lbl.place(x=15,y=0)

file_listbox = tk.Listbox(home_frame, width=221,height=20)
file_listbox.place(x=20,y=60)


tree_menu = tk.Menu(root, tearoff=0)
tree_menu.add_command(label="Unpin", command=lambda: unpin_from_tree())

file_listbox.bind("<Button-3>", show_listbox_menu)# the right click function and bind with the show_list_menu function


update_file_list()

#three button for the new, open, delete function
btn_new = tk.Button(home_frame, text="New", font=20,relief="flat",width=30, height=5)
btn_new.place(x=50, y=400)

btn_open = tk.Button(home_frame, text="Open",font=20, relief="flat",width=30, height=5)
btn_open.place(x=500, y=400)

btn_delete = tk.Button(home_frame, text="Delete",font=20,relief="flat",width=30, height=5)
btn_delete.place(x=950, y=400)

pinnednote_lbl= tk.Label(home_frame, text="Pinned Note",bg="white",font=('Arial',25))
pinnednote_lbl.place(x=15,y=550)


#create a box for the pinned note
tree = ttk.Treeview(home_frame, columns=("Name",), show="headings", height=15)
tree.heading("Name", text="File Name",)
tree.column("Name", width=1325)
tree.place(x=20, y=600)
tree.bind("<Button-3>", show_tree_menu)
load_pinned_notes()


#timer section
timer_lbl= tk.Label(timer_frame, text="Timer Section", font=("Arial", 30), bg="white")
timer_lbl.place(x=0,y=0)

#calendar section
calendar_lbl= tk.Label(calendar_frame,text="Calendar",bg="white",font=('Arial',30))
calendar_lbl.place(x=0,y=0)
setup_calendar()

theme_var = tk.StringVar()
theme_var.set("Choose Theme")  # Default text

theme_options = ["Pink", "Blue", "Purple", "Custom"]

theme_menu = tk.OptionMenu(calendar_frame, theme_var, *theme_options, command=apply_theme)
theme_menu.config(font=("Arial", 12), bg="#f0f0f0")
theme_menu.pack(pady=10)

#todolist section
todolist_lbl= tk.Label(todolist_frame,text="To- Do-List",bg="white", font=('Arial',30))
todolist_lbl.place(x=0,y=0)


show_frame(home_frame)



root.mainloop()


