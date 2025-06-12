import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk,messagebox,colorchooser, filedialog, StringVar
import zipfile
from tkhtmlview import HTMLLabel
import markdown
import re
from bs4 import BeautifulSoup
import os
from pathlib import Path
from datetime import date, datetime, timedelta, timezone
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from tkinter import ttk, messagebox
import tkinter as tk
import threading 
from dateutil import parser
import pygame
from plyer import notification
import time
import sys


def on_exit():
    root.destroy()
    sys.exit()  # Ensure the Python process ends


pygame.mixer.init()

global folder_path
folder_name = "Notes"
folder_path = Path.home() / folder_name

try:
    os.makedirs(folder_path, exist_ok=True)
    print(f"Folder '{folder_path}' created successfully!")
except Exception as e:
    print(f"An error occurred: {e}")

def get_token_path():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)  # if running as .exe
    else:
        base_path = os.path.dirname(__file__)        # if running as .py

    return os.path.join(base_path, 'token.json')

def get_cred_path():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, "credentials.json")



def run_notepad(file_content=""):
    global Text_Box
    NotepadWindow = tk.Toplevel() 
    NotepadWindow.title("Note Editor")
    NotepadWindow.config(bg="#a8a8a9")
    NotepadWindow.minsize(width=800, height=700)
    screen_width = NotepadWindow.winfo_screenwidth()
    screen_height = NotepadWindow.winfo_screenheight()

    # Optional padding to not use full screen
    app_width = int(screen_width * 0.95)
    app_height = int(screen_height * 0.95)

    NotepadWindow.geometry(f"{app_width}x{app_height}")
    #Set variable for the file name to False, when first starting the program
    global open_status_name 
    open_status_name = False

    #Set variable for the Cut Content to False, when first starting the program
    global selected_text_by_user 
    selected_text_by_user = False

    #Set another global variable for saving the file and switching modes
    Current_File_Mode = "Markdown"

    #Creating Functions Here
    # Creating New File 
    def New_File():
        #Clearing text box
        Text_Box.delete("1.0", tk.END)
        # Adding in a title 
        NotepadWindow.title("New Note")
        change_to_markdown()
        #Adding status bar for display
        Status_bar.config(text="New File    ")
        global open_status_name 
        open_status_name = False

    # Creating a opening function
    def Opening():
        #Clearing text box
        global Current_File_Mode, text_file
        Text_Box.delete("1.0", tk.END)
        #Grab The file name

        if not text_file:
            text_file = filedialog.askopenfilename(
                initialdir=str(folder_path),
                title="Open a File",
                filetypes=(
                    ("Text Files", "*.txt"),
                    ("HTML Files", "*.html"),
                    ("Markdown Files", "*.md"),
                    ("All Files", "*.*")
                )
            )
            if not text_file:
                return  # User cancelled, stop here
        
        Window_title = text_file
        #Check if there is a file name and if yes, make it global
        if text_file:
            global open_status_name 
            open_status_name = text_file
            File_extension  =  os.path.splitext(text_file)[1].lower()
            if File_extension == ".md":
                Current_File_Mode = "Markdown"
                print("markdown")
                change_to_markdown()
            elif File_extension in [".html", ".htm"]:
                Current_File_Mode = "HTML"
                print("html")
                change_to_html()
            elif File_extension == ".txt":
                Current_File_Mode = "Text"
                print("txt")
                change_to_text()
            else:
                # Default to text if unknown type
                print("This is changing it to MD is seems ")
                change_to_markdown()
        #Updating Status bar 
        name = text_file
        Status_bar.config(text=f"{name}    ")
        NotepadWindow.title(f"{Window_title} - Note Editor")

        # Load File Content
        text_file = open(text_file, "r")
        File_Content = text_file.read()
        #Add it into the text box
        Text_Box.insert(tk.END, File_Content)
        #Then, Close the open file
        text_file.close()

        
    # Creating a function to save a file as (in a .txt format) 
    def Saving_File_As():
        global open_status_name 
        if Current_File_Mode == "Text":
            file_extention ="*.txt"
            filetypestosave = [("Text Files", "*.txt"), ("All Files", "*.*")]

        if Current_File_Mode == "HTML":
            file_extention ="*.html"
            filetypestosave = [("HTML Files", "*.html"), ("All Files", "*.*")]

        if Current_File_Mode == "Markdown":
            file_extention ="*.md"
            filetypestosave = [("Markdown Files", "*.md"), ("All Files", "*.*")]
            
        text_file = filedialog.asksaveasfilename(defaultextension=file_extention, initialdir=str(folder_path), title="Save File As", filetypes=filetypestosave)
        if text_file:
            open_status_name = text_file
            #Update the status bar
            name = text_file
            Status_bar.config(text=f"Saved: {name}    ")
      

            # Save the file 
            text_file = open(text_file, "w")
            text_file.write(Text_Box.get(1.0, tk.END))
            #close the file 
            text_file.close()

    # Creating a function to save file (to update the contents of the file tbh)
    def Saving_File():
        global open_status_name
        if open_status_name:
            # Save the file 
            text_file = open(open_status_name, "w")
            text_file.write(Text_Box.get(1.0, tk.END))
            #close the file 
            text_file.close()
            # Prompting user with a message box
            Message_Pop = messagebox.showinfo(title="Saving File", message="Your file has been saved!")
            Status_bar.config(text=f"Saved: {open_status_name}    ")
        else:
            Saving_File_As()

    def insert_markdown(tag):
        ZWSP = "\u200b"  # Invisible separator character

        try:
            selected = Text_Box.get(tk.SEL_FIRST, tk.SEL_LAST)
            start = Text_Box.index(tk.SEL_FIRST)
            end = Text_Box.index(tk.SEL_LAST)

            # Pause undo stack to avoid intermediate steps
            Text_Box.edit_separator()  # Mark undo boundary before the change (Checkpoint for the programm to undo)

            if tag in ["**", "*"]:  # Bold or italic
                Text_Box.replace(start, end, f"{tag}{selected}{tag}{ZWSP}")
                update_preview()
            elif tag == "<u></u>":
                Text_Box.replace(start, end, f"<u>{selected}</u>{ZWSP}")
                update_preview()
            elif tag == "font-size":
                size = font_choice.get()
                Text_Box.replace(start, end, f'<span style="font-size:{size}px">{selected}</span>{ZWSP}')
                update_preview()

            Text_Box.edit_separator()  # Mark undo boundary after the change (New checkpoint for the programm to undo)

        except tk.TclError:
            pass


    def change_to_html():
        global Current_File_Mode
        Current_File_Mode = "HTML"
        print("called change to html")
        File_Settings_Menu.entryconfig("Change to Text File", background="white")  # Color for active mode
        File_Settings_Menu.entryconfig("Change to HTML", background="lightblue")  # Reset others
        File_Settings_Menu.entryconfig("Change to Markdown", background="white")
        bold_btn.config(state=tk.DISABLED)
        italic_btn.config(state=tk.DISABLED)
        underline_btn.config(state=tk.DISABLED)
        font_size_menu.config(state=tk.DISABLED)
        
        

    def change_to_text():
        global Current_File_Mode
        Current_File_Mode = "Text"
        print("called change to txt")
        File_Settings_Menu.entryconfig("Change to Text File", background="lightblue")  # Color for active mode
        File_Settings_Menu.entryconfig("Change to HTML", background="white")  # Reset others
        File_Settings_Menu.entryconfig("Change to Markdown", background="white")
        bold_btn.config(state=tk.DISABLED)
        italic_btn.config(state=tk.DISABLED)
        underline_btn.config(state=tk.DISABLED)
        font_size_menu.config(state=tk.DISABLED)

    def change_to_markdown():
        global Current_File_Mode
        Current_File_Mode = "Markdown"
        print("called change to md")
        File_Settings_Menu.entryconfig("Change to Text File", background="white")  # Color for active mode
        File_Settings_Menu.entryconfig("Change to HTML", background="white")  # Reset others
        File_Settings_Menu.entryconfig("Change to Markdown", background="lightblue")
        bold_btn.config(state=tk.NORMAL)
        italic_btn.config(state=tk.NORMAL)
        underline_btn.config(state=tk.NORMAL)
        font_size_menu.config(state=tk.NORMAL)

    # Creating a function for cut function
    def cut_text(e=None):
        global selected_text_by_user
        if e:
            selected_text_by_user = NotepadWindow.clipboard_get()
        else:
            if Text_Box.selection_get():
                # put into a variable
                selected_text_by_user = Text_Box.selection_get()
                # Delete the selected text
                Text_Box.delete("sel.first" ,"sel.last")
                #Clear clipboard, then put new infomation
                NotepadWindow.clipboard_clear()
                NotepadWindow.clipboard_append(selected_text_by_user)


    # Creating a function for copy function
    def copy_text(e=None):
        global selected_text_by_user
        # Check to see if we used keyboard shortcuts
        if e:
            selected_text_by_user = NotepadWindow.clipboard_get()

        if Text_Box.selection_get():
            selected_text_by_user = Text_Box.selection_get()
            #Clear clipboard, then put new infomation
            NotepadWindow.clipboard_clear()
            NotepadWindow.clipboard_append(selected_text_by_user)


    # Creating a function for paste function
    def paste_text(e=None):
        global selected_text_by_user

        #check to see if there are any keybaord shortcut
        if e:
            selected_text_by_user = NotepadWindow.clipboard_get()
        else:
            if selected_text_by_user:
                Position = Text_Box.index(tk.INSERT)
                Text_Box.insert(Position, selected_text_by_user) 


    def count_words():
        text = Text_Box.get("1.0", tk.END)  # Get all the text
        words = text.split()
        word_count = len(words) # Gets the number of words 
        
        lines = text.split('\n')
        line_count = len(lines) - 1  # Subtract 1 because of the extra newline at the end
        
        char_count = len(text) - 1  # Subtract 1 to exclude the final newline character

        word_count_label.config(
            text=f"Words: {word_count} | Lines: {line_count} | Characters: {char_count}"
        )

    def on_release(event):
        sync_preview_scroll(event)
        count_words()

    def help_guide(event=None):
        help_win = tk.Toplevel()  # create a Toplevel window
        help_win.title("Notepad Help")
        help_win.geometry("400x300")

        # Custom style for active tab
        style = ttk.Style(help_win)

        style.map("TNotebook.Tab",
                background=[("selected", "lightblue")])  # Active tab color

        notebook = ttk.Notebook(help_win)  # tab manager widget
        notebook.pack(fill="both", expand=True)  # fill the whole window

        # Tab 1: File Settings
        tab1 = ttk.Frame(notebook)  # Create a frame to act as the first tab
        notebook.add(tab1, text="File Settings")  # Adds it to the notebook with "File Settings"
        
        # Create the label
        Tab1Text = tk.Label(tab1, text=(
            "1) Markdown - All features are available.\n"
            "2) HTML - Use HTML tags, no Markdown.\n"
            "3) Text - Regular text files."
        ), justify="left", padx=10, pady=10)
        
        # Set the font size
        Tab1Text.config(font=("Segoe UI", 15))  # Apply font before packing
        # Pack the label
        Tab1Text.pack(anchor="w")

        # Tab 2: Shortcuts
        tab2 = ttk.Frame(notebook) 
        notebook.add(tab2, text="Shortcuts")
        
        Tab2Text = tk.Label(tab2, text=(
            "Ctrl+B - Bold\n"
            "Ctrl+P - Italic \n"
            "Ctrl+U - Underline\n"
            "Ctrl+S - Save\n"
            "Ctrl+O - Open"
        ), justify="left", padx=10, pady=10)
        
        # Set the font size
        Tab2Text.config(font=("Segoe UI", 15))  # Apply font before packing
        # Pack the label
        Tab2Text.pack(anchor="w")

        # Tab 3: Preview Info
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Preview")
        
        Tab3Text = tk.Label(tab3, text=(
            "• Preview updates automatically on after typing.\n"
            "• Supports Markdown and HTML preview.\n"
            "• Some advanced tags may not render fully."
        ), justify="left", padx=10, pady=10)
        
        # Set the font size
        Tab3Text.config(font=("Segoe UI", 15))  # Apply font before packing
        # Pack the label
        Tab3Text.pack(anchor="w")

    # Toolbar Frame (Putting this first so that its top)
    ToolFrame = tk.Frame(NotepadWindow, bg="#a8a8a8", highlightbackground="black", highlightthickness=1, border=15)
    ToolFrame.pack(fill="x", side="top")


    # Create main frame
    # (Putting the Text typing area and the scroll bar in the same area)
    # Main container frame
    MainFrame = tk.Frame(NotepadWindow)
    MainFrame.config(bg="white")
    MainFrame.pack(pady=0, padx=5, fill="both", expand=True)

    # 2 equal columns
    MainFrame.rowconfigure(0, weight=1)

    MainFrame.columnconfigure(0, weight=1)
    MainFrame.columnconfigure(1, weight=1)

    # Text Frame + Scrollbar
    text_frame = tk.Frame(MainFrame, bg="white",)
    text_frame.grid(row=0, column=0, sticky="nsew")

    text_scroll = ttk.Scrollbar(text_frame)
    text_scroll.pack(side="right", fill="y")

    Text_Box = tk.Text(text_frame, font=("Helvetica", 16),selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="word", bd=2, relief="solid")
    Text_Box.pack(pady=20, padx=20, fill="both", expand=True)

    text_scroll.config(command=Text_Box.yview)


    # Create a style object
    style = ttk.Style()

    # Define custom styles for bold, italic, and underline
    style.configure('Bold.TButton', font=('Helvetica', 10, 'bold'), padding=(5, 5), background="black")
    style.configure('Italic.TButton', font=('Helvetica', 10, 'italic'), padding=(5, 5), background="black")
    style.configure('Underline.TButton', font=('Helvetica', 10, 'underline'), padding=(5, 5), background="black")
    style.configure('Undo.TButton', font=('Helvetica', 10), padding=(5, 5), background="black")
    style.configure('Cut.TButton', font=('Helvetica', 10), padding=(5, 5), background="black")
    style.configure('Copy.TButton', font=('Helvetica', 10), padding=(5, 5), background="black")
    style.configure('Redo.TButton', font=('Helvetica', 10), padding=(5, 5), background="black")
    style.configure('Paste.TButton', font=('Helvetica', 10), padding=(5, 5), background="black")
    style.configure('help.TButton', font=('Helvetica', 10), padding=(5, 5), background="black")

    left_wrap = ttk.Frame(ToolFrame)
    left_wrap.pack(side="left", padx=(20, 0))  # only push from left

    bold_btn = ttk.Button(ToolFrame, text="B", style="Bold.TButton", width=5, command=lambda: insert_markdown("**"))
    bold_btn.pack(side="left", padx=10, pady=10)

    italic_btn = ttk.Button(ToolFrame, text="I", style="Italic.TButton", width=5, command=lambda: insert_markdown("*"))
    italic_btn.pack(side="left", padx=10, pady=10)

    underline_btn = ttk.Button(ToolFrame, text="U", style="Underline.TButton", width=5, command=lambda: insert_markdown("<u></u>"))
    underline_btn.pack(side="left", padx=10, pady=10)

    undo_button = ttk.Button(ToolFrame, text="Undo", style="Undo.TButton", width=5, command=Text_Box.edit_undo)
    undo_button.pack(side="left", padx=10, pady=10)

    redo_button = ttk.Button(ToolFrame, text="Redo", style="Redo.TButton", width=5,  command=Text_Box.edit_redo)
    redo_button.pack(side="left", padx=10, pady=10)

    cut_button = ttk.Button(ToolFrame, text="Cut", style="Cut.TButton", width=5, command=cut_text)
    cut_button.pack(side="left", padx=10, pady=10)

    copy_button = ttk.Button(ToolFrame, text="Copy" , style="Copy.TButton", width=5, command=copy_text)
    copy_button.pack(side="left", padx=10, pady=10)

    paste_button = ttk.Button(ToolFrame, text="Paste", style="Paste.TButton", width=5, command=paste_text)
    paste_button.pack(side="left", padx=10, pady=10)

    help_button = ttk.Button(ToolFrame, text="Help", style="help.TButton", width=5, command=help_guide)
    help_button.pack(side="left", padx=10, pady=10)


    def update_preview(event=None):
        markdown_text = Text_Box.get("1.0", tk.END)

        lines = markdown_text.splitlines()
        safe_lines = []
        skipping = False

        for line in lines:
            if re.search(r'<\w+\s+style=.*?>', line) and not re.search(r'</\w+>', line):
                skipping = True
                continue

            if skipping:
                if re.search(r'</\w+>', line):
                    skipping = False
                continue

            safe_lines.append(line)

        filtered_text = "\n".join(safe_lines)

        if Current_File_Mode == "Markdown":
            try:
                #to convert markdown into html for display
                html_content = markdown.markdown(filtered_text, extensions=["nl2br"]) #New line to break
                # General knowledge - Parse - analyzes and interprets strings of data, breaking them down into meaningful parts according to a specific set of rules or grammar
                # We use soup to to inspect the HTML, not to drink 
                soup = BeautifulSoup(html_content, "html.parser")
                # Make a list of the halal styles that we aallow the program to use  
                # Adding in an if statement that filters out tags depending on the program's mode  
                if Current_File_Mode == "Markdown":
                    ALLOWED_STYLES = ["font-size", "color"]
                elif Current_File_Mode == "html":
                    ALLOWED_STYLES = ["font-size", "color", "background", "border", "margin", "padding"]
                else:
                    ALLOWED_STYLES = []  # for pure text, no styles at all
                    for tag in soup.find_all(True):
                        tag.unwrap() # Removes tags, keep content
                #Find all the tags in the program 
                for tag in soup.find_all(True):
                    # check if style attribute is present 
                    if "style" in tag.attrs:
                        # split the string into individual parts
                        # example
                        #tag[style] does --> "font-size:12px; color:red; background:black;"
                        # the split thing does --> ["font-size:12px", "color:red", "background:black"]
                        styles = tag["style"].split(";")
                        clean_styles = []
                        # now we loop in the styles we have gotten 
                        for s in styles:
                            # remove whitespaces 
                            s = s.strip()
                            #Check is the sstyle is halal or haram 
                            for allowed in ALLOWED_STYLES:
                                # if halal ?
                                if s.startswith(allowed):
                                    # we keep it 
                                    clean_styles.append(s)
                        # if there any suitable tags remaining, then we rebuild it together with the ";"
                        if clean_styles:
                            tag["style"] = "; ".join(clean_styles)
                        #Otherwise remove it completely 
                        else:
                            del tag["style"]
                        
                # Convert Soup to String
                final_html = str(soup)
                #update the html Preview 
                html_preview.set_html(final_html)
        
            #Catch any errors then print it out 
            except Exception as e:
                print(f"Error generating HTML preview: {e}")

        
        elif Current_File_Mode == "HTML":
            # For HTML mode, we don't convert, just send raw HTML to the preview widget
            html_preview.set_html(markdown_text)  # Directly display HTML content in preview


    # Bind the function to key release in the Text_Box
    Text_Box.bind("<KeyRelease>", update_preview)

    # Function to allow the scroll of both window to be the same 
    def sync_scroll(event):
        # Get the scroll position of the Text Box
        text_scroll = Text_Box.yview()
        # Set the same scroll position to the preview
        html_preview.yview_moveto(text_scroll[0])
    # Bind the Text Box vertical scroll event 
    Text_Box.bind('<MouseWheel>', sync_scroll)

    #Avoid the Preview from jumping around when typing 
    def sync_preview_scroll(event):
        # Get the current vertical position of the preview
        preview_scroll_position = html_preview.yview()[0]
        # Update the preview with the new content
        update_preview() 
        # reset the scroll position
        html_preview.yview_moveto(preview_scroll_position)
    # Use this function o update the preview as you type
    Text_Box.bind('<KeyRelease>',on_release)

    # Change the column weight for the preview frame to limit its space usage
    MainFrame.columnconfigure(1, weight=0, minsize=250)  # Reduced weight and set a minimum size for the preview frame

    # Preview Frame
    preview_frame = tk.Frame(MainFrame, bd=2, relief="solid")
    preview_frame.config(bg="white")
    preview_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=20)

    html_preview = HTMLLabel(preview_frame, html="")
    html_preview.config(bg="white")
    html_preview.pack(pady=10, padx=10, ipadx=43, fill="both", expand=True)  # Adjust padding and prevent it from expanding

    #Creating Menu Top menu bar
    TopMenuBar = tk.Menu(NotepadWindow)
    NotepadWindow.config(menu=TopMenuBar)

    # Set up OptionMenu for font size
    font_choice = tk.StringVar()
    font_choice.set("12")  # Set default value to string
    font_size_options = [str(size) for size in range(12, 42, 2)]

    font_size_menu = ttk.OptionMenu(ToolFrame, font_choice, *font_size_options)
    font_size_menu.pack(side="left", padx="10", pady="5")


    def change_font_size(*args):
        insert_markdown("font-size")

    # Bind the function to handle changes in selection
    font_choice.trace("w", change_font_size)

    #Adding in File Menu into the Menu Bar
    file_menu = tk.Menu(TopMenuBar, tearoff=False)
    TopMenuBar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=New_File)
    file_menu.add_command(label="Open", command=Opening)
    file_menu.add_command(label="Save", command=Saving_File)
    file_menu.add_command(label="Save as", command=Saving_File_As)

    #Adding editing menu 
    edit_menu = tk.Menu(TopMenuBar, tearoff=False)
    TopMenuBar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut    Ctrl+X", command=lambda: cut_text(False))
    edit_menu.add_command(label="Copy   Ctrl+C", command=lambda: copy_text(False))
    edit_menu.add_command(label="Paste  Ctrl+V", command=lambda: paste_text(False))
    edit_menu.add_command(label="Undo  Ctrl+z", command=Text_Box.edit_undo)
    edit_menu.add_command(label="Redo  Ctrl+r", command=Text_Box.edit_redo)

    #Adding File setting Menu 
    File_Settings_Menu = tk.Menu(TopMenuBar, tearoff=False)
    TopMenuBar.add_cascade(label="File Settings", menu=File_Settings_Menu)
    File_Settings_Menu.add_command(label="Change to Markdown", command=change_to_markdown, background="lightblue")
    File_Settings_Menu.add_command(label="Change to HTML", command=change_to_html, background="white")
    File_Settings_Menu.add_command(label="Change to Text File", command=change_to_text, background="white")

    #Adding a status bar (For referance)
    Status_bar = tk.Label(NotepadWindow, text="Ready    ", anchor="e", bg="#a8a8a8")
    Status_bar.pack(side="right", ipady=5)

    word_count_label = tk.Label(NotepadWindow,text=f"Words: 0 | Lines: 0 | Characters: 0")
    word_count_label.config(bg="#a8a8a8")
    word_count_label.pack(side="left", ipady=5)


    # Adding in basic Binding
    NotepadWindow.bind("<Control-Key-x>", selected_text_by_user)
    NotepadWindow.bind("<Control-Key-c>", copy_text)
    NotepadWindow.bind("<Control-Key-v>", paste_text)
    NotepadWindow.bind("<Control-b>", lambda event: insert_markdown("**"))
    NotepadWindow.bind("<Control-p>", lambda event: insert_markdown("*"))
    NotepadWindow.bind("<Control-u>", lambda event: insert_markdown("<u></u>"))
    NotepadWindow.bind("<F1>", help_guide)


    NotepadWindow.Opening = Opening
    return NotepadWindow       


