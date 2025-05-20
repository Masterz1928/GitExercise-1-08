import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from tkcalendar import Calendar
import os
from datetime import datetime
import zipfile


# ------------------- Theme Settings -------------------
WHITE_BG = "#fdfcfa"
PINK_BG = "#e6e6fa"
PINK_ACCENT = "#e6e6fa"
PINK_SELECTED = "#d8bfd8"
TEXT_COLOR = "#4b3869"
LOGO_COLOR = "#800080"

FONT_LOGO = ("Segoe UI", 14, "bold")
FONT_HEADING = ("Segoe UI", 18, "bold")
FONT_TEXT = ("Segoe UI", 11)

# ------------------- Global Paths and Variables -------------------

remarks={}
pinned_files = []
folder_path = "C:/Notes"
trash_folder = os.path.join(folder_path, "Trash")
os.makedirs(trash_folder, exist_ok=True)

# ------------------- Main Window -------------------
root = tk.Tk()
root.title("🎓 MMU Study Buddy")
root.geometry("900x600")
root.configure(bg=WHITE_BG)
root.minsize(700, 500)

# ------------------- Logo Bar -------------------
top_frame = tk.Frame(root, bg=WHITE_BG, height=60)
top_frame.pack(fill='x')

logo_label = tk.Label(top_frame,
                      text="🎓 MMU Study Buddy",
                      font=FONT_LOGO,
                      bg=WHITE_BG,
                      fg=LOGO_COLOR,
                      anchor='w')
logo_label.pack(side='left', padx=20, pady=10)
def open_drive_panel():
    drive_window = tk.Toplevel()
    drive_window.title("Drive Panel")
    drive_window.resizable(False, False)

    # Dimensions and position (top-right)
    window_width = 300
    window_height = 320
    screen_width = drive_window.winfo_screenwidth()
    screen_height = drive_window.winfo_screenheight()
    x_position = screen_width - window_width - 10
    y_position = 10
    drive_window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
    drive_window.configure(bg="#f0f0f0")

    # Button style
    button_style = {"font": ("Arial", 10, "bold"), "bg": "#4caf50", "fg": "white", "relief": "raised", "bd": 2}

    # Buttons
    tk.Button(drive_window, text="Download", **button_style).pack(pady=10, ipadx=10, ipady=5)
    tk.Button(drive_window, text="Upload", **button_style).pack(pady=10, ipadx=10, ipady=5)
    tk.Button(drive_window, text="Go to Drive", **button_style).pack(pady=10, ipadx=10, ipady=5)
    tk.Button(drive_window, text="Reload", **button_style).pack(pady=10, ipadx=10, ipady=5)
    tk.Button(drive_window, text="Log Out", bg="#f44336", fg="white", font=("Arial", 10, "bold"), relief="raised", bd=2).pack(pady=10, ipadx=10, ipady=5)


btn_drive = tk.Button(top_frame, text="Drive", command=open_drive_panel)
btn_drive.pack(side="right", padx=10)
# ------------------- Notebook Style -------------------
style = ttk.Style()
style.theme_use('default')
style.configure('TNotebook', background=WHITE_BG, borderwidth=0)
style.configure('TNotebook.Tab',
                background=PINK_ACCENT,
                foreground=TEXT_COLOR,
                padding=[20, 10],
                font=("Segoe UI", 10, "bold"),
                borderwidth=0)
style.map("TNotebook.Tab",
          background=[("selected", PINK_SELECTED)],
          expand=[("selected", [1, 1, 1, 0])])

# ------------------- Notebook Area -------------------
notebook_frame = tk.Frame(root, bg=WHITE_BG)
notebook_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

notebook = ttk.Notebook(notebook_frame)
notebook.pack(fill='both', expand=True)

# ------------------- Home Tab with Feature Cards -------------------
home = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(home, text="🏠 Home")


home_title = tk.Label(home,
                      text="💖 Welcome to MMU Study Buddy 💖",
                      font=FONT_HEADING,
                      bg=WHITE_BG,
                      fg=TEXT_COLOR)
home_title.pack(pady=20)

card_frame = tk.Frame(home, bg=WHITE_BG)
card_frame.pack(pady=10)

def create_feature_card(parent, icon, title, desc, tab_index):
    card = tk.Frame(parent, bg=PINK_ACCENT, bd=1, relief="flat", highlightthickness=2,
                    highlightbackground=PINK_SELECTED)
    card.bind("<Button-1>", lambda e: notebook.select(tab_index))

    def on_enter(e): card.config(bg=PINK_SELECTED)
    def on_leave(e): card.config(bg=PINK_ACCENT)

    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)

    icon_label = tk.Label(card, text=icon, font=("Segoe UI Emoji", 30), bg=PINK_ACCENT)
    icon_label.pack(pady=(10, 0))

    title_label = tk.Label(card, text=title, font=("Segoe UI", 13, "bold"), bg=PINK_ACCENT, fg=TEXT_COLOR)
    title_label.pack(pady=(5, 0))

    desc_label = tk.Label(card, text=desc, font=("Segoe UI", 10), bg=PINK_ACCENT, fg=TEXT_COLOR, wraplength=180,
                          justify="center")
    desc_label.pack(pady=(5, 10))

    return card


