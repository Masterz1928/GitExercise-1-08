import tkinter as tk
from tkcalendar import Calendar
from tkinter import ttk,messagebox,colorchooser
import os
from datetime import date,datetime
import zipfile
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from tkinter import ttk, messagebox
import tkinter as tk
import threading 

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

def deleting_notes():
    selected_files = file_listbox.curselection() #Get the file that the user selected 
    if not selected_files: # IF no files are selected, then do this  
        messagebox.showwarning("No selection", "Select a file to delete.") #Prompt the User
        return #Basically telling python to stop runninng this part and go out of this block of code 
    file_delete_name = file_listbox.get(selected_files[0]) # Since the selected_files variable contains a tuple, we take the first value e.g. (1,) 
    confirm = messagebox.askyesno("Delete?", f"Are you sure you want to delete '{file_delete_name}'?")
    if confirm:
        os.remove(os.path.join(folder_path, file_delete_name)) # Removes the file 
        update_file_list() #Updates the Listbox 


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
clear_search_button.place(relx=0.9, rely=0.5, anchor="center")  # Position it next to the search bar`

update_file_list()

##########################################################################
import mimetypes
import webbrowser

# Defines permission 
# metadata - view file names adn metadata 
#drive.file uploading files 
SCOPES = ["https://www.googleapis.com/auth/drive.metadata.readonly", "https://www.googleapis.com/auth/drive.file"]

# variable to store instance of authentication 
service = None

#Creating a function for authentication 
def authenticate_google_account():
    # Use global var 
    global service  
    creds = None
    # if token.json exsits, use that instead of loggin in (No need to relog in) 
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        # If credentials are invalid or expired but we have a fresh token, refresh them.
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get script's folder
            # path to credential.json
            CREDENTIALS_PATH = os.path.join(BASE_DIR, "credentials.json")
            # Sets up the log in flow and request permission for necessary permissions
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            # Opens a browser  window (port=0 means any free port)
            # save and successful login as creds 
            creds = flow.run_local_server(port=0)
        
        # Save the credentials to token.json 
        with open("token.json", "w") as token:
            # save as json file 
            token.write(creds.to_json())
    
    # connect the progrram to the google drive API 
    service = build("drive", "v3", credentials=creds)



# Creating a function to get files
def list_files(service):
    try:
        # get up to 10 files 
        # if there are more than to the nextpageToken will bring out the other set 
        # files(id, name) - gives us name and id of each file
        results = service.files().list(pageSize=10, fields="nextPageToken, files(id, name)").execute()

        # if there are files, get that, otherwise, just return back an empty list 
        items = results.get("files", [])
        # if no items are found 
        if not items:
            print("No files found.")
            return
        print("Files:")
        # go thorugh each file in the list and display the name + id 
        for item in items:
            print(f"{item['name']} ({item['id']})")

    # something does wrong show the error 
    except HttpError as error:
        print(f"An error occurred: {error}")

# Creating a function to upload files to Google Drive 
def upload_file_to_drive(service, filename, filepath, folder_id=None):
    try:
        mime_type, _ = mimetypes.guess_type(filename)
        if mime_type is None:
            # if cant guess file type then we set it to a binary file 
            mime_type = 'application/octet-stream'

        # what to name the file in drive 
        file_metadata = {'name': filename}

        if folder_id:
            # parent is to spesify which folder on the drive 
            file_metadata['parents'] = [folder_id]
        
        # handling file upload + path + what kind of file its receiving 
        media = MediaFileUpload(filepath, mimetype=mime_type)
        # actual uploading.  using service to interact with API 
        # sends the file's meta data (names/parent folder) and get bacc the id 
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        
        print(f"Uploaded '{filename}' with file ID: {file.get('id')}")
        messagebox.showinfo("Uploaded", f"Uploaded '{filename}'")
    except HttpError as error:
        print(f"An error occurred: {error}")

#Creating a function to create folder  
def create_or_get_folder(service, folder_name="MMU Study Buddy Files"):
    # search for the folder with the name "MMU Study Buddy Files"
    results = service.files().list(
    # Using mimeType='application/vnd.google-apps.folder to only search for folders 
    # feild tells the API to return the name and the ID 
        q=f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'", 
        fields="files(id, name)"
    ).execute()
    # get the files, if no files then retunr empty list 
    items = results.get("files", [])
    
    if items:
        # Get the ID from the folder from the first result
        # the [0] is only for first folder (since we only have 1 folder ) 

        folder_id = items[0]['id']
        print(f"Folder '{folder_name}' found with ID: {folder_id}")
    # If dun have the folder 
    else:
        #Create the folder with the folder name adn MIME type 
        file_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = service.files().create(body=file_metadata, fields='id').execute()
        # get ID and print 
        folder_id = folder.get('id')
        print(f"Folder '{folder_name}' created with ID: {folder_id}")
    # to allow other func to use the folder_id var 
    return folder_id