def open_note_in_notepad(file_path):
    global open_status_name, FileModeToSet, text_file
    text_file = file_path
    notepad_window = run_notepad()  # create window and get instance
    notepad_window.Opening()  # call inner function via window

# Example button click to open a file
def open_file_button_clicked():
    selected_file = file_listbox.curselection()  # Get the selected file in the Listbox
    if selected_file:
        file_name = file_listbox.get(selected_file[0])  # Get file name from listbox
        file_path = os.path.join(folder_path, file_name)  # Combine folder and file name to get full path
        file_path = os.path.abspath(file_path)  # Get absolute path to avoid issues
        open_note_in_notepad(file_path)

# color settings of the default
WHITE_BG       = "#fdfcfa"
BLUE_BG        = "#e8f0fe"
BLUE_ACCENT    = "#cfe2ff"
BLUE_SELECTED  = "#a7c7e7"
TEXT_COLOR     = "#2c3e50"
LOGO_COLOR     = "#1f4e79"

FONT_LOGO = ("Segoe UI", 14, "bold")
FONT_HEADING = ("Segoe UI", 18, "bold")
FONT_TEXT = ("Segoe UI", 11)



# all the path and source
remarks={}
pinned_files = []
trash_folder = os.path.join(folder_path, "Trash")
remark_path=os.path.join(folder_path,"Remark")
pinned_path=os.path.join(folder_path,"pinned note")
remark_file=os.path.join(remark_path, "remarks.txt")
pinned_file = os.path.join(pinned_path, "ImportantNote.txt")