# Placeholder tabs for Timer and To-Do for now
timer_tab = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(timer_tab, text="⏲ Timer")

todo_tab = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(todo_tab, text="✅ To-Do List")
# ------------------- Notes Functions -------------------

def update_file_list():
    file_listbox.delete(0, tk.END)
    files = [f for f in os.listdir(folder_path) if f.endswith((".txt", ".md", ".html"))]
    for file in files:
        file_listbox.insert(tk.END, file)

def search_notes():
    search_term = search_entry.get().lower()
    file_listbox.delete(0, tk.END)
    files = [f for f in os.listdir(folder_path) if f.endswith((".txt", ".md", ".html"))]
    for file in files:
        if search_term in file.lower():
            file_listbox.insert(tk.END, file)

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

def export_all_notes():
    export_path = "all_notes_export.txt"
    with open(export_path, "w", encoding="utf-8") as export_file:
        files = [f for f in os.listdir(folder_path) if f.endswith((".txt",".html",".md"))]
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
    files = [f for f in os.listdir(folder_path) if f.endswith((".txt", ".html", ".md"))]
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
    with open("pinned_notes.txt", "w") as f:
        for item in tree.get_children():
            filename = tree.item(item, "values")[0]
            f.write(f"{filename}\n")


def load_pinned_notes():
    if os.path.exists("pinned_notes.txt"):
        with open("pinned_notes.txt", "r") as f:
            for line in f:
                note = line.strip()
                pinned_files.append(note)
                tree.insert("", tk.END, values=(note,))


def deleting_notes():
    selected_files = file_listbox.curselection()
    if not selected_files:
        messagebox.showwarning("No selection", "Select a file to delete.")
        return
    file_delete_name = file_listbox.get(selected_files[0])
    confirm = messagebox.askyesno("Delete?", f"Move '{file_delete_name}' to Trash?")
    if confirm:
        original_path = os.path.join(folder_path, file_delete_name)
        trash_path = os.path.join(trash_folder, file_delete_name)
        os.rename(original_path, trash_path)
        update_file_list()
        messagebox.showinfo("Deleted", f"'{file_delete_name}' moved to Trash.")

def open_trash_bin():
    trash_win = tk.Toplevel(root)
    trash_win.title("Trash Bin")
    trash_win.geometry("500x400")

    tk.Label(trash_win, text="Deleted Notes", font=("Arial", 16)).pack(pady=10)

    trash_listbox = tk.Listbox(trash_win, width=60, height=15)
    trash_listbox.pack(pady=10)

    deleted_files = os.listdir(trash_folder)
    for file in deleted_files:
        trash_listbox.insert(tk.END, file)

    def restore_file():
        selected = trash_listbox.curselection()
        if not selected:
            messagebox.showinfo("Restore", "Please select a file.")
            return
        filename = trash_listbox.get(selected[0])
        from_path = os.path.join(trash_folder, filename)
        to_path = os.path.join(folder_path, filename)
        if os.path.exists(to_path):
            messagebox.showerror("Restore Failed", f"A file named '{filename}' already exists.")
            return
        os.rename(from_path, to_path)
        trash_listbox.delete(selected[0])
        update_file_list()
        messagebox.showinfo("Restored", f"'{filename}' has been restored.")

    def delete_all_files():
        confirm = messagebox.askyesno("Delete All", "Are you sure you want to permanently delete all files in the Trash Bin?")
        if confirm:
            for f in os.listdir(trash_folder):
                os.remove(os.path.join(trash_folder, f))
            trash_listbox.delete(0, tk.END)
            messagebox.showinfo("Deleted", "All files permanently deleted")

    btn_restore = ttk.Button(trash_win, text="Restore Selected", command=restore_file)
    btn_restore.pack(side='left', padx=(100,20), pady=10)

    btn_delete_all = ttk.Button(trash_win, text="Clear", command=delete_all_files)
    btn_delete_all.pack(side='right', padx=(20,100), pady=10)
# ------------------- Notes Tab -------------------
notes_tab = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(notes_tab, text="📝 Notes")

# Search bar
search_entry = tk.Entry(notes_tab, font=FONT_TEXT)
search_entry.place(relx=0.1, rely=0.05, relwidth=0.5)
search_entry.bind("<Return>", lambda event: perform_advanced_search())

clear_search_button = ttk.Button(notes_tab, text="Clear Search", command=lambda: [search_entry.delete(0, tk.END), update_file_list()])
clear_search_button.place(relx=0.62, rely=0.05, relwidth=0.15)

btn_trash = ttk.Button(notes_tab, text="Trash Bin", command=lambda: open_trash_bin())
btn_trash.place(relx=0.8, rely=0.05, relwidth=0.15)

search_entry.bind("<KeyRelease>", lambda e: search_notes())

# Listbox for files
file_listbox = tk.Listbox(notes_tab, font=FONT_TEXT)
file_listbox.place(relx=0.05, rely=0.12, relwidth=0.4, relheight=0.8)

