[33mcommit 73a755319a95e2c593f5fdd0afbacded9fd790e0[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mNotepadStyle[m[33m, [m[1;31morigin/NotepadStyle[m[33m)[m
Author: Harsimran <hsj030609@gmail.com>
Date:   Thu Apr 24 13:42:45 2025 +0800

    FIXed Style tag issue ad added in undo redo buttons

[1mdiff --git a/main.py b/main.py[m
[1mindex 65e9ce3..18ee4cd 100644[m
[1m--- a/main.py[m
[1m+++ b/main.py[m
[36m@@ -1,13 +1,20 @@[m
 import tkinter as tk # Getting tkinter into the program[m
[32m+[m[32mfrom tkinter import ttk[m
 from tkinter import filedialog[m
 from tkinter import messagebox[m
 from tkhtmlview import HTMLLabel[m
 import markdown[m
[32m+[m[32mimport re[m
[32m+[m[32mfrom bs4 import BeautifulSoup[m
 [m
 NotepadWindow = tk.Tk()[m
 NotepadWindow.title("Note Editor")[m
 NotepadWindow.state("zoomed") [m
 [m
[32m+[m[32mstyle = ttk.Style()[m
[32m+[m[32mstyle.configure("TButton", padding=6, relief="flat", background="#dbeafe", font=("Helvetica", 10))[m
[32m+[m
[32m+[m
 #Set variable for the file name to False, when first starting the program[m
 global open_status_name [m
 open_status_name = False[m
[36m@@ -32,7 +39,7 @@[m [mdef Opening():[m
     Text_Box.delete("1.0", tk.END)[m
     #Grab The file name[m
     text_file = filedialog.askopenfilename(initialdir="C:/Notes", title="Open a File", filetypes=(("Text Files", "*.txt"),("All Files", "*.*")))[m
[31m-    [m
[32m+[m[32m    Window_title = text_file[m
     #Check if there is a file name and if yes, make it global[m
     if text_file:[m
         global open_status_name [m
[36m@@ -41,7 +48,7 @@[m [mdef Opening():[m
     name = text_file[m
     Status_bar.config(text=f"{name}    ")[m
     name = name.replace("C:/Users/", "") #Removing the C:/ Prefix[m
[31m-    NotepadWindow.title(f"{name} - Note Editor")[m
[32m+[m[32m    NotepadWindow.title(f"{Window_title} - Note Editor")[m
 [m
     # Load File Content[m
     text_file = open(text_file, "r")[m
[36m@@ -99,10 +106,13 @@[m [mdef insert_markdown(tag):[m
             # Replace the selected text with HTML underline tags (Cuz no default one in Markdown)[m
             Text_Box.replace(tk.SEL_FIRST, tk.SEL_LAST, f"<u>{selected}</u>")[m
 [m
[31m-    except tk.TclError:[m
[31m-        # If no text is selected, [m
[31m-        pass # Can ignore and continue on [m
[32m+[m[32m        elif tag == "font-size":[m
[32m+[m[32m            # Change the font size[m[41m [m
[32m+[m[32m            size = font_choice.get()  # Get the font size from the StringVar[m
[32m+[m[32m            Text_Box.replace(tk.SEL_FIRST, tk.SEL_LAST, f'<span style="font-size:{size}px">{selected}</span>')  # Use `size` here[m
 [m
[32m+[m[32m    except tk.TclError:[m
[32m+[m[32m        pass  # If no text is selected, just ignore[m
 [m
 # Toolbar Frame (Putting this first so that its top)[m
 ToolFrame = tk.Frame(NotepadWindow)[m
[36m@@ -123,7 +133,7 @@[m [mMainFrame.columnconfigure(1, weight=1)[m
 text_frame = tk.Frame(MainFrame)[m
 text_frame.grid(row=0, column=0, sticky="nsew")[m
 [m
[31m-text_scroll = tk.Scrollbar(text_frame)[m
[32m+[m[32mtext_scroll = ttk.Scrollbar(text_frame)[m
 text_scroll.pack(side="right", fill="y")[m
 [m
 Text_Box = tk.Text(text_frame, font=("Helvetica", 16),selectbackground="yellow", selectforeground="black", undo=True, yscrollcommand=text_scroll.set, wrap="word")[m
[36m@@ -131,40 +141,82 @@[m [mText_Box.pack(pady=20, padx=20, fill="both", expand=True)[m
 text_scroll.config(command=Text_Box.yview)[m
 [m
 [m
[31m-# Buttons for bolding italicing and underlining[m
[31m-bold_btn = tk.Button(ToolFrame, text="Bold", command=lambda: insert_markdown("**"))[m
[31m-bold_btn.pack(side="left", padx=5, pady=5)[m
[32m+[m[32m# Create a style object[m
[32m+[m[32mstyle = ttk.Style()[m
 [m
[31m-italic_btn = tk.Button(ToolFrame, text="Italic", command=lambda: insert_markdown("*"))[m
[31m-italic_btn.pack(side="left", padx=5, pady=5)[m
[32m+[m[32m# Define custom styles for bold, italic, and underline[m
[32m+[m[32mstyle.configure('Bold.TButton', font=('Helvetica', 14, 'bold'))[m
[32m+[m[32mstyle.configure('Italic.TButton', font=('Helvetica', 14, 'italic'))[m
[32m+[m[32mstyle.configure('Underline.TButton', font=('Helvetica', 14, 'underline'))[m
 [m
[31m-underline_btn = tk.Button(ToolFrame, text="Underline", command=lambda: insert_markdown("<u></u>"))[m
[31m-underline_btn.pack(side="left", padx=5, pady=5)[m
[32m+[m[32m# Buttons for bolding, italicing, and underlining[m
[32m+[m[32mbold_btn = ttk.Button(ToolFrame, text="B", style="Bold.TButton")[m
[32m+[m[32mbold_btn.pack(side="left", padx=5, pady=10, ipadx=5, ipady=10)[m
 [m
[31m-# Function to update the preview[m
[31m-def update_preview(event=None):  # Binding event as KeyRelease[m
[31m-    print("update_preview triggered")  # To see if fucn is called properly [m
[31m-    markdown_text = Text_Box.get("1.0", tk.END)     # Get all the text from the Text_Box [m
[32m+[m[32mitalic_btn = ttk.Button(ToolFrame, text="I", style="Italic.TButton")[m
[32m+[m[32mitalic_btn.pack(side="left", padx=5, pady=10, ipadx=5, ipady=10)[m
 [m
[31m-    # Check if the text contains a style tag ('<style='). If it does, ignore updating the preview.[m
[31m-    if "<style=" in markdown_text:[m
[31m-        print("Style tag detected. Skipping preview update.")  # print a response [m
[31m-        return  # Stop the HTML preview fro updating. Otherwise need to restart [m
[32m+[m[32munderline_btn = ttk.Button(ToolFrame, text="U", style="Underline.TButton")[m
[32m+[m[32munderline_btn.pack(side="left", padx=5, pady=10, ipadx=5, ipady=10)[m
 [m
[31m-    try:[m
[31m-        # convert the Markdown into HTML[m
[31m-        html_content = markdown.markdown(markdown_text)[m
[31m-        [m
[31m-        # Remove whitespaces [m
[31m-        if html_content.strip():[m
[31m-            # If got something in the HTML content update preview [m
[31m-            html_preview.set_html(html_content)[m
[31m-        else:[m
[31m-            # otherwise show this message [m
[31m-            print("Generated HTML content is empty.") [m
[32m+[m[32mundo_button = ttk.Button(ToolFrame, text="Undo", command=Text_Box.edit_undo)[m
[32m+[m[32mundo_button.pack(side="left", padx=5, pady=10, ipadx=5, ipady=10)[m
[32m+[m
[32m+[m[32mredo_button = ttk.Button(ToolFrame, text="Redo", command=Text_Box.edit_redo)[m
[32m+[m[32mredo_button.pack(side="left", padx=5, pady=10, ipadx=5, ipady=10)[m
[32m+[m
[32m+[m[32mcopy_button = ttk.Button(ToolFrame, text="Copy")[m
[32m+[m[32mcopy_button.pack(side="left", padx=5, pady=10, ipadx=5, ipady=10)[m
[32m+[m
[32m+[m[32mpaste_button = ttk.Button(ToolFrame, text="Paste")[m
[32m+[m[32mpaste_button.pack(side="left", padx=5, pady=10, ipadx=5, ipady=10)[m
[32m+[m
[32m+[m
[32m+[m[32mdef update_preview(event=None):[m
[32m+[m[32m    markdown_text = Text_Box.get("1.0", tk.END)[m
[32m+[m
[32m+[m[32m    lines = markdown_text.splitlines()[m
[32m+[m[32m    safe_lines = [][m
[32m+[m[32m    skipping = False[m
 [m
[31m-    except Exception as e:  # If got error, take the error as "e"[m
[31m-        print(f"Error generating HTML preview: {e}")  # Print the error message[m
[32m+[m[32m    for line in lines:[m
[32m+[m[32m        if re.search(r'<\w+\s+style=.*?>', line) and not re.search(r'</\w+>', line):[m
[32m+[m[32m            skipping = True[m
[32m+[m[32m            continue[m
[32m+[m
[32m+[m[32m        if skipping:[m
[32m+[m[32m            if re.search(r'</\w+>', line):[m
[32m+[m[32m                skipping = False[m
[32m+[m[32m            continue[m
[32m+[m
[32m+[m[32m        safe_lines.append(line)[m
[32m+[m
[32m+[m[32m    filtered_text = "\n".join(safe_lines)[m
[32m+[m
[32m+[m[32m    try:[m
[32m+[m[32m        html_content = markdown.markdown(filtered_text)[m
[32m+[m[32m        soup = BeautifulSoup(html_content, "html.parser")[m
[32m+[m
[32m+[m[32m        ALLOWED_STYLES = ["font-size", "color"][m
[32m+[m[32m        for tag in soup.find_all(True):[m
[32m+[m[32m            if "style" in tag.attrs:[m
[32m+[m[32m                styles = tag["style"].split(";")[m
[32m+[m[32m                clean_styles = [][m
[32m+[m[32m                for s in styles:[m
[32m+[m[32m                    s = s.strip()[m
[32m+[m[32m                    for allowed in ALLOWED_STYLES:[m
[32m+[m[32m                        if s.startswith(allowed):[m
[32m+[m[32m                            clean_styles.append(s)[m
[32m+[m[32m                if clean_styles:[m
[32m+[m[32m                    tag["style"] = "; ".join(clean_styles)[m
[32m+[m[32m                else:[m
[32m+[m[32m                    del tag["style"][m
[32m+[m
[32m+[m[32m        final_html = str(soup)[m
[32m+[m[32m        html_preview.set_html(final_html)[m
[32m+[m
[32m+[m[32m    except Exception as e:[m
[32m+[m[32m        print(f"Error generating HTML preview: {e}")[m
 [m
 [m
 # Bind the function to key release in the Text_Box[m
[36m@@ -182,6 +234,21 @@[m [mhtml_preview.pack(pady=20, padx=20, ipadx=150, fill="both", expand=True)[m
 TopMenuBar = tk.Menu(NotepadWindow)[m
 NotepadWindow.config(menu=TopMenuBar)[m
 [m
[32m+[m[32m# Set up OptionMenu for font size[m
[32m+[m[32mfont_choice = tk.StringVar()[m
[32m+[m[32mfont_choice.set("12")  # Set default value to string[m
[32m+[m[32mfont_size_options = [str(size) for size in range(12, 42, 2)][m
[32m+[m
[32m+[m[32mfont_size_menu = ttk.OptionMenu(ToolFrame, font_choice, *font_size_options)[m
[32m+[m[32mfont_size_menu.pack(side="left", padx="10", pady="5", ipady="20")[m
[32m+[m
[32m+[m
[32m+[m[32mdef change_font_size(*args):[m
[32m+[m[32m    insert_markdown("font-size")[m
[32m+[m
[32m+[m[32m# Bind the function to handle changes in selection[m
[32m+[m[32mfont_choice.trace("w", change_font_size)[m
[32m+[m
 #Adding in File Menu into the Menu Bar[m
 file_menu = tk.Menu(TopMenuBar, tearoff=False)[m
 TopMenuBar.add_cascade(label="File", menu=file_menu)[m