#make sure that the directory is always occur , if disappear , it will create a new
os.makedirs(trash_folder, exist_ok=True)
os.makedirs(remark_path, exist_ok=True)
os.makedirs(pinned_path, exist_ok=True)
#main page code
root = tk.Tk()
root.title("MMU Study Buddy")
root.geometry("900x600")
root.configure(bg=WHITE_BG)
root.minsize(700, 500)
root.protocol("WM_DELETE_WINDOW", on_exit)


def get_icon_path():
    if getattr(sys, 'frozen', False):
        # .exe version
        return os.path.join(sys._MEIPASS, "025.ico")
    else:
        # .py version
        return os.path.join(os.path.dirname(__file__), "025.ico")

icon_path = get_icon_path()
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)  # <-- Use this for .ico files
else:
    print("Icon file not found.")


top_frame = tk.Frame(root, bg=BLUE_BG, height=60)  # Use new blue background
top_frame.pack(fill='x')

logo_label = tk.Label(top_frame,
                      text="📘 MMU Study Buddy",  
                      font=FONT_LOGO,
                      bg=BLUE_BG,
                      fg=LOGO_COLOR,         
                      anchor='w')
logo_label.pack(side='left', padx=20, pady=10)

#notebook tab style
style = ttk.Style()
style.configure('TNotebook', background=WHITE_BG, borderwidth=0)
style.configure('TNotebook.Tab',
                background=BLUE_ACCENT,
                foreground=TEXT_COLOR,
                padding=[20, 10],
                font=("Segoe UI", 10, "bold"),
                borderwidth=0)
style.map("TNotebook.Tab",
          background=[("selected", BLUE_SELECTED)],
          expand=[("selected", [1, 1, 1, 0])])

