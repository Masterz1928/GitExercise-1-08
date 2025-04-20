import tkinter as tk # Getting tkinter into the program
from tkinter import filedialog
from tkinter import messagebox

root = tk.Tk()
root.title("Note Editor")
root.geometry("1200x600")
#root.state("zoomed") *Not sure to make it zoomed or not yet, but writing it here for referance*

#Set variable for the file name to False, when first starting the program
global open_status_name 
open_status_name = False

#Creating Functions Here
# Creating New File 
def New_File():
    #Clearing text box
    Text_Box.delete("1.0", tk.END)
    # Adding in a title 
    root.title("New Note")
    #Adding status bar for display
    Status_bar.config(text="New File    ")
    global open_status_name 
    open_status_name = False

# Creating a opening function
def Opening():
    #Clearing text box
    Text_Box.delete("1.0", tk.END)
    #Grab The file name
    text_file = filedialog.askopenfilename(initialdir="C:/Users/Harsimran/Desktop/Documents/Notes", title="Open a File", filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
    
    #Check if there is a file name and if yes, make it global
    if text_file:
        global open_status_name 
        open_status_name = text_file
    #Updating Status bar 
    name = text_file
    Status_bar.config(text=f"{name}    ")
    name = name.replace("C:/Users/", "") #Removing the C:/ Prefix
    root.title(f"{name} - Note Editor")

    # Load File Content
    text_file = open(text_file, "r")
    File_Content = text_file.read()
    #Add it into the text box
    Text_Box.insert(tk.END, File_Content)
    #Then, Close the open file
    text_file.close()
# Creating a function to save a file as (in a .txt format) 
def Saving_File_As():
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/Users/Harsimran/Desktop/Documents/Notes", title="Save File As", filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))
    if text_file:
        #Update the status bar
        name = text_file
        Status_bar.config(text=f"Saved: {name}    ")
        name = name.replace("C:/Users/", "") #Removing the C:/ Prefix
        root.title(f"{name} - Note Editor")       

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
        Message_Pop.pack()
        Status_bar.config(text=f"Saved: {open_status_name}    ")
    else:
        Saving_File_As()


# Create main frame
# (Putting the Text typing area and the scroll bar in the same area)
MainFrame = tk.Frame(root)
MainFrame.pack(pady=5, padx=5, fill="both", expand=True)

#Creating scrollbar
text_scroll =tk.Scrollbar(MainFrame)
text_scroll.pack(side="right", fill="y")

#Creating The Text Area to type
Text_Box = tk.Text(MainFrame, width=90, height=25, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="word")
Text_Box.pack(pady=20, padx=20, fill="both", expand=True)
text_scroll.config(command=Text_Box.yview)

#Creating Menu Top menu bar
TopMenuBar = tk.Menu(root)
root.config(menu=TopMenuBar)

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
Status_bar = tk.Label(root, text="Ready    ", anchor="e")
Status_bar.pack(fill="x", side="bottom", ipady=5)


root.mainloop()
