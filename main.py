import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk,messagebox,colorchooser, filedialog
from datetime import date,datetime
import zipfile
from tkhtmlview import HTMLLabel
import markdown
import re
from bs4 import BeautifulSoup
import os
import time
import winsound
from tkinter import StringVar

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

    # Set Folder for Notes Location
    global folder_path
    folder_path = "C:/Notes"

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
        global Current_File_Mode
        Text_Box.delete("1.0", tk.END)
        #Grab The file name
        text_file = filedialog.askopenfilename(initialdir="C:/Notes", title="Open a File", filetypes=(("Text Files", "*.txt"),("HTML Files", "*.html"),("Markdown Files", "*.md"),("All Files", "*.*")))
        Window_title = text_file
        #Check if there is a file name and if yes, make it global
        if text_file:
            global open_status_name 
            open_status_name = text_file
            File_extension  =  os.path.splitext(text_file)[1].lower()
            if File_extension == ".md":
                Current_File_Mode = "Markdown"
                change_to_markdown()
            elif File_extension in [".html", ".htm"]:
                Current_File_Mode = "HTML"
                change_to_html()
            elif File_extension == ".txt":
                Current_File_Mode = "text"
                change_to_text()
            else:
                # Default to text if unknown type
                Current_File_Mode = "Markdown"
        #Updating Status bar 
        name = text_file
        Status_bar.config(text=f"{name}    ")
        name = name.replace("C:/Users/", "") #Removing the C:/ Prefix
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
            
        text_file = filedialog.asksaveasfilename(defaultextension=file_extention, initialdir="C:/Notes", title="Save File As", filetypes=filetypestosave)
        if text_file:
            open_status_name = text_file
            #Update the status bar
            name = text_file
            Status_bar.config(text=f"Saved: {name}    ")
            name = name.replace("C:/Users/", "") #Removing the C:/ Prefix
            NotepadWindow.title(f"{name} - Note Editor")       

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

    def update_button_based_on_mode():
        if Current_File_Mode == "Text":
            bold_btn.config(state=tk.DISABLED)
            italic_btn.config(state=tk.DISABLED)
            underline_btn.config(state=tk.DISABLED)
            font_size_menu.config(state=tk.DISABLED)
            
        if Current_File_Mode == "HTML":
            bold_btn.config(state=tk.DISABLED)
            italic_btn.config(state=tk.DISABLED)
            underline_btn.config(state=tk.DISABLED)
            font_size_menu.config(state=tk.DISABLED)
            
        if Current_File_Mode == "Markdown":
            bold_btn.config(state=tk.NORMAL)
            italic_btn.config(state=tk.NORMAL)
            underline_btn.config(state=tk.NORMAL)
            font_size_menu.config(state=tk.NORMAL)
            
    def change_to_html():
        global Current_File_Mode
        Current_File_Mode = "HTML"
        File_Settings_Menu.entryconfig("Change to Text File", background="white")  # Color for active mode
        File_Settings_Menu.entryconfig("Change to HTML", background="lightblue")  # Reset others
        File_Settings_Menu.entryconfig("Change to Markdown", background="white")
        update_button_based_on_mode()

    def change_to_text():
        global Current_File_Mode
        Current_File_Mode = "Text"
        File_Settings_Menu.entryconfig("Change to Text File", background="lightblue")  # Color for active mode
        File_Settings_Menu.entryconfig("Change to HTML", background="white")  # Reset others
        File_Settings_Menu.entryconfig("Change to Markdown", background="white")
        update_button_based_on_mode()

    def change_to_markdown():
        global Current_File_Mode
        Current_File_Mode = "Markdown"
        File_Settings_Menu.entryconfig("Change to Text File", background="white")  # Color for active mode
        File_Settings_Menu.entryconfig("Change to HTML", background="white")  # Reset others
        File_Settings_Menu.entryconfig("Change to Markdown", background="lightblue")
        update_button_based_on_mode()

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
    def copy_text(e):
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
            "• Preview updates automatically on save.\n"
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