#notebook area
notebook_frame = tk.Frame(root, bg=WHITE_BG)
notebook_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20))

notebook = ttk.Notebook(notebook_frame)  #notebook style design
notebook.pack(fill='both', expand=True)

#home tab with feature card
home = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(home, text="🏠 Home")


home_title = tk.Label(home,
                      text="🌟 Welcome to Your MMU Study Buddy! 🌟",
                      font=FONT_HEADING,
                      bg=WHITE_BG,
                      fg=TEXT_COLOR)
home_title.pack(pady=20)

def check_reminders_on_startup():
    now = datetime.now()
    due_reminders = []

    for date_str, remark in remarks.items():
        try:
            reminder_time = datetime.strptime(date_str, "%Y-%m-%d") #just make sure all remark saved run with the true format 
        except ValueError:
            print(f"Invalid date format: {date_str}")
            continue
        
        if now <= reminder_time :
            due_reminders.append(f"{date_str} → {remark}")

    if due_reminders:
        message = "\n\n".join(due_reminders)
        messagebox.showinfo("Due Reminders", message)

def get_greeting():
    current_hour = datetime.now().hour   # the greeting word will change with the time 
    if 5 <= current_hour < 12:
        return "🌞 Good Morning!"
    elif 12 <= current_hour < 18:
        return "🌤️ Good Afternoon!"
    elif 18 <= current_hour < 21:
        return "🌆 Good Evening!"
    else:
        return "🌙 Good Night!"


def fade_in(widget, delay=250, steps=10):
    colors = [
        "#CCCCCC", "#BBBBBB", "#AAAAAA", "#999999", "#888888",
        "#777777", "#666666", "#444444", "#222222", "#000000"
    ]

    def step(i=0):
        if i < len(colors):
            widget.configure(foreground=colors[i])
            widget.after(delay, step, i + 1)

    step()

# Add inside your `home_frame` setup
greeting_text = get_greeting()
greeting_label = tk.Label(home, text=greeting_text, font=("Segoe UI", 14, "bold"), fg="#000000", bg=home["bg"])
greeting_label.pack(pady=(10, 0))

# Start fade-in effect
fade_in(greeting_label)

def get_pinned_notes_from_txt():
    notes = []
    try:
        with open(pinned_file, "r", encoding="utf-8") as file:# encoding is used to handles ASCII and more, and avoids errors or misread characters.
            for line in file:
                filename = line.strip()
                if filename:
                    notes.append(filename)
        return notes[:3]# only show the first three
    except FileNotFoundError:
        return []

def populate_pinned_preview(parent_frame):
    for widget in parent_frame.winfo_children():
        widget.destroy()

    tk.Label(parent_frame, text="📌 Pinned Notes", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(5, 0))

    listbox = tk.Listbox(parent_frame, width=60, height=6, bg=WHITE_BG)
    listbox.pack(fill="x", padx=10, pady=5)

    pinned = get_pinned_notes_from_txt()
    if pinned:
        for filename in pinned:
            listbox.insert("end", filename)
    else:
        listbox.insert("end", "No pinned notes.")



card_frame = tk.Frame(home, bg=WHITE_BG)
card_frame.pack(pady=10)

pinned_preview_frame = ttk.Frame(home)
pinned_preview_frame.pack(fill="x", padx=10, pady=(0, 10))


def create_feature_card(parent, icon, title, desc, tab_index):
    card = tk.Frame(parent, bg=BLUE_ACCENT, bd=1, relief="flat", highlightthickness=2,
                    highlightbackground=BLUE_SELECTED)
    card.bind("<Button-1>", lambda e: notebook.select(tab_index))

    def on_enter(e): card.config(bg=BLUE_SELECTED)
    def on_leave(e): card.config(bg=BLUE_ACCENT)

    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)

    icon_label = tk.Label(card, text=icon, font=("Segoe UI Emoji", 30), bg=BLUE_ACCENT)
    icon_label.pack(pady=(10, 0))

    title_label = tk.Label(card, text=title, font=("Segoe UI", 13, "bold"), bg=BLUE_ACCENT, fg=TEXT_COLOR)
    title_label.pack(pady=(5, 5))

    desc_label = tk.Label(card, text=desc, font=("Segoe UI", 10), bg=BLUE_ACCENT, fg=TEXT_COLOR, wraplength=180,
                          justify="center")
    desc_label.pack(pady=(5, 10))

    return card


# Placeholder tabs for Timer and To-Do for now
timer_tab = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(timer_tab, text="⏲ Timer")

#Fdisplay clock
def clock():
    hour = time.strftime("%H")
    minute = time.strftime("%M")
    second = time.strftime("%S")
    day = time.strftime("%a")
    date = time.strftime("%d")

    label_time.config(text=hour + ":" + minute + ":" + second)
    label_day_date.config(text=day + "," + date)
    label_time.after(1000, clock)

label_time = tk.Label(timer_tab, text="time", font=("Arial", 20))
label_time.place(relx=1.0, x=-10, y=10, anchor="ne")
label_day_date = tk.Label(timer_tab, text="", font=("Arial", 12))
label_day_date.place(relx=1.0, x=-10, y=40, anchor="ne")

#connect betwen python and tkinter
hours = StringVar(value="00")
mins = StringVar(value="00")
secs = StringVar(value="00")

#get purpose
purpose = StringVar(timer_tab, "")

main_label = tk.Label(timer_tab, text="Set the time")
main_label.pack()

timeinput_frame = tk.LabelFrame(timer_tab)
timeinput_frame.pack(pady=10)

#input
hoursentry = tk.Entry(timeinput_frame, width=2, textvariable=hours, font=("arial", 18))
hoursentry.pack(side=tk.LEFT)
separatorlabel = tk.Label(timeinput_frame, text=":")
separatorlabel.pack(side=tk.LEFT)
minsentry = tk.Entry(timeinput_frame, width=2, textvariable=mins, font=("arial", 18))
minsentry.pack(side=tk.LEFT)
separatorlabel2= tk.Label(timeinput_frame, text=":")
separatorlabel2.pack(side=tk.LEFT)
secsentry = tk.Entry(timeinput_frame, width=2, textvariable=secs, font=("arial", 18))
secsentry.pack(side=tk.LEFT)

#Frame for preset buttons
preset_frame = tk.Frame(timer_tab)
preset_frame.pack(pady=10)

def set_preset_time(h, m, s):
    hours.set(f"{h:02}")
    mins.set(f"{m:02}")
    secs.set(f"{s:02}")

#preset buttons
preset_5min = tk.Button(preset_frame, text="5 min")
preset_5min.config(command=lambda: set_preset_time(0, 5, 0))
preset_5min.pack(side=tk.LEFT, padx=5)

preset_10min = tk.Button(preset_frame, text="10 min")
preset_10min.config(command=lambda: set_preset_time(0, 10, 0))
preset_10min.pack(side=tk.LEFT, padx=5)

preset_25min = tk.Button(preset_frame, text="25 min")
preset_25min.config(command=lambda: set_preset_time(0, 25, 0))
preset_25min.pack(side=tk.LEFT, padx=5)

preset_1hour = tk.Button(preset_frame, text="1 hour")
preset_1hour.config(command=lambda: set_preset_time(1, 0, 0))
preset_1hour.pack(side=tk.LEFT, padx=5)

purpose_label = tk.Label(timer_tab, text="Purpose")
purpose_label.pack()
purpose_entry= tk.Entry(timer_tab, textvariable=purpose, font=("arial", 14))
purpose_entry.pack()

timers_frame = tk.Frame(timer_tab)
timers_frame.pack(pady=20)

#checking input validation
def inputvalidation():
    try:

        if  int(secs.get()) < 0 or int(secs.get()) > 59:
            messagebox.showerror("invalid input", "It must be between 0 to 59")
            return False
        if int(mins.get()) < 0 or int(mins.get()) > 59:
            messagebox.showerror("invalid input", "It must be between 0 to 59")
            return False
        if int(hours.get()) < 0 or int(hours.get()) > 99:
            messagebox.showerror("invalid input", "It must be between 0 to 99")
            return False
        if hours.get() == "00" and mins.get() == "00" and secs.get() == "00":
           messagebox.showerror("Invalid Time", "Time must be greater than 00:00:00.")
           return  False
     
        return True
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numbers for hours, minutes, and seconds.")
        return False

