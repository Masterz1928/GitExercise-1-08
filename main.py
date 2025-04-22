import tkinter as tk # Getting tkinter into the program
from tkinter import filedialog
from tkinter import messagebox
from tkhtmlview import HTMLLabel
import markdown

NotepadWindow = tk.Tk()
NotepadWindow.title("Note Editor")
NotepadWindow.state("zoomed") 

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
    
    #Check if there is a file name and if yes, make it global
    if text_file:
        global open_status_name 
        open_status_name = text_file
    #Updating Status bar 
    name = text_file
    Status_bar.config(text=f"{name}    ")
    name = name.replace("C:/Users/", "") #Removing the C:/ Prefix
    NotepadWindow.title(f"{name} - Note Editor")

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

    except tk.TclError:
        # If no text is selected, 
        pass # Can ignore and continue on 


# Toolbar Frame (Putting this first so that its top)
ToolFrame = tk.Frame(NotepadWindow)
ToolFrame.pack(fill="x", side="top")


# Create main frame
# (Putting the Text typing area and the scroll bar in the same area)
# Main container frame
MainFrame = tk.Frame(NotepadWindow)
MainFrame.pack(pady=5, padx=5, fill="both", expand=True)

# 2 equal columns
MainFrame.columnconfigure(0, weight=1)
MainFrame.columnconfigure(1, weight=1)

# Text Frame + Scrollbar
text_frame = tk.Frame(MainFrame)
text_frame.grid(row=0, column=0, sticky="nsew")

text_scroll = tk.Scrollbar(text_frame)
text_scroll.pack(side="right", fill="y")

Text_Box = tk.Text(text_frame, font=("Helvetica", 16),selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="word")
Text_Box.pack(pady=20, padx=20, fill="both", expand=True)
text_scroll.config(command=Text_Box.yview)


# Buttons for bolding italicing and underlining
bold_btn = tk.Button(ToolFrame, text="Bold", command=lambda: insert_markdown("**"))
bold_btn.pack(side="left", padx=5, pady=5)

italic_btn = tk.Button(ToolFrame, text="Italic", command=lambda: insert_markdown("*"))
italic_btn.pack(side="left", padx=5, pady=5)

underline_btn = tk.Button(ToolFrame, text="Underline", command=lambda: insert_markdown("<u></u>"))
underline_btn.pack(side="left", padx=5, pady=5)

# Function to update the preview
def update_preview(event=None):
    markdown_text = Text_Box.get("1.0", tk.END)
    html_content = markdown.markdown(markdown_text)
    html_preview.set_html(html_content)

# Bind the function to key release in the Text_Box
Text_Box.bind("<KeyRelease>", update_preview)

# Preview Frame
preview_frame = tk.Frame(MainFrame, bg="white", bd=5, relief="ridge")
preview_frame.grid(row=0, column=1, sticky="nsew")

html_preview = HTMLLabel(preview_frame, html="", bg="white")
html_preview.pack(pady=20, padx=20, ipadx=150, fill="both", expand=True)


#Creating Menu Top menu bar
TopMenuBar = tk.Menu(NotepadWindow)
NotepadWindow.config(menu=TopMenuBar)

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