def open_note_in_notepad(file_path):
    # Open the notepad window with content from the file
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
    except Exception as e:
        print(f"Error opening file: {e}")
        file_content = f"Error: {e}"

    # Call run_notepad with file content
    run_notepad(file_content)
    Text_Box.insert(tk.END, file_content)

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
folder_path = "C:/Notes"
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

icon = tk.PhotoImage(file=r"C:\Users\ASUS\project\pythonfile\Mini_IT_Project-1-08\025.png")  # Use a PNG file
root.iconphoto(False, icon)

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
style.theme_use('default')
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


# tabs for Timer
timer_tab = tk.Frame(notebook, bg=WHITE_BG)
notebook.add(timer_tab, text="⏲ Timer")
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

purpose = StringVar(timer_tab, "")

main_label = tk.Label(timer_tab, text="Set the time")
main_label.pack()

timeinput_frame =tk.LabelFrame(timer_tab)
timeinput_frame.pack(pady=10)

#input
hoursentry = tk.Entry(timeinput_frame, width=2, textvariable=hours, font=("arial", 18))
hoursentry.pack(side =tk.LEFT)
separatorlabel = tk.Label(timeinput_frame, text=":")
separatorlabel.pack(side =tk.LEFT)
minsentry = tk.Entry(timeinput_frame, width=2, textvariable=mins, font=("arial", 18))
minsentry.pack(side =tk.LEFT)
separatorlabel2= tk.Label(timeinput_frame, text=":")
separatorlabel2.pack(side =tk.LEFT)
secsentry = tk.Entry(timeinput_frame, width=2, textvariable=secs, font=("arial", 18))
secsentry.pack(side =tk.LEFT)

purpose_label = tk.Label(timer_tab, text="Purpose")
purpose_label.pack()
purpose_entry= tk.Entry(timer_tab, textvariable=purpose, font=("arial", 14))
purpose_entry.pack()

timers_frame = tk.Frame(timer_tab)
timers_frame.pack(pady=20)

def inputvalidation():
    try:

        if  int(secs.get()) < 0 or int(secs.get()) > 59:
            messagebox.showerror("invalid input", "It must be smaller than 59 or greater than 0")
            return False
        if int(mins.get()) < 0 or int(mins.get()) > 59:
            messagebox.showerror("invalid input", "It must be smaller than 59 or greater than 0")
            return False
        if int(hours.get()) < 0 or int(hours.get()) > 99:
            messagebox.showerror("invalid input", "It must be smaller than 100 or greater than 0")
            return False
        if hours.get() == "00" and mins.get() == "00" and secs.get() == "00":
           messagebox.showerror("Invalid Time", "Time must be greater than 00:00:00.")
           return  False
     
        return True
    except ValueError:
        messagebox.showerror("Invalid Input","Ah boi do uk how to use a timer")
        return False

#timer function
def timer():
    if not inputvalidation():
        return
    
    totaltime = int(hours.get())*3600 + int(mins.get())*60 + int(secs.get())

    create_time = time.strftime("%Y-%m-%d %H:%M:%S")
    purpose_text = purpose.get()

    #saving func
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
            winsound.Beep(1000, 500) 
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

def open_history_window():
    history_window = tk.Toplevel(timer_tab)
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

clock()

# todo tab
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

#delete task function
def deletetask():
        whichtask = task_tree.selection()                                                       #see which task selecred
        if whichtask:                           
            task_tree.delete(whichtask)                                                         #delete selected task
        else:
             messagebox.showerror("Error","No task selected")                                   #if didnt select task

        tdl_task()                                                                              #update the txt file

completed_task = []                                                                             #list to hold completed tasks

#toggle function
def togglecheckbox(event):
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

completed_tasktree = None                                                                       #global the treeview

#untoggle function
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

button_frame = tk.Frame(todo_tab)
button_frame.pack(pady=10, fill="x")

addtask_btn = tk.Button(button_frame, text="Add Task", command=addtask)
addtask_btn.pack(side="left", padx=10, pady=5) 

deltask_btn = tk.Button(button_frame, text="Delete Task", command=deletetask)
deltask_btn.pack(side="left", padx=10, pady=5)