#timer function
def timer():
    if not inputvalidation():
        return
    
    totaltime = int(hours.get())*3600 + int(mins.get())*60 + int(secs.get())

    create_time = time.strftime("%Y-%m-%d %H:%M:%S")
    purpose_text = purpose.get()

    #saving function
    with open("timerhistory.txt","a") as f:
        f.write(f"{create_time} - {purpose_text} ({hours.get()}:{mins.get()}:{secs.get()})\n")
    
    ntimer = tk.Frame(timers_frame)
    ntimer.pack(pady=5)

    ntimer_label = tk.Label(ntimer, text="", font=("Arial", 18))
    ntimer_label.pack(side=tk.LEFT)

    purposetext = tk.Label(ntimer, text=f"for {purpose_text}")
    purposetext.pack(side=tk.LEFT)

    remaining_time = [totaltime]
    paused = [False]

    #countdown function
    def countdown(timeleft):
        if timeleft >= 0:
            hourss,remainder = divmod(timeleft,3600)
            minss,secss = divmod(remainder,60)
            ntimer_label.config(text=f"{hourss:02}:{minss:02}:{secss:02}")
            if not paused[0]:
                root.after(1000, countdown, timeleft - 1)
            remaining_time[0] = timeleft
        else:
            ntimer_label.config(text="DONE!", fg="green")

            if os.path.exists(sound_path.get()):
                try:
                    pygame.mixer.music.load(sound_path.get())
                    pygame.mixer.music.play()

                except Exception as e:
                    print("Error playing sound:", e)
            else:
                print("No sound file selected or path invalid.")

            if show_notification.get():
                notification.notify(
                    title="Timer Finished",
                    message=f"Time's up for '{purpose_text}'",
                    timeout=3
                )
                messagebox.showinfo("ALERT", f"TIMES UP for '{purpose_text}'")


    def pause():
        paused[0] = True
        pause_btn.config(state="disabled")
        resume_btn.config(state="normal")
    
    def resume():
        paused[0] = False
        countdown(remaining_time[0])
        resume_btn.config(state="disabled")
        pause_btn.config(state="normal")
    
    def clear():
        paused[0] = True
        ntimer.destroy()
        resume_btn.config(state="disabled")
        pause_btn.config(state="normal")

    pause_btn = tk.Button(ntimer, text="⏸ Pause", command=pause)
    pause_btn.pack(side=tk.LEFT)

    resume_btn = tk.Button(ntimer, text="▶ Resume", command=resume)
    resume_btn.pack(side=tk.LEFT)

    clear_btn = tk.Button(ntimer, text="❌ Clear", command=clear)
    clear_btn.pack(side=tk.LEFT)

    hours.set("00")
    mins.set("00")
    secs.set("00")
    purpose.set("")

    countdown(totaltime)  
      
start_btn = tk.Button(timer_tab, text="Start New Timer", command=timer)
start_btn.pack()

#history tab 
def open_history_window():
    history_window = tk.Toplevel(root)
    history_window.title("History")
    history_window.geometry("400x400")
    history_label = tk.Label(history_window, text="History Here", font=("Arial", 16))
    history_label.pack(pady=20)
    history_text = tk.Text(history_window, wrap=tk.WORD)
    history_text.pack()

    try:
        with open("timerhistory.txt", "r") as f:
            content = f.read()
            history_text.insert(tk.END, content)
    except FileNotFoundError:
        history_text.insert(tk.END, "No history yet.")

history_button = tk.Button(timer_tab, text="History", command=open_history_window)
history_button.place(relx=0.0, rely=1.0, x=10, y=-10, anchor="sw")

sound_path = StringVar(value="") 
if os.path.exists("alarmpath.txt"):
    with open("alarmpath.txt", "r") as f:
        saved_alarm = f.read().strip()
        if os.path.exists(saved_alarm):
            sound_path.set(saved_alarm)
        else:
            messagebox.showwarning("Alarm Sound Not Found", "The previously saved alarm sound file was not found. Please select a new one.")

def choose_sound():
    file = filedialog.askopenfilename(
        title="Select Alarm Sound",
        filetypes=[("Audio Files", "*.wav *.mp3 *.ogg")]
    )
    if file:
        sound_path.set(file)
        with open("alarmpath.txt", "w") as f:
            f.write(file)

def preview_sound():
    if os.path.exists(sound_path.get()):
        try:
            pygame.mixer.music.load(sound_path.get())
            pygame.mixer.music.play()
        except Exception as e:
            messagebox.showerror("Sound Error", f"Could not play the sound.\n{e}")
    else:
        messagebox.showwarning("No Sound", "Please select a valid sound file first.")


show_notification = tk.BooleanVar(value=True)

options_frame = tk.Frame(timer_tab)
options_frame.place(relx=1.0, rely=1.0, x=-10, y=-10, anchor="se")

select_button = tk.Button(options_frame, text="🎵 Choose Alarm Sound", command=choose_sound)
select_button.pack(side=tk.LEFT)

preview_button = tk.Button(options_frame, text="🔊 Preview", command=preview_sound)
preview_button.pack(side=tk.LEFT, padx=5)


notify_checkbox = tk.Checkbutton(options_frame, text="Notification PoPup", variable=show_notification)
notify_checkbox.pack(side=tk.LEFT, padx=10)


clock()


todo_tab = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(todo_tab, text="✅ To-Do List")

input_frame = tk.Frame(todo_tab)
input_frame.pack(pady=10, fill="x") 

#task entry
task_label = tk.Label(input_frame, text="Task")
task_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

task_entry = tk.Entry(input_frame, width=40)
task_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")  

#priority
priority_label = tk.Label(input_frame, text="Priority")
priority_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

priority_frame = tk.Frame(input_frame)
priority_frame.grid(row=0, column=3, padx=5, pady=5, sticky="w")

priority_var = StringVar()
priority_var.set("Medium")

tk.Radiobutton(priority_frame, text="High", variable=priority_var, value="High").pack(side="left")
tk.Radiobutton(priority_frame, text="Medium", variable=priority_var, value="Medium").pack(side="left")
tk.Radiobutton(priority_frame, text="Low", variable=priority_var, value="Low").pack(side="left")

#add task function
def addtask(event = None):
        date = time.strftime("%Y-%m-%d")                                                        #get date
        task = task_entry.get()                                                                 #get task
        priority = priority_var.get()                                                           #get priority
        if task == "" :                                                                         #show no task or not
            messagebox.showerror("task","no task")                                              
        else:                                                                                   
            task_tree.insert("", "end", values=("☐", date, task, priority), tags=(priority))   #add task to list 
            task_entry.delete(0, tk.END)                                                       #delete entry after task added  
        tdl_task()                                                                             #save to txt file
        temp_message("Task added!")

#delete task function
def deletetask():
        whichtask = task_tree.selection()                                                       #see which task selecred
        if whichtask:                           
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?"):
                task_tree.delete(whichtask)
                tdl_task()
                
        else:
             messagebox.showerror("Error","No task selected")                                   #if didnt select task

        tdl_task()                                                                              #update the txt file
        temp_message("Task deleted!", color="red")

completed_task = []                                                                             #list to hold completed tasks

#toggle function
def togglecheckbox(event):

    #check where user clicking
    region = task_tree.identify("region", event.x, event.y)
    if region != "cell":
        return
    
    selected = task_tree.selection()                                                            #get task              
    if selected:
        for task in selected:
            status = list(task_tree.item(task, "values"))                                       #get task data in list 
            if status[0] == "☐":
                status[0] = "☑"
                completed_task.append(status)                                                   #add to completed list
                task_tree.delete(task)                                                          #delete from the task tree list
    
    tdl_task()
    tracker_task()
    temp_message("Task marked as completed!")

completed_tasktree = None                                                                       #global the treeview

#undo toggle function
def undo_completedtask(event):
    selected = completed_tasktree.selection()
    if selected:
        for task in selected:
            status = list(completed_tasktree.item(task, "values"))
            if status[0] == "☑":
                status[0] = "☐"
                task_tree.insert("", "end", values=status, tags=status[3])                      #reinsert the task to list with correct values
                completed_tasktree.delete(task)                                                 #delete the task from tracker

                for task in completed_task:
                    if task[1:] == status[1:]:                                                  #compare the task values
                        completed_task.remove(task)                                             #if match then remove it
                        break   
    
    tdl_task()
    tracker_task()
    temp_message("Task restored!", color="red")

button_frame = tk.Frame(todo_tab)
button_frame.pack(pady=10, fill="x")

message_label = tk.Label(todo_tab, text="", fg="green", font=("Arial", 10))
message_label.pack(pady=(0, 5))

addtask_btn = tk.Button(button_frame, text="Add Task", command=addtask)
addtask_btn.pack(side="left", padx=10, pady=5) 

deltask_btn = tk.Button(button_frame, text="Delete Task", command=deletetask)
deltask_btn.pack(side="left", padx=10, pady=5)

listbox_frame = tk.Frame(todo_tab)
listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)
listbox_frame.grid_rowconfigure(0, weight=1)
listbox_frame.grid_columnconfigure(0, weight=1)

section = ("status", "Date", "Task", "Priority")
task_tree = ttk.Treeview(listbox_frame, columns=section, show="headings")

scrollbar = ttk.Scrollbar(listbox_frame, orient="vertical", command=task_tree.yview)
task_tree.configure(yscrollcommand=scrollbar.set)
task_tree.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

