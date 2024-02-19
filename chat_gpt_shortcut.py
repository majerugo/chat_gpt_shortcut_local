from conversation_logger import parse_file_to_histo, sumarrize
from output_manager import put_text_in_clipboard, display_new_response
from input_manager import get_selected_text

import os
from openai import OpenAI
import keyboard
import argparse
import threading
import tkinter as tk
from tkhtmlview import HTMLText
from bs4 import BeautifulSoup

window = None

class HTMLViewerApp:
    def __init__(self, root, file):
        self.root = root
        self.file = file
        self.root.title("GPT answer")

       # Set background colors for Ubuntu-like terminal theme
        bg_color = "#2C001E"  # Dark purple background
        text_bg_color = "#2C001E"  # Dark purple background
        button_bg_color = "#4CAF50"  # Ubuntu-like green

        # Set text color for Ubuntu-like terminal theme
        text_color = "#D3D3D3"  # Light gray text
        input_color = "#E6E6FA"  # Light lavender input background

        # Configure root window
        root.configure(bg=bg_color)

        # Create an HTMLText widget for displaying HTML content
        self.html_text = HTMLText(root, wrap=tk.WORD, bg=text_bg_color, fg=text_color, insertbackground=text_color, highlightthickness=0)
        self.html_text.pack(expand=True, fill="both", padx=10, pady=10)

        # Create a frame for the text entry and button
        input_frame = tk.Frame(root, bg=bg_color)
        input_frame.pack(fill="x", side=tk.BOTTOM)

        # Create a text entry widget
        self.text_entry = tk.Entry(input_frame, bg=input_color, fg="black", highlightbackground=bg_color, highlightcolor=bg_color, font=('Helvetica', 14))
        self.text_entry.pack(side=tk.LEFT, expand=True, fill="both", padx=5)

        # Bind the <Return> event to the send_request function
        self.text_entry.bind("<Return>", lambda event: self.send_request())

        # Create a button to send the request with reduced vertical padding
        self.send_button = tk.Button(input_frame, text="Send request", command=self.send_request, bg=button_bg_color, fg="white", pady=5)
        self.send_button.pack(side=tk.RIGHT, expand=False, fill="both", padx=5)

        # Load initial HTML content from file
        self.load_html_content()

    def load_html_content(self):
        try:
            with open(self.file, "r", encoding="utf-8") as f:
                text = f.read()
                styled_html = f'<div style="background-color: #2C001E; color: #D3D3D3;">{text}</div>'
                # Parse HTML and modify <h5> text color
                
                soup = BeautifulSoup(styled_html, "html.parser")
                h5_tags = soup.find_all("h5")
                for h5_tag in h5_tags:
                    h5_tag["style"] = "color: green;"  # Change color to red
                modified_html = str(soup)
                self.html_text.set_html(modified_html)
                # Set the vertical scrollbar to the bottom position
                self.html_text.yview(tk.END)
        except FileNotFoundError:
            print(f"File not found: {self.file}")
    def send_request(self):
        # Get the text from the entry
        text = self.text_entry.get()
        self.text_entry.delete(0, tk.END)
        send_request_and_save(text)


def send_request_and_save(text):
    """
    Send a request to GPT-3
    args:
        text: the text to send to GPT-3
    """

    # Take history from file
    histo_parse = parse_file_to_histo(file)
    # Create request for GPT-3
    histo_parse.append({"role": "user", "content": text})
        
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=histo_parse
    )
    if (verbose):
        print("Completion:", completion.choices[0].message.content)
    output,histo_parse = (completion.choices[0].message.content, histo_parse)
    global window
    if clipboard:
        put_text_in_clipboard(output)
        sumarrize(histo_parse, file, output, verbose, client)
    else:
        f = display_new_response(output, histo_parse, file)
        sumarrize(histo_parse, file, output, verbose, client)
        if (window != None and window.winfo_exists()):
            window.destroy()
        window = tk.Tk()
        app = HTMLViewerApp(window, f)
        window.mainloop()

def on_key_event(e):
    """
    Function called when a key is pressed
    args:
        e: the event of the key pressed
    """

    if e.event_type == keyboard.KEY_DOWN and keyboard.is_pressed('ctrl+alt+a'):
        
        selected_text = get_selected_text()
        if verbose:
            if selected_text:
                print("Texte sélectionné :", selected_text)
            else:
                print("Aucun texte sélectionné")
        if selected_text:
            send_request_and_save(selected_text)

# Create the file and the history
file = "conversations/conversation.txt"
histo = [{"role": "system", "content": "You are an engineer in computer science."}]

# Verbose mode
verbose = False

# Output in clipboard
clipboard = False

# Parse the arguments
parser = argparse.ArgumentParser(description='Shortcut for GPT-3')
parser.add_argument('--api_key','-k', help='OpenAI API key')
parser.add_argument('--histo', help='Take a file as input and use it as history')
parser.add_argument('--verbose','-v', action='store_true', help='Verbose mode')
parser.add_argument('--clipboard', '-c', action='store_true', help='Save the output in the clipboard')

args = parser.parse_args()

# Get history from file
if args.histo:
    file = args.histo
    histo = parse_file_to_histo(args.histo)
else:
    f = open(file, "w")
    f.write("S: You are an engineer in computer science.\n")
    f.close()

# Verbose mode
if args.verbose:
    verbose = True

# Output in clipboard
if args.clipboard:
    clipboard = True

# Create the client
if args.api_key:
    client = OpenAI(api_key=args.api_key)
else:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

print("Press ctrl+alt+a to send the selected text to GPT-3")

# Listen to the keyboard
keyboard.hook(on_key_event)

# Wait for the user to press the escape key
keyboard.wait('esc')
