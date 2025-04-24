import tkinter as tk # Getting tkinter into the program
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkhtmlview import HTMLLabel
import markdown
import re
from bs4 import BeautifulSoup

NotepadWindow = tk.Tk() 
NotepadWindow.title("Note Editor")
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
# Set Folder for Notes Location
folder_path = "C:/Notes"

#Creating Functions Here
# Creating New File 
def New_File():
    #Clearing text box
    Text_Box.delete("1.0", tk.END)
    # Adding in a title 
    NotepadWindow.title("New Note")
    #Adding status bar for display
    Status_bar.config(text="New File    ")
    global open_status_name 
    open_status_name = False

# Creating a opening function
def Opening():
    #Clearing text box
    Text_Box.delete("1.0", tk.END)
    #Grab The file name
    text_file = filedialog.askopenfilename(initialdir="C:/Notes", title="Open a File", filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
    Window_title = text_file
    #Check if there is a file name and if yes, make it global
    if text_file:
        global open_status_name 
        open_status_name = text_file
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
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Notes", title="Save File As", filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
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
    try:
        # Get the currently selected text from the Text_Box widget
        selected = Text_Box.get(tk.SEL_FIRST, tk.SEL_LAST)

        # If the tag is for bold or italic (markdown)
        if tag in ["**", "*"]:
            # Replace the selected text with the tag
            Text_Box.replace(tk.SEL_FIRST, tk.SEL_LAST, f"{tag}{selected}{tag}")

        # If the tag is for underline (HTML)
        elif tag == "<u></u>":
            # Replace the selected text with HTML underline tags (Cuz no default one in Markdown)
            Text_Box.replace(tk.SEL_FIRST, tk.SEL_LAST, f"<u>{selected}</u>")

        elif tag == "font-size":
            # Change the font size 
            size = font_choice.get()  # Get the font size from the StringVar
            Text_Box.replace(tk.SEL_FIRST, tk.SEL_LAST, f'<span style="font-size:{size}px">{selected}</span>')  # Use `size` here

    except tk.TclError:
        pass  # If no text is selected, just ignore

# Toolbar Frame (Putting this first so that its top)
ToolFrame = tk.Frame(NotepadWindow, bg="#3538d4")
ToolFrame.pack(fill="x", side="top")


# Create main frame
# (Putting the Text typing area and the scroll bar in the same area)
# Main container frame
MainFrame = tk.Frame(NotepadWindow, background="red")
MainFrame.pack(pady=0, padx=5, fill="both", expand=True)

# 2 equal columns
MainFrame.rowconfigure(0, weight=1)
MainFrame.columnconfigure(0, weight=1)
MainFrame.columnconfigure(1, weight=1)

# Text Frame + Scrollbar
text_frame = tk.Frame(MainFrame)
text_frame.grid(row=0, column=0, sticky="nsew")

text_scroll = ttk.Scrollbar(text_frame)
text_scroll.pack(side="right", fill="y")

Text_Box = tk.Text(text_frame, font=("Helvetica", 16),selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="word", bd=2, relief="solid")
Text_Box.pack(pady=20, padx=20, fill="both", expand=True)

text_scroll.config(command=Text_Box.yview)


# Create a style object
style = ttk.Style()

# Define custom styles for bold, italic, and underline
style.configure('Bold.TButton', font=('Helvetica', 10, 'bold'), padding=(5, 5))
style.configure('Italic.TButton', font=('Helvetica', 10, 'italic'), padding=(5, 5))
style.configure('Underline.TButton', font=('Helvetica', 10, 'underline'), padding=(5, 5))
style.configure('Undo.TButton', font=('Helvetica', 10), padding=(10, 5))
style.configure('Redo.TButton', font=('Helvetica', 10), padding=(10, 5))
style.configure('Copy.TButton', font=('Helvetica', 10), padding=(10, 5))
style.configure('Paste.TButton', font=('Helvetica', 10), padding=(10, 5))

left_wrap = ttk.Frame(ToolFrame)
left_wrap.pack(side="left", padx=(20, 0))  # only push from left

bold_btn = ttk.Button(ToolFrame, text="B", style="Bold.TButton", width=10)
bold_btn.pack(side="left", padx=10, pady=10)

italic_btn = ttk.Button(ToolFrame, text="I", style="Italic.TButton", width=10)
italic_btn.pack(side="left", padx=10, pady=10)

underline_btn = ttk.Button(ToolFrame, text="U", style="Underline.TButton", width=10)
underline_btn.pack(side="left", padx=10, pady=10)

undo_button = ttk.Button(ToolFrame, text="Undo", style="Undo.TButton", width=10, command=Text_Box.edit_undo)
undo_button.pack(side="left", padx=10, pady=10)

redo_button = ttk.Button(ToolFrame, text="Redo", style="Redo.TButton", width=10,  command=Text_Box.edit_redo)
redo_button.pack(side="left", padx=10, pady=10)

copy_button = ttk.Button(ToolFrame, text="Copy" , style="Copy.TButton", width=10)
copy_button.pack(side="left", padx=10, pady=10)

paste_button = ttk.Button(ToolFrame, text="Paste", style="Paste.TButton", width=10)
paste_button.pack(side="left", padx=10, pady=10)


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

    try:
        html_content = markdown.markdown(filtered_text)
        soup = BeautifulSoup(html_content, "html.parser")

        ALLOWED_STYLES = ["font-size", "color"]
        for tag in soup.find_all(True):
            if "style" in tag.attrs:
                styles = tag["style"].split(";")
                clean_styles = []
                for s in styles:
                    s = s.strip()
                    for allowed in ALLOWED_STYLES:
                        if s.startswith(allowed):
                            clean_styles.append(s)
                if clean_styles:
                    tag["style"] = "; ".join(clean_styles)
                else:
                    del tag["style"]

        final_html = str(soup)
        html_preview.set_html(final_html)

    except Exception as e:
        print(f"Error generating HTML preview: {e}")


# Bind the function to key release in the Text_Box
Text_Box.bind("<KeyRelease>", update_preview)

# Preview Frame
preview_frame = tk.Frame(MainFrame, bg="white", bd=2, relief="solid")
preview_frame.grid(row=0, column=1, sticky="nsew")

html_preview = HTMLLabel(preview_frame, html="")
html_preview.pack(pady=0, padx=0, ipadx=150, fill="both", expand=True)

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
file_menu.add_command(label="Save as", command=Saving_File_As)
file_menu.add_command(label="Save", command=Saving_File)

#Adding editing menu 
edit_menu = tk.Menu(TopMenuBar, tearoff=False)
TopMenuBar.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Copy")
edit_menu.add_command(label="Paste")
edit_menu.add_command(label="Undo")
edit_menu.add_command(label="Redo")

#Adding a status bar (For referance)
Status_bar = tk.Label(NotepadWindow, text="Ready    ", anchor="e")
Status_bar.pack(fill="x", side="bottom", ipady=5)


NotepadWindow.mainloop()