task_tree.heading("status", text="Status")
task_tree.column("status", width=50, stretch=tk.NO) 
task_tree.heading("Date", text="Date", command=lambda: sorting(task_tree, "Date", sort_states.get("Date", False)))
task_tree.column("Date", width=100, stretch=tk.NO)  
task_tree.heading("Task", text="Task", command=lambda: sorting(task_tree, "Task", sort_states.get("Task", False)))
task_tree.column("Task", width=300, stretch=tk.YES)  
task_tree.heading("Priority", text="Priority", command=lambda: sorting(task_tree, "Priority", sort_states.get("Priority", False)))
task_tree.column("Priority", width=150, stretch=tk.NO)  

task_tree.bind("<Double-1>", togglecheckbox)

task_tree.tag_configure("High", background="#ff9999")   
task_tree.tag_configure("Medium", background="#ffff99")  
task_tree.tag_configure("Low", background="#ccffcc")     

task_entry.bind("<Return>", addtask)

def completion_tracker():
    global completed_tasktree
    completiontracker = tk.Toplevel(root)  
    completiontracker.title("Completion Tracker")
    completiontracker.geometry("500x500")
    frame = tk.Frame(completiontracker)
    frame.pack(fill="both", expand=True, padx=10, pady=10)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)
    
    if not completed_task:
        label = tk.Label(completiontracker, text="No completed tasks yet.")
        label.pack(pady=20)
        return
    
    else:
        completed_tasktree = ttk.Treeview(frame, columns=section, show="headings")
        completed_tasktree.heading("status", text="Status")
        completed_tasktree.column("status", width=50, stretch=tk.NO) 
        completed_tasktree.heading("Date", text="Date")
        completed_tasktree.column("Date", width=70, stretch=tk.NO)  
        completed_tasktree.heading("Task", text="Task")
        completed_tasktree.column("Task", width=100, stretch=tk.YES)  
        completed_tasktree.heading("Priority", text="Priority")
        completed_tasktree.column("Priority", width=80, stretch=tk.NO)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=completed_tasktree.yview)
        completed_tasktree.configure(yscrollcommand=scrollbar.set)
        completed_tasktree.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        for task in completed_task:
            completed_tasktree.insert("", "end", values=task)

        completed_tasktree.bind("<Double-1>", undo_completedtask)

completion_tracker_btn = tk.Button(button_frame, text="Completion Tracker", command=completion_tracker)
completion_tracker_btn.pack(side="right", padx=10, pady=5)


def tdl_task():
    with open ("tdltask.txt", "w", encoding="utf-8") as file:                               
        for task in task_tree.get_children():
            values = task_tree.item(task)["values"]                                                 #get task values
            content = f"{values[0]} | {values[1]} | {values[2]} | {values[3]}\n"                    #split em in |
            file.write(content)

def tracker_task():
    with open ("trackertask.txt", "w", encoding="utf-8") as file:
        for task in completed_task:
            content = f"{task[0]} | {task[1]} | {task[2]} | {task[3]}\n"
            file.write(content)


def load_txt():
    try:
        with open ("tdltask.txt", "r", encoding="utf-8") as file:
            for content in file:
                parts = content.strip().split(" | ")                                                #split content into parts
                if len(parts) == 4:                                                                 #check wheter have 4 parts
                    task_tree.insert("", "end", values=parts, tags=(parts[3]))                      #true then insert all of the values
    except FileNotFoundError:
        pass

    try:
        with open("trackertask.txt", "r", encoding="utf-8") as file:
            for content in file:
                parts = content.strip().split(" | ")
                if len(parts) == 4:
                    completed_task.append(parts)
    except FileNotFoundError:
        pass

sort_states = {}                                                                                    #dict to store sort state

def sorting(tree, col, descending):
    global sort_states
    data = [(tree.set(item, col), item) for item in tree.get_children()]                            #get value and item id list

    if col == "Date":
        data.sort(key=lambda t: datetime.strptime(t[0], "%Y-%m-%d"), reverse=descending)            #convert date string and see wheter ascending or descending

    elif col == "Priority":
        priority_order = {"High": 0, "Medium": 1, "Low": 2}
        data.sort(key=lambda t: priority_order.get(t[0].capitalize(), 99), reverse=descending)      #get priority and make sure everything in correct form

    else:
        data.sort(key=lambda t: t[0].lower(), reverse=descending)

    for index, (val, item) in enumerate(data):                                                      #check all index and give all data a index
        tree.move(item, '', index)                                                                  #move it

    for colname in tree["columns"]:
        arrow = ""
        if colname == col:
            arrow = " ↓" if descending else " ↑"
        sort_states[col] = not descending                                              
        tree.heading(colname, text=colname + arrow, command=lambda c=colname: sorting(tree, c, sort_states.get(c, False))) #update the heading

#notification
def temp_message(message, color="green"):
    message_label.config(text=message, fg=color)
    root.after(1500, lambda: message_label.config(text=""))

load_txt()

# all note function
def update_file_list():
    file_listbox.delete(0, tk.END)
    files = [f for f in os.listdir(folder_path) if f.endswith((".txt", ".md", ".html"))]
    for file in files:
        file_listbox.insert(tk.END, file)

def search_notes():
    search_term = search_entry.get().lower().strip()
    file_listbox.delete(0, tk.END)
    files = [f for f in os.listdir(folder_path) if f.endswith((".txt", ".md", ".html"))]

    shown_files = set()  # To prevent duplicates

    for file in files:
        file_path = os.path.join(folder_path, file)

        file_name_match = search_term in file.lower()
        content_match = False

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
                content_match = search_term in content
        except Exception as e:
            print(f"Could not read {file}: {e}")
            continue

        # Show if either file name or content matches
        if (file_name_match or content_match) and file not in shown_files:
            file_listbox.insert(tk.END, file)
            shown_files.add(file)

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

            name_match = query in file_name.lower()
            content_match = False

            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    content_match = query in content.lower()
            except Exception as e:
                print(f"Could not read {file_name}: {e}")
                continue

            if name_match and content_match:
                results.append(f"Match in File: {file_name} (name + content)")
            elif name_match:
                results.append(f"File Name Match: {file_name}")
            elif content_match:
                results.append(f"Content Match in {file_name}")

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

def export_all_notes_as_zip():
    files = [f for f in os.listdir(folder_path) if f.endswith((".txt", ".html", ".md"))]
    if not files:
        messagebox.showinfo("Info", "No notes to export.")
        return

    export_folder = folder_path/ "Exports"
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
                save_pinned_notes()
                populate_pinned_preview(pinned_preview_frame)
                messagebox.showinfo("Info", f"Pinned '{file_name}' successfully!")
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
                save_pinned_notes()  # ✅ Save the updated list
                populate_pinned_preview(pinned_preview_frame)
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
            save_pinned_notes()  # ✅ Save the updated list
            populate_pinned_preview(pinned_preview_frame)
            messagebox.showinfo("Info", f"Unpinned '{file_name}' successfully!")
    else:
        messagebox.showinfo("Remind", "Please select a pinned note first.")

def save_pinned_notes():
    with open(pinned_file, "w") as f:
        for item in tree.get_children():
            filename = tree.item(item, "values")[0]
            f.write(f"{filename}\n")


def load_pinned_notes():
    if os.path.exists(pinned_file):
        with open(pinned_file, "r") as f:
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

# Google Drive API 


import mimetypes
import webbrowser
import json

# Defines permission 
# metadata - view file names adn metadata 
#drive.file uploading files 
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.file"]
auth_window = None  
SYNC_META_PATH = folder_path / ".syncmeta.json"
LOCAL_FOLDER_PATH = folder_path
service = None

def authenticate():
    creds = None
    token_path = get_token_path()

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            cred_path = get_cred_path()
            flow = InstalledAppFlow.from_client_secrets_file(cred_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())


    return build('drive', 'v3', credentials=creds)

def get_or_create_main_folder(service):
    global folder
    folder_name = "MMU Study Buddy Files"
    query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    items = results.get('files', [])
    if items:
        return items[0]['id']
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = service.files().create(body=file_metadata, fields='id').execute()
    return folder['id']

##############

def sync_upload_file(service, file_path, folder_id, existing_drive_id=None):
    file_name = os.path.basename(file_path)
    file_metadata = {"name": file_name, "parents": [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)

    if existing_drive_id:
        uploaded_file = service.files().update(
            fileId=existing_drive_id,
            media_body=media
        ).execute()
    else:
        uploaded_file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, modifiedTime"
        ).execute()

    # 🔁 Make sure to fetch the updated modifiedTime
    updated_file = service.files().get(fileId=uploaded_file["id"], fields="id, modifiedTime").execute()

    return {
        "local_modified": get_local_modified_time(file_path).isoformat(),
        "drive_modified": updated_file["modifiedTime"],
        "drive_id": updated_file["id"]
    }