listbox_frame = tk.Frame(todo_tab)
listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

section = ("status", "Date", "Task", "Priority")
task_tree = ttk.Treeview(listbox_frame, columns=section, show="headings")

task_tree.heading("status", text="Status")
task_tree.column("status", width=50, stretch=tk.NO) 
task_tree.heading("Date", text="Date")
task_tree.column("Date", width=100, stretch=tk.NO)  
task_tree.heading("Task", text="Task")
task_tree.column("Task", width=300, stretch=tk.YES)  
task_tree.heading("Priority", text="Priority")
task_tree.column("Priority", width=100, stretch=tk.NO)

task_tree.pack(fill="both", expand=True)
task_tree.bind("<Double-1>", togglecheckbox)

task_tree.tag_configure("High", background="#ff9999")   
task_tree.tag_configure("Medium", background="#ffff99")  
task_tree.tag_configure("Low", background="#ccffcc")     

task_entry.bind("<Return>", addtask)

def completion_tracker():
    global completed_tasktree
    completiontracker = tk.Toplevel(todo_tab)  
    completiontracker.title("Completion Tracker")
    completiontracker.geometry("500x500")
    
    if not completed_task:
        label = tk.Label(completiontracker, text="No completed tasks yet.")
        label.pack(pady=20)
        return
    
    else:
        completed_tasktree = ttk.Treeview(completiontracker, columns=section, show="headings")
        completed_tasktree.heading("status", text="Status")
        completed_tasktree.column("status", width=50, stretch=tk.NO) 
        completed_tasktree.heading("Date", text="Date")
        completed_tasktree.column("Date", width=70, stretch=tk.NO)  
        completed_tasktree.heading("Task", text="Task")
        completed_tasktree.column("Task", width=100, stretch=tk.YES)  
        completed_tasktree.heading("Priority", text="Priority")
        completed_tasktree.column("Priority", width=80, stretch=tk.NO)

        for task in completed_task:
            completed_tasktree.insert("", "end", values=task)

        completed_tasktree.pack(fill="both", expand=True, padx=10, pady=10)
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


load_txt()



# all note function
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
        file_path = os.path.join(folder_path, file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().lower()
            if search_term in content:
                file_listbox.insert(tk.END, file)
        except Exception as e:
            # Optional: handle unreadable files gracefully
            print(f"Could not read {file}: {e}")

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

def open_drive_panel():
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
    button_frame = tk.Frame(drive_window, bg="#f0f0f0")
    button_frame.pack(pady=10)

    # Common button style
    def create_button(text):
        return tk.Button(
            button_frame,
            text=text,
            font=("Arial", 10, "bold"),
            bg="#e0e0e0",    # light gray background
            fg="#000000",    # black text
            relief="raised",
            bd=2,
            width=20,
            height=2
        )

    # Buttons
    create_button("⬇️ Download").pack(pady=5)
    create_button("⬆️ Upload").pack(pady=5)
    create_button("🌐 Go to Drive").pack(pady=5)
    create_button("🔄 Reload").pack(pady=5)
    create_button("🚪 Log Out").pack(pady=5)

    # Footer
    tk.Label(
        drive_window,
        text="Connected to Google Drive",
        font=("Arial", 9, "italic"),
        bg="#f0f0f0",
        fg="#555555"
    ).pack(pady=(15, 10))


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
btn_new = ttk.Button(note_btn_frame, text="New Note",command=run_notepad)
btn_new.pack(side='left', padx=5)

btn_open = ttk.Button(note_btn_frame, text="Open Note",command=open_file_button_clicked)
btn_open.pack(side='left', padx=5)

btn_delete = ttk.Button(note_btn_frame, text="Delete Note", command=lambda: deleting_notes())
btn_delete.pack(side='left', padx=5)

btn_export = ttk.Button(note_btn_frame, text="Export Notes", command=lambda: export_notes_with_format())
btn_export.pack(side='left', padx=5)

btn_drive = ttk.Button(note_btn_frame, text="Open Drive", command=open_drive_panel)
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