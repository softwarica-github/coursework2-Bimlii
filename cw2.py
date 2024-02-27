import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests

def fetch_headers(url):
    try:
        response = requests.get(url)
        return response.headers
    except requests.exceptions.RequestException as e:
        return f"Error fetching headers for {url}: {e}"

def directory_brute_force(url, wordlist):
    found_directories = []
    for directory in wordlist:
        full_url = f"{url}/{directory.strip()}"
        try:
            response = requests.get(full_url)
            if response.status_code == 200:
                found_directories.append(full_url)
        except requests.exceptions.RequestException as e:
            pass  # Skipping errors in GUI mode for brevity
    return found_directories

def display_source_code(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch source code from {url}. Status code: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching source code for {url}: {e}"

# GUI Functions
def perform_actions():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Error", "URL is required!")
        return
    
    output_text.delete(1.0, tk.END)  # Clear existing text
    
    if var_headers.get():
        headers = fetch_headers(url)
        output_text.insert(tk.END, f"Headers for {url}:\n{headers}\n\n")
    
    if var_dir_brute.get():
        wordlist = ['admin', 'backup', 'login', 'images', 'test']  # Example wordlist
        directories = directory_brute_force(url, wordlist)
        if directories:
            output_text.insert(tk.END, f"Found directories for {url}:\n{directories}\n\n")
        else:
            output_text.insert(tk.END, f"No directories found for {url}.\n\n")
    
    if var_source_code.get():
        source_code = display_source_code(url)
        output_text.insert(tk.END, f"Source code for {url}:\n{source_code[:1000]}\n\n")  # Display first 1000 characters for brevity

def clear_output():
    output_text.delete(1.0, tk.END)

# GUI setup
root = tk.Tk()
root.title("Web Enumeration Tool")

# URL entry
tk.Label(root, text="URL:").pack()
url_entry = tk.Entry(root, width=50)
url_entry.pack()

# Checkbuttons for actions
var_headers = tk.BooleanVar()
tk.Checkbutton(root, text="Fetch Headers", variable=var_headers).pack()
var_dir_brute = tk.BooleanVar()
tk.Checkbutton(root, text="Directory Brute Force", variable=var_dir_brute).pack()
var_source_code = tk.BooleanVar()
tk.Checkbutton(root, text="Display Source Code", variable=var_source_code).pack()

# Action button
action_button = tk.Button(root, text="Perform Actions", command=perform_actions)
action_button.pack()

# Clear Output button
clear_button = tk.Button(root, text="Clear Output", command=clear_output)
clear_button.pack()

# Output text area
output_text = scrolledtext.ScrolledText(root, height=15)
output_text.pack()

# Run the application
root.mainloop()
