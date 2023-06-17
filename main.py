import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import sqlite3
import difflib
from tkinter import ttk
from tkinter import scrolledtext

# Database Initialization
conn = sqlite3.connect('documents.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS documents
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              content TEXT)''')

# GUI Initialization
window = tk.Tk()
window.title("Plagiarism Checker")
window.configure(bg="#9d54b8")  # Set background color
window.geometry("400x400")  # Set window dimensions

# Function to center the window on the screen
def center_window():
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Center the window on the screen
center_window()
#function to open fille
def open_file():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            name = file_path.split('/')[-1]
            c.execute("INSERT INTO documents (name, content) VALUES (?, ?)", (name, content))
            conn.commit()
            messagebox.showinfo("Success", "File uploaded successfully.")
            update_document_list()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while opening the file:\n{str(e)}")
#function to check plagiarism
def check_plagiarism():
    try:
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            c.execute("SELECT id, name, content FROM documents")
            documents = c.fetchall()
            plagiarized_docs = []
            total_documents = len(documents)
            progress = 0
            progress_bar["maximum"] = total_documents
            progress_label.config(text="Checking...")
            for doc in documents:
                similarity = difflib.SequenceMatcher(None, content, doc[2]).ratio()
                if similarity >= 0.8:
                    plagiarized_docs.append(doc[1])
                progress += 1
                progress_bar["value"] = progress
                window.update_idletasks()
            if plagiarized_docs:
                messagebox.showinfo("Plagiarism Detected", "The file matches the following documents:\n\n" + "\n".join(plagiarized_docs))
            else:
                # Custom message box with increased size
                msg_box = tk.Toplevel(window)
                msg_box.title("No Plagiarism Detected")
                msg_box.geometry("400x300")  # Set the desired size
                msg_label = tk.Label(msg_box, text="The file is unique.", font=("Arial", 12))
                msg_label.pack(pady=20)
                ok_button = tk.Button(msg_box, text="OK", command=msg_box.destroy)
                ok_button.pack(pady=10)
                msg_box.transient(window)
                msg_box.grab_set()
                window.wait_window(msg_box)
            progress_bar["value"] = 0
            progress_label.config(text="")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while checking plagiarism:\n{str(e)}")
# function to clear datbase
def clear_database():
    try:
        result = messagebox.askyesno("Clear Database", "Are you sure you want to clear the database?")
        if result == tk.YES:
            c.execute("DELETE FROM documents")
            conn.commit()
            messagebox.showinfo("Database Cleared", "The database has been cleared.")
            update_document_list()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while clearing the database:\n{str(e)}")
#function to delete_document
def delete_document():
    try:
        selected_indices = document_list.curselection()
        if selected_indices:
            selected_id = document_list.get(selected_indices[0])
            result = messagebox.askyesno("Delete Document", "Are you sure you want to delete this document?")
            if result == tk.YES:
                c.execute("DELETE FROM documents WHERE id=?", (selected_id,))
                conn.commit()
                messagebox.showinfo("Document Deleted", "The document has been deleted.")
                update_document_list()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while deleting the document:\n{str(e)}")
#function to update document
def update_document_list():
    try:
        c.execute("SELECT id, name FROM documents")
        documents = c.fetchall()
        document_list.delete(0, tk.END)
        for doc in documents:
            document_list.insert(tk.END, f"{doc[0]} - {doc[1]}")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while updating the document list:\n{str(e)}")

#upload button to upload document
upload_button = tk.Button(window, text="Upload Document", command=open_file, width=20)
upload_button.pack(pady=10)
#check button to check plagiarism
check_button = tk.Button(window, text="Check Plagiarism", command=check_plagiarism, width=20)
check_button.pack(pady=10)
#clear database button to clear database
clear_button = tk.Button(window, text="Clear Database", command=clear_database, width=20)
clear_button.pack(pady=10)
#list_box
document_list = tk.Listbox(window, width=50, height=10)
document_list.pack(pady=10)
#delete button to delete document
delete_button = tk.Button(window, text="Delete Document", command=delete_document, width=20)
delete_button.pack(pady=10)

progress_label = tk.Label(window, text="", width=30)
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(window, mode="determinate", length=300)
progress_bar.pack(pady=10)

update_document_list()

window.mainloop()