# Creaing the main part of the code that the user interacts with and bind to button 
def main_api():
    # show all files in the folder dir 
    def show_files():
        folder_path = r"C:\Notes"
        try:
            # list the files out
            files = os.listdir(folder_path)
            # filters out the files form the dictionary 
            files = [file for file in files if os.path.isfile(os.path.join(folder_path, file))]
            # clear list box 
            file_listbox.delete(0, tk.END)
            # insert all of the filesinto the listbox 
            for file in files:
                file_listbox.insert(tk.END, file)
        except FileNotFoundError:
            print("The folder path doesn't exist.")

    Upload_Option = tk.Toplevel(root)
    Upload_Option.geometry("350x550")
    Upload_Option.title("File Listbox")
    
    show_files()
    # Creating a function to upload user's selection of folders 
    def User_Selection_Of_Upload_File():
        global service
        # if the user didnt sign in
        if service is None:
            messagebox.showerror("Error", "You're not signed in. Please sign in first.")
            print(service)
            return
        # get user selection 
        selection = file_listbox.curselection()
        if selection:
            # take first selection 
            index = selection[0]
            # gets the selected file name 
            filename = file_listbox.get(index)
            # gets the file path 
            filepath = os.path.join(r"C:\Notes", filename)
            
            # then upload the file by calling the create or get folder func 
            folder_id = create_or_get_folder(service)
            # to avoid lag or inresponsive behavoir 
            threading.Thread(target=upload_file_to_drive, args=(service, filename, filepath, folder_id)).start()
        else:
            messagebox.showerror("No selected File","No file selected for upload.")
    # create a function to list out the file that have been uuploaded 
    def list_files_from_drive(service):
        try:
            # either create of finds the MMu study buddy folder 
            folder_id = create_or_get_folder(service)
            # find the files in the MMu study buddy folder 
            query = f"'{folder_id}' in parents and trashed = false"
            # gets the file that match, and gets the file name by searching in the main drive space 
            results = service.files().list(
                q=query,
                fields="files(name)",
                spaces="drive"
            ).execute()
            # gets the files or return empty list if dont have 
            files = results.get('files', [])
            return [f["name"] for f in files]
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []
        

    def open_drive_files_window():
        global service
        if service is None:
            messagebox.showerror("Error", "You're not signed in.")
            return

        files = list_files_from_drive(service)
        
        if not files:
            messagebox.showinfo("No Files", "No files found in your Drive folder.")
            return

        listboxuploadedfiles = tk.Listbox(Upload_Option, width=40)
        listboxuploadedfiles.pack(padx=10, pady=10, ipadx=25, ipady=75)

        for file in files:
            listboxuploadedfiles.insert(tk.END, file)

    def open_drive():
        webbrowser.open("https://drive.google.com/drive/my-drive")



    ReloadButton = ttk.Button(Upload_Option, text="Reload Files", command=show_files)
    ReloadButton.pack(pady=10)

    UploadButton = ttk.Button(Upload_Option, text="Upload File", command=User_Selection_Of_Upload_File)
    UploadButton.pack(pady=10)

    Todrivebutton = ttk.Button(Upload_Option, text="Go to Google Drive", command=open_drive)
    Todrivebutton.pack(pady=10)


    def logout():
        global service
        print("Logging out...")
        service = None
        if os.path.exists("token.json"):
            os.remove("token.json")
        messagebox.showinfo("Logged Out", "You have been logged out successfully.")

    def on_closing():
        if messagebox.askyesno("Sign Out", "Are you sure you want to sign out?"):
            logout()
            UploadButton.config(state="disabled")
            LogOutButton.config(state="disabled")
            ShowUploadedFilesButton.config(state="disabled")
            messagebox.showinfo("Goodbye", "You have been signed out. You will need to sign in again next time.")
            Upload_Option.destroy()
        else:
            Upload_Option.destroy()
            main_api()  # Relaunch the program (user will remain signed in)
    
    LogOutButton = ttk.Button(Upload_Option, text="Log Out", command=on_closing)
    LogOutButton.pack(pady=10)

    ShowUploadedFilesButton = ttk.Button(Upload_Option, text="Show All Uploaded Files", command=open_drive_files_window)
    ShowUploadedFilesButton.pack(pady=10)


    service = authenticate_google_account()  # Authenticate once at the start
    UploadButton.config(state="normal")
    LogOutButton.config(state="normal")
    ShowUploadedFilesButton.config(state="normal")


#################################################################################################################################################


#three button for the new, open, delete function
button_frame = tk.Frame(home_frame, bg="white")
button_frame.pack(pady=15)

btn_new = tk.Button(button_frame, text="New", font=25, relief="flat", width=20, height=3)
btn_new.pack(side="left", padx=20)

btn_open = tk.Button(button_frame, text="Open", font=25, relief="flat", width=20, height=3)
btn_open.pack(side="left", padx=20)

btn_delete = tk.Button(button_frame, text="Delete", font=25, relief="flat", width=20, height=3,command=deleting_notes)
btn_delete.pack(side="left", padx=20)

btn_export = tk.Button(button_frame, text="Export All Notes", font=25, relief="flat", width=20, height=3, command=export_notes_with_format)
btn_export.pack(side="left", padx=20)# Adjust as needed

btn_upload = tk.Button(button_frame, text="Upload to Google Drive", font=25, relief="flat", width=20, height=3, command=main_api)
btn_upload.pack(side="left", padx=20)# Adjust as needed


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