# Button Frame
note_btn_frame = tk.Frame(notes_tab, bg=WHITE_BG)
note_btn_frame.place(relx=0.05, rely=0.01, relwidth=0.9)



# Pinned notes treeview
tree = ttk.Treeview(notes_tab, columns=("Pinned Notes",), show="headings")
tree.heading("Pinned Notes", text="Pinned Notes")
tree.place(relx=0.55, rely=0.12, relwidth=0.4, relheight=0.8)
load_pinned_notes()

file_listbox.bind("<Button-3>", show_listbox_menu)
tree.bind("<Button-3>", show_tree_menu)
btn_new = ttk.Button(note_btn_frame, text="New Note")
btn_new.pack(side='left', padx=5)

btn_open = ttk.Button(note_btn_frame, text="Open Note")
btn_open.pack(side='left', padx=5)

btn_delete = ttk.Button(note_btn_frame, text="Delete Note", command=lambda: deleting_notes())
btn_delete.pack(side='left', padx=5)

btn_export = ttk.Button(note_btn_frame, text="Export Notes", command=lambda: export_all_notes())
btn_export.pack(side='left', padx=5)

listbox_menu = tk.Menu(card_frame, tearoff=0)# tear off is the dash line in the menu list
listbox_menu.add_command(label="Pin", command=lambda: pin_selected_note())
listbox_menu.add_command(label="Unpin", command=lambda: unpin_selected_note())

tree_menu = tk.Menu(card_frame, tearoff=0)
tree_menu.add_command(label="Unpin", command=lambda: unpin_from_tree())

def on_closing():
    save_pinned_notes()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

#calanedr section
calendar_tab = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(calendar_tab, text="📅 Calendar")

# Bigger calendar
cal = Calendar(calendar_tab, selectmode='day', date_pattern='yyyy-mm-dd',
               font=("Arial", 14))  # Larger font
cal.pack(pady=20, ipadx=10, ipady=10)  # Increased padding

# Multiline remark input
remark_text = tk.Text(calendar_tab, width=50, height=6, font=("Arial", 12))
remark_text.pack(pady=10)

# Theme function
def choose_calendar_color():
    color = colorchooser.askcolor(title="Choose Calendar Color")[1]
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
            background="#FFE4E1",
            headersbackground="#FFB6C1",
            disabledbackground="#FFE4E1",
            normalbackground="#FFE4E1",
            weekendbackground="#FFD1DC",
            selectbackground="#FF69B4",
            selectforeground="white",
        )
    elif choice == "Blue":
        cal.config(
            background="#E0FFFF",
            headersbackground="#87CEFA",
            disabledbackground="#E0FFFF",
            normalbackground="#E0FFFF",
            weekendbackground="#ADD8E6",
            selectbackground="#00BFFF",
            selectforeground="white",
        )
    elif choice == "Purple":
        cal.config(
            background="#E6E6FA",
            headersbackground="#D8BFD8",
            disabledbackground="#E6E6FA",
            normalbackground="#E6E6FA",
            weekendbackground="#D8BFD8",
            selectbackground="#9370DB",
            selectforeground="white",
        )

# Save/load remarks
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

# Save remark for selected date
def save_remark_for_date():
    selected_date = cal.get_date()
    remark = remark_text.get("1.0", tk.END).strip()
    if remark:
        remarks[selected_date] = remark
        save_remarks()
        messagebox.showinfo("Saved", f"Remark for {selected_date} saved.")
    else:
        messagebox.showwarning("Empty", "Please enter a remark.")

# Display saved remark for selected date
def display_remark_for_date(event=None):
    selected_date = cal.get_date()
    remark_text.delete("1.0", tk.END)
    if selected_date in remarks:
        remark_text.insert("1.0", remarks[selected_date])

# Theme dropdown
theme_var = tk.StringVar()
theme_var.set("Choose Theme")
theme_options = ["Pink", "Blue", "Purple", "Custom"]
theme_menu = tk.OptionMenu(calendar_tab, theme_var, *theme_options, command=apply_theme)
theme_menu.config(font=("Arial", 12), bg="#f0f0f0")
theme_menu.pack(pady=10)

# Save button
save_btn = tk.Button(calendar_tab, text="Save Remark", command=save_remark_for_date, font=("Arial", 12))
save_btn.pack(pady=5)

# Bind calendar selection to display remark
cal.bind("<<CalendarSelected>>", display_remark_for_date)

# Load saved remarks on startup
load_remarks()
card1 = create_feature_card(card_frame, "⏲", "Timer", "Start/stop Pomodoro or normal timer.", 1)
card2 = create_feature_card(card_frame, "✅", "To-Do List", "Manage your daily tasks efficiently.", 2)
card3 = create_feature_card(card_frame, "📝", "Notes", "Create, search, pin, and manage notes.", 3)
card4 = create_feature_card(card_frame, "📅", "Calendar", "Add remarks to calendar dates.", 4)

card1.grid(row=0, column=0, padx=15, pady=15)
card2.grid(row=0, column=1, padx=15, pady=15)
card3.grid(row=0, column=2, padx=15, pady=15)
card4.grid(row=0, column=3, padx=15, pady=15)


update_file_list()

root.mainloop()