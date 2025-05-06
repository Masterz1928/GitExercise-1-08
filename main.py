# branch to add in auto save feature + Word Count thingy 

#Testing to add in pictures into Notepad
import tkinter as tk # Getting tkinter into the program
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox  
from tkhtmlview import HTMLLabel
import markdown
import re
from bs4 import BeautifulSoup
import os

NotepadWindow = tk.Tk() 
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
    word_count = len(words)
    
    lines = text.split('\n')
    line_count = len(lines) - 1  # Subtract 1 because of the extra newline at the end
    
    char_count = len(text) - 1  # Subtract 1 to exclude the final newline character

    word_count_label.config(
        text=f"Words: {word_count} | Lines: {line_count} | Characters: {char_count}"
    )

def on_release(event):
    sync_preview_scroll(event)
    count_words()

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

help_button = ttk.Button(ToolFrame, text="Help", style="help.TButton", width=5)
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
edit_menu.add_command(label="Undo", command=Text_Box.edit_undo)
edit_menu.add_command(label="Redo", command=Text_Box.edit_redo)

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

NotepadWindow.mainloop()