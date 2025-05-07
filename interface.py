import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk,messagebox,colorchooser
import os
from datetime import date,datetime
import zipfile

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
    today = date.today()
    cal = Calendar(
        calendar_frame,
        selectmode='day',
        font=("Arial", 16),
        cursor="hand1"
    )
    cal.pack(padx=(0,50), pady=(80,90), expand=True, fill="both")

def choose_calendar_color():
    color = colorchooser.askcolor(title="Choose Calendar Color")[1]  # Open color picker and get HEX color
    if color:
        cal.config(
            background=color,
            headersbackground=color,
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
            background="#FFE4E1",  # Soft pink background
            headersbackground="#FFB6C1",  # A bit stronger pink for headers
            disabledbackground="#FFE4E1",
            normalbackground="#FFE4E1",
            weekendbackground="#FFD1DC",
            selectbackground="#FF69B4",
            selectforeground="white",
        )
    elif choice == "Blue":
        cal.config(
            background="#E0FFFF",  # Light cyan background
            headersbackground="#87CEFA",  # Sky blue headers
            disabledbackground="#E0FFFF",
            normalbackground="#E0FFFF",
            weekendbackground="#ADD8E6",
            selectbackground="#00BFFF",
            selectforeground="white",
        )
    elif choice == "Purple":
        cal.config(
            background="#E6E6FA",  # Lavender background
            headersbackground="#D8BFD8",  # Thistle purple for headers
            disabledbackground="#E6E6FA",
            normalbackground="#E6E6FA",
            weekendbackground="#D8BFD8",
            selectbackground="#9370DB",
            selectforeground="white",
        )

#remark of the calendar
def load_remarks():
    if os.path.exists("remarks.txt"):
        with open("remarks.txt", "r") as f:
            for line in f:
                if "|" in line:
                    date, remark = line.strip().split("|", 1)
                    remarks[date] = remark


def save_remarks():
    with open("remarks.txt", "w") as f:
        for date, remark in remarks.items():
            f.write(f"{date}|{remark}\n")

# Save button
def save_remark_for_date():
    selected_date = cal.get_date()
    remark = remark_entry.get().strip()
    if remark:
        remarks[selected_date] = remark
        save_remarks()
        messagebox.showinfo("Saved", f"Remark for {selected_date} saved.")
    else:
        messagebox.showwarning("Empty", "Please enter a remark.")

# Show existing remark when date selected


def display_remark_for_date(event=None):
    selected_date = cal.get_date()
    remark_entry.delete(0, tk.END)
    if selected_date in remarks:
        remark_entry.insert(0, remarks[selected_date])


def search_notes(event=None):
    search_term = search_entry.get().lower()  # Get search term and make it lowercase for case-insensitive comparison
    file_listbox.delete(0, tk.END)  # Clear the current list in the listbox

    # Loop through all files and add those that match the search term
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    for file in files:
        if search_term in file.lower():  # Case-insensitive comparison
            file_listbox.insert(tk.END, file)

def clear_search():
    search_entry.delete(0, tk.END)  # Clear the search bar
    update_file_list()  # Show all files again


def export_all_notes():
    export_path = "all_notes_export.txt"
    with open(export_path, "w", encoding="utf-8") as export_file:
        files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
        if not files:
            messagebox.showinfo("Info", "No notes to export.")
            return

        for file in files:
            file_path = os.path.join(folder_path, file)
            export_file.write(f"\n--- {file} ---\n")
            with open(file_path, "r", encoding="utf-8") as f:
                export_file.write(f.read() + "\n")

    messagebox.showinfo("Success", f"All notes exported to '{export_path}' successfully.")

def export_notes_with_format():
    # Ask user to choose format
    format_choice = messagebox.askquestion("Export Format", "Export as ZIP file?")

    if format_choice == "yes":
        export_all_notes_as_zip()
    else:
        None