def sync_download_files(service, file_id, local_file_path):
    try:
        request = service.files().get_media(fileId=file_id)
        os.makedirs(os.path.dirname(local_file_path), exist_ok=True)
        with open(local_file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
            drive_file = service.files().get(fileId=file_id, fields='modifiedTime').execute()
        drive_mod_time_str = drive_file['modifiedTime']
        drive_mod_time = parser.parse(drive_mod_time_str)
        mod_timestamp = drive_mod_time.timestamp()
        os.utime(local_file_path, (mod_timestamp, mod_timestamp))
        return {
            "drive_id": file_id,
            "drive_modified": drive_mod_time_str,
            "local_modified": drive_mod_time.isoformat()
    }
    except Exception as e:
        print(f"error:{str(e)}")


def list_drive_files(service, folder_id):
    query = f"'{folder_id}' in parents and trashed = false"
    fields = "files(id, name, modifiedTime)"
    results = service.files().list(q=query, fields=fields).execute()
    return results.get('files', [])

# ---------- Sync meta (local cache) ----------

def load_sync_meta():
    if os.path.exists(SYNC_META_PATH):
        try:
            with open(SYNC_META_PATH, "r", encoding="utf-8") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
        except json.JSONDecodeError:
            print("⚠️ Warning: .syncmeta.json is corrupted or invalid. Resetting.")
            return {}
    return {}

def save_sync_meta(meta):
    print(f"Saving sync meta to: {SYNC_META_PATH}")
    try:
        with open(SYNC_META_PATH, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=4)
        print("Updated into json")
    except Exception as e:
        print("Failed to save sync meta:", e)

def get_local_modified_time(filepath):
    return datetime.fromtimestamp(os.path.getmtime(filepath), tz=timezone.utc)


def timestamps_close(t1, t2, tolerance_seconds=2):
    delta = abs((t1 - t2).total_seconds())
    return delta <= tolerance_seconds

# ---------- Main sync function ----------
 
def sync_now_to_drive():
    sync_meta = load_sync_meta()
    updated_meta = {}
    all_synced = True  # Assume everything is synced unless proven otherwise

    try:
        print("🔄 2-Way Sync started...")
        folder_path = LOCAL_FOLDER_PATH
        service = authenticate()
        drive_folder_id = get_or_create_main_folder(service)

        drive_files = list_drive_files(service, drive_folder_id)
        drive_file_map = {f["name"]: f for f in drive_files}

        for root_dir, dirs, files in os.walk(folder_path):
            # Only allow 'Notes' subfolder
            rel_path = os.path.relpath(root_dir, folder_path)
            
            if rel_path != '.' and not rel_path.startswith("Notes"):
                print(f"⏭️ Skipped folder: {root_dir}")
                dirs[:] = []  # Don't recurse further into this subfolder
                continue


            for filename in files:
                if filename == ".syncmeta.json":
                    continue

                local_path = os.path.join(folder_path, filename)
                local_time = get_local_modified_time(local_path)
                drive_file = drive_file_map.get(filename)
                
                prev_entry = sync_meta.get(filename, {})
                prev_local_time = parser.parse(prev_entry.get("local_modified")) if prev_entry.get("local_modified") else None
                prev_drive_time = parser.parse(prev_entry.get("drive_modified")) if prev_entry.get("drive_modified") else None

                if drive_file:
                    drive_id = drive_file["id"]
                    drive_time = parser.parse(drive_file["modifiedTime"])

                    if local_time > drive_time and not timestamps_close(local_time, drive_time):
                        print(f"🔼 Local newer → Uploading {filename}")
                        all_synced = False
                        uploaded = sync_upload_file(service, local_path, drive_folder_id, existing_drive_id=drive_id)
                        updated_meta[filename] = {
                            "local_modified": local_time.isoformat(),
                            "drive_modified": uploaded["drive_modified"],
                            "drive_id": uploaded["drive_id"]
                        }

                    elif drive_time > local_time and not timestamps_close(drive_time, local_time):
                        print(f"🔽 Drive newer → Downloading {filename}")
                        all_synced = False
                        result = sync_download_files(service, drive_id, local_path)
                        updated_meta[filename] = result

                    else:
                        print(f"✅ Up-to-date: {filename}")
                        # Leave `all_synced` unchanged here to avoid false positive
                        updated_meta[filename] = {
                            "local_modified": local_time.isoformat(),
                            "drive_modified": drive_time.isoformat(),
                            "drive_id": drive_id
                        }

                else:
                    print(f"🔼 Only on PC → Uploading {filename}")
                    all_synced = False
                    uploaded = sync_upload_file(service, local_path, drive_folder_id)
                    updated_meta[filename] = {
                        "local_modified": local_time.isoformat(),
                        "drive_modified": uploaded["drive_modified"],
                        "drive_id": uploaded["drive_id"]
                    }

        # Handle files only on Drive
        for drive_file in drive_files:
            filename = drive_file["name"]
            local_file_path = os.path.join(folder_path, filename)
            if not os.path.exists(local_file_path):
                print(f"🔽 Only on Drive → Downloading {filename}")
                all_synced = False
                result = sync_download_files(service, drive_file["id"], local_file_path)
                updated_meta[filename] = result

        save_sync_meta(updated_meta)

        print("✅ 2-Way Sync complete!")
        return all_synced

    except Exception as e:
        print("❌ Sync failed:", e)
        return True  # Fail safe: exit loop on error

def threading_sync_till_up_to_date():
    def sync_till_up_to_date():
        print("I am till all file is up to date")
        while True:
            SyncStatus = sync_now_to_drive()
            if SyncStatus:
                break
        print("✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅✅")
        messagebox.showinfo("Sync Completed", "All Files Have Been Synced")
    threading.Thread(target=sync_till_up_to_date, daemon=True).start()
    


######




import tkinter as tk
from tkinter import ttk, messagebox
import threading
import os
import webbrowser

# --- Sync logic (outside main_api) ---


SYNC_OPTIONS = {
    "Every 10 min": 600,
    "Every 30 min": 1800,
    "Every 1 hour": 3600
}

sync_interval_var = tk.StringVar(value="Every 10 min")
auto_sync_enabled_var = tk.BooleanVar(value=True)
auto_sync_enabled = True
auto_sync_timer = None

def start_auto_sync(interval_label):
    global auto_sync_timer, auto_sync_enabled

    interval_seconds = SYNC_OPTIONS.get(interval_label, 0)
    if interval_seconds == 0 or not auto_sync_enabled:
        print("⛔ Auto-sync is OFF.")
        return

    print(f"⏳ Scheduled next auto-sync in {interval_seconds} seconds...")
    auto_sync_timer = threading.Timer(interval_seconds, run_auto_sync, args=(interval_label,))
    auto_sync_timer.start()

def run_auto_sync(interval_label):
    global auto_sync_enabled

    if not auto_sync_enabled:
        print("⛔ Auto-sync stopped; won't continue syncing.")
        return

    try:
        print("🔄 Auto-Sync triggered...")
        threading_sync_till_up_to_date()
    finally:
        if auto_sync_enabled:
            start_auto_sync(interval_label)


def stop_auto_sync():
    global auto_sync_timer
    if auto_sync_timer:
        auto_sync_timer.cancel()
        auto_sync_timer = None
    print("⏸️ Auto-Sync Paused")

# --- UI function ---

def main_api():
    authenticate()
    global auto_sync_enabled

    drive_window = tk.Toplevel()
    drive_window.title("Drive Panel")
    drive_window.resizable(False, False)
    drive_window.configure(bg="#f0f0f0")

    # Title Label
    tk.Label(
        drive_window,
        text="📁 Drive Control Panel",
        font=("Helvetica", 14, "bold"),
        bg="#f0f0f0",
        fg="#000000"
    ).pack(pady=(15, 10))

    # Frame for buttons
    button_frame = tk.Frame(drive_window)
    button_frame.pack(pady=10)



    def show_files():
        try:
            files = os.listdir(folder_path)
            files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
            file_listbox.delete(0, tk.END)
            for file in files:
                file_listbox.insert(tk.END, file)
        except FileNotFoundError:
            print("The folder path doesn't exist.")

    # Buttons
    SyncNow = tk.Button(button_frame, text="⬇️ Sync Now", command=threading_sync_till_up_to_date, font=("Arial", 10),
                        bg="#e0e0e0", fg="#000000", relief="raised", bd=2, width=20, height=2)
    SyncNow.pack(pady=5)

    def open_drive():
        webbrowser.open("https://drive.google.com/drive/my-drive")

    ToDrive = tk.Button(button_frame, text="🌐 Go to Drive", command=open_drive, font=("Arial", 10),
                        bg="#e0e0e0", fg="#000000", relief="raised", bd=2, width=20, height=2)
    ToDrive.pack(pady=5)

    ReloadFiles = tk.Button(button_frame, text="🔄 Reload", command=show_files, font=("Arial", 10),
                            bg="#e0e0e0", fg="#000000", relief="raised", bd=2, width=20, height=2)
    ReloadFiles.pack(pady=5)

    # Interval dropdown
    SyncTiming = ttk.OptionMenu(button_frame, sync_interval_var, sync_interval_var.get(), *SYNC_OPTIONS.keys())
    SyncTiming.pack(pady=5)


    def toggle_auto_sync():
        global sync_interval_var
        global auto_sync_enabled

        auto_sync_enabled = auto_sync_enabled_var.get()
        if auto_sync_enabled:
            SyncTiming.config(state="normal")
            start_auto_sync(sync_interval_var.get())
            print("▶️ Auto-Sync Enabled")
        else:
            SyncTiming.config(state="disabled")
            stop_auto_sync()

    SyncAuto = tk.Checkbutton(button_frame, text="Auto-Sync", variable=auto_sync_enabled_var, command=toggle_auto_sync)
    SyncAuto.pack(pady=5)

    def logout():
        global service
        print("Logging out...")
        service = None
        token_path = get_token_path()  # <-- Use your helper function here
        if os.path.exists(token_path):
            try:
                os.remove(token_path)
                print("✅ token.json deleted successfully")
            except Exception as e:
                print(f"❌ Failed to delete token.json: {e}")
        else:
            print("⚠️ token.json not found, already deleted?")

        messagebox.showinfo("Logged Out", "You have been logged out successfully.")
        drive_window.destroy()
        

    LogOut = tk.Button(button_frame, text="🚪 Log Out", command=logout, font=("Arial", 10),
                        bg="#e0e0e0", fg="#000000", relief="raised", bd=2, width=20, height=2)
    LogOut.pack(pady=5)

    # Footer
    tk.Label(
        drive_window,
        text="Connected to Google Drive",
        font=("Arial", 9, "italic"),
        bg="#f0f0f0",
        fg="#555555"
    ).pack(pady=(15, 10))

    show_files()

    # Initialize auto sync state

token_path = get_token_path()
auto_sync_enabled = auto_sync_enabled_var.get()
if auto_sync_enabled and os.path.exists(token_path):
    start_auto_sync(sync_interval_var.get())
else: 
    messagebox.showinfo("Sign In for Auto-Sync", "Sign in to enable your auto sync function")

def threaded_authenticate(callback):
    global auth_window 

    def worker():
        global service
        try:
            service = authenticate()
            root.after(0, lambda: finish_auth(callback))  # callback on main thread
        except Exception as e:
            print("Authentication failed:", e)
            root.after(0, lambda: messagebox.showerror("Error", "Authentication failed. Please try again."))


    threading.Thread(target=worker, daemon=True).start()

def finish_auth(callback):
    global auth_window
    if auth_window is not None:
        auth_window.destroy()
        auth_window = None
    callback()


#note tab
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
file_listbox = tk.Listbox(notes_tab, font=FONT_TEXT,bg="white")
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
btn_new = ttk.Button(note_btn_frame, text="New Note", command=run_notepad)
btn_new.pack(side='left', padx=5)

btn_open = ttk.Button(note_btn_frame, text="Open Note", command=open_file_button_clicked)
btn_open.pack(side='left', padx=5)

btn_delete = ttk.Button(note_btn_frame, text="Delete Note", command=lambda: deleting_notes())
btn_delete.pack(side='left', padx=5)

btn_export = ttk.Button(note_btn_frame, text="Export Notes", command=lambda: export_notes_with_format())
btn_export.pack(side='left', padx=5)

btn_drive = ttk.Button(note_btn_frame, text="Open Drive", command=main_api)
btn_drive.pack(side="left", padx=5)

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
def highlight_remark_dates():
    cal.calevent_remove('all')  # clear previous events/highlights

    for date_str, remark in remarks.items():
        tag = None
        if "#low" in remark:
            tag = 'low'
        elif "#medium" in remark:
            tag = 'medium'
        elif "#high" in remark:
            tag = 'high'

        if tag:
            try:
                # Convert date string to datetime.date object
                date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                # Add a calendar event with the tag (color)
                cal.calevent_create(date_obj, remark, tag)
            except Exception as e:
                print(f"Could not tag date {date_str}: {e}")

def load_remarks():
    if os.path.exists(remark_file):
        with open(remark_file, "r") as f:
            for line in f:
                if "|" in line:
                    date, remark = line.strip().split("|", 1)
                    remarks[date] = remark
    highlight_remark_dates()

def save_remarks():
    try:
        with open(remark_file, "w") as f:
            for date, remark in remarks.items():
                f.write(f"{date}|{remark}\n")
        highlight_remark_dates()
    except FileNotFoundError:
        print("error")


# Save remark for selected date
def save_remark_for_date():
    selected_date = cal.get_date()
    remark = remark_text.get("1.0", tk.END).strip()

    if not remark:
        messagebox.showwarning("Empty", "Please enter a remark.")
        return

    def open_importance_popup():
        popup = tk.Toplevel()
        popup.title("Select Importance")
        popup.geometry("250x200")

        tk.Label(popup, text="Select importance level:", font=("Arial", 12)).pack(pady=10)

        importance_var = tk.StringVar(value="None")

        tk.Radiobutton(popup, text="Low", variable=importance_var, value="#low").pack(anchor="w", padx=20)
        tk.Radiobutton(popup, text="Medium", variable=importance_var, value="#medium").pack(anchor="w", padx=20)
        tk.Radiobutton(popup, text="High", variable=importance_var, value="#high").pack(anchor="w", padx=20)
        tk.Radiobutton(popup, text="None", variable=importance_var, value="None").pack(anchor="w", padx=20)

        def confirm_importance():
            tag = importance_var.get()
            final_remark = remark + (f" {tag}" if tag != "None" else "")
            remarks[selected_date] = final_remark
            save_remarks()
            highlight_remark_dates()
            popup.destroy()
            messagebox.showinfo("Saved", f"Remark for {selected_date} saved.")

        tk.Button(popup, text="Save", command=confirm_importance).pack(pady=10)

    open_importance_popup()

# Display saved remark for selected date
def display_remark_for_date(event=None):
    selected_date = cal.get_date()
    remark_text.delete("1.0", tk.END)
    if selected_date in remarks:
        remark_text.insert("1.0", remarks[selected_date])

def view_all_remarks():
    if not remarks:
        messagebox.showinfo("Remarks", "No saved remarks.")
        return
    remark_window = tk.Toplevel()
    remark_window.title("All Remarks")
    remark_window.geometry("400x300")

    text_widget = tk.Text(remark_window, wrap="word", font=("Arial", 12))
    text_widget.pack(expand=True, fill="both", padx=10, pady=10)

    for date, remark in sorted(remarks.items()):
        text_widget.insert(tk.END, f"{date}: {remark}\n\n")

def clear_remark_for_date():
    selected_date = cal.get_date()
    remark_text.delete("1.0", tk.END)
    if selected_date in remarks:
        del remarks[selected_date]  # Remove the saved remark
        save_remarks()  # Save updated remarks to file
    messagebox.showinfo("Cleared", f"Remark for {selected_date} cleared.")
    highlight_remark_dates()

button_frame = tk.Frame(calendar_tab, bg=WHITE_BG)
button_frame.pack(pady=10)

save_button = tk.Button(button_frame, text="💾 Save Remark", command=save_remark_for_date)
save_button.grid(row=0, column=0, padx=5)

clear_button = tk.Button(button_frame, text="🧹 Clear Remark", command=clear_remark_for_date)
clear_button.grid(row=0, column=1, padx=5)

theme_button = tk.Menubutton(button_frame, text="🎨 Theme", relief=tk.RAISED)
theme_menu = tk.Menu(theme_button, tearoff=0)
theme_menu.add_command(label="Pink", command=lambda: apply_theme("Pink"))
theme_menu.add_command(label="Blue", command=lambda: apply_theme("Blue"))
theme_menu.add_command(label="Purple", command=lambda: apply_theme("Purple"))
theme_menu.add_command(label="Custom", command=lambda: apply_theme("Custom"))
theme_button.config(menu=theme_menu)
theme_button.grid(row=0, column=2, padx=5)

view_all_button = tk.Button(button_frame, text="📋 View All Remarks", command=view_all_remarks)
view_all_button.grid(row=0, column=3, padx=5)

cal.tag_config('low', background='lightgreen')
cal.tag_config('medium', background='orange')
cal.tag_config('high', background='red')
# Bind calendar selection to display remark
cal.bind("<<CalendarSelected>>", display_remark_for_date)


# Load saved remarks on startup
load_remarks()
card1 = create_feature_card(card_frame, "⏲", "Timer", "Stay calm and focused in your study with the timer.", 1)
card2 = create_feature_card(card_frame, "✅", "To-Do List", "Organize tasks and boost daily productivity.", 2)
card3 = create_feature_card(card_frame, "📝", "Notes", "Write, pin, search, and export your study notes.", 3)
card4 = create_feature_card(card_frame, "📅", "Calendar", "Attach notes or events to any calendar date.", 4)

card1.grid(row=0, column=0, padx=15, pady=15)
card2.grid(row=0, column=1, padx=15, pady=15)
card3.grid(row=0, column=2, padx=15, pady=15)
card4.grid(row=0, column=3, padx=15, pady=15)

populate_pinned_preview(pinned_preview_frame)

update_file_list()
check_reminders_on_startup()
root.mainloop()