def export_all_notes_as_zip():
    files = [f for f in os.listdir(folder_path) if f.endswith(".txt")]
    if not files:
        messagebox.showinfo("Info", "No notes to export.")
        return

    export_folder = "C:/Notes/Exports"
    os.makedirs(export_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    zip_path = os.path.join(export_folder, f"exported_notes_{timestamp}.zip")

    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            for file in files:
                file_path = os.path.join(folder_path, file)
                zipf.write(file_path, arcname=file)
        messagebox.showinfo("Success", f"Notes exported as ZIP to:\n{zip_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export notes:\n{e}")

def perform_advanced_search():
    query = search_entry.get().strip().lower()
    if not query:
        messagebox.showinfo("Search", "Please enter a keyword.")
        return

    results = []

    # Search in file names and contents
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)

            # Match file name
            if query in file_name.lower():
                results.append(f"File Name Match: {file_name}")

            # Match file content
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                if query in content.lower():
                    results.append(f"Content Match in {file_name}")

    # Search in calendar remarks
    for date_str, remark in remarks.items():
        if query in remark.lower():
            results.append(f"Remark Match: {date_str} - {remark}")

    # Show results
    if results:
        result_text = "\n".join(results)
        messagebox.showinfo("Search Results", result_text)
    else:
        messagebox.showinfo("Search", "No matches found.")

root= tk.Tk()
#the title show on the top
root.title("MMU Study Buddy")
# the size of whole window show
root.state("zoomed")

#dictionary & path
remarks={}
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
search_entry.bind("<Return>", lambda event: perform_advanced_search())

# show the sidebar
sidebar = tk.Frame(root, width=120, bg="#f1efec")
sidebar.pack(side="left", fill="y")

content_area = tk.Frame(root, bg="white")
content_area.pack(expand=True, fill="both")

# Create different frames for each own section
home_frame = tk.Frame(content_area, bg="white")
home_scroll= ttk.Scrollbar(home_frame)
home_scroll.pack(side="right",fill="y",expand= True)

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
note_lbl= tk.Label(home_frame, text="All Note",font=('Arial',30),bg="white")
note_lbl.place(x=15,y=0)

file_listbox = tk.Listbox(home_frame, width=221,height=20)
file_listbox.pack(padx=5,pady=50)


tree_menu = tk.Menu(root, tearoff=0)
tree_menu.add_command(label="Unpin", command=lambda: unpin_from_tree())

file_listbox.bind("<Button-3>", show_listbox_menu)# the right click function and bind with the show_list_menu function
search_entry.bind("<KeyRelease>", search_notes)
clear_search_button = tk.Button(top_frame, text="Clear", command=clear_search)
clear_search_button.place(relx=0.9, rely=0.5, anchor="center")  # Position it next to the search bar

update_file_list()

#three button for the new, open, delete function
button_frame = tk.Frame(home_frame, bg="white")
button_frame.pack(pady=15)

btn_new = tk.Button(button_frame, text="New", font=25, relief="flat", width=20, height=3)
btn_new.pack(side="left", padx=10)

btn_open = tk.Button(button_frame, text="Open", font=25, relief="flat", width=20, height=3)
btn_open.pack(side="left", padx=10)

btn_delete = tk.Button(button_frame, text="Delete", font=25, relief="flat", width=20, height=3)
btn_delete.pack(side="left", padx=10)

btn_export = tk.Button(button_frame, text="Export All Notes", font=25, relief="flat", width=20, height=3, command=export_notes_with_format)
btn_export.pack(side="left", padx=10)# Adjust as needed



pinnednote_lbl= tk.Label(home_frame, text="Pinned Note",bg="white",font=('Arial',25))
pinnednote_lbl.place(x=15,y=550)


#create a box for the pinned note
tree = ttk.Treeview(home_frame, columns=("Name",), show="headings", height=10)
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

remark_entry = tk.Entry(calendar_frame, font=("Arial", 14), width=50)
remark_entry.pack(pady=10)
save_btn = tk.Button(calendar_frame, text="Save Remark", command=save_remark_for_date, font=("Arial", 12))
save_btn.pack(pady=5)
cal.bind("<<CalendarSelected>>", display_remark_for_date)
load_remarks()




#todolist section
todolist_lbl= tk.Label(todolist_frame,text="To- Do-List",bg="white", font=('Arial',30))
todolist_lbl.place(x=0,y=0)


show_frame(home_frame)

root.mainloop()


