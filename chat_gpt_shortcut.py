import os
from openai import OpenAI
import keyboard
import subprocess
import argparse
import threading

def sumarrize(msg, file, text):
    """
    Summarize the text and put it in the file
    args:
        msg: the history of the chat
        file: the file where the history is stored
        text: the text to summarize
    """

    # Create request for GPT-3
    summary = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "sums it up:" + text}]
    )
    if (verbose):
        print("Summary:", summary.choices[0].message.content)
    msg.append({"role":"assistant", "content": summary.choices[0].message.content})
    put_histo_in_file(msg, file)

def send_request(text):
    """
    Send a request to GPT-3
    args:
        text: the text to send to GPT-3
    return:
        (the response of GPT-3, the history of the chat)
    """

    # Take history from file
    msg = parse_file_to_histo(file)

    # Create request for GPT-3
    msg.append({"role": "user", "content": text})

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=msg
    )
    if (verbose):
        print("Completion:", completion.choices[0].message.content)
    return (completion.choices[0].message.content, msg)

def get_selected_text():
    """
    Get the selected text in the clipboard
    return:
        the selected text
    """

    # Take the content of the clipboard and put it in a file
    f = open("/tmp/clipboard.txt", "w")
    subprocess.run(["xclip", "-selection", "clipboard", "-o"], stdout=f)
    f.close()

    # Read the content of this file
    f = open("/tmp/clipboard.txt", "r")
    selected_text = f.read()
    f.close()

    # Delete the file
    subprocess.run(["rm", "/tmp/clipboard.txt"])
    return selected_text

def put_text_in_clipboard(output):
    """
    Put the text in the clipboard
    args:
        output: the text to put in the clipboard
    """

    # echo $text | xclip -selection clipboard
    cmd1 = ["echo", output]
    process1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)

    cmd2 = ["xclip", "-selection", "clipboard"]
    process2 = subprocess.Popen(cmd2, stdin=process1.stdout, stdout=subprocess.PIPE)
    
    process1.stdout.close()
    print("Text copied to clipboard")

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
        output,msg = send_request(selected_text)

        thread = threading.Thread(target=sumarrize, args=(msg, file, output))
        thread1 = threading.Thread(target=put_text_in_clipboard, args=(output,))

        thread.start()
        thread1.start()

        thread.join()
        thread1.join()

def parse_file_to_histo(file):
    """
    Parse the file to get the history of the chat
    args:
        file: the file to parse
    return:
        the history of the chat
    """

    f = open(file, "r")
    lines = f.readlines()
    f.close()

    histo = []
    for line in lines:
        if line[0] == "S":
            histo.append({"role": "system", "content": line[2:]})
        elif line[0] == "U":
            histo.append({"role": "user", "content": line[2:]})
        elif line[0] == "A":
            histo.append({"role": "assistant", "content": line[2:]})
    return histo

def put_histo_in_file(histo, file):
    """
    Put the history of the chat in the file
    args:
        histo: the history of the chat
        file: the file where to put the history
    """

    f = open(file, "w")
    for msg in histo:
        if msg["role"] == "system":
            f.write("S: " + msg["content"])
        elif msg["role"] == "user":
            f.write("U: " + msg["content"])
        elif msg["role"] == "assistant":
            f.write("A: " + msg["content"])
    f.close()

# Create the file and the history
file = "conversations/conversation.txt"
histo = [{"role": "system", "content": "You are an engineer in computer science."}]

# Verbose mode
verbose = False

# Parse the arguments
parser = argparse.ArgumentParser(description='Shortcut for GPT-3')
parser.add_argument('--histo', help='Take a file as input and use it as history')
parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')
parser.add_argument('--api_key','-k', help='OpenAI API key')

args = parser.parse_args()

# Get history from file
if args.histo:
    file = args.histo
    histo = parse_file_to_histo(args.histo)
else:
    if not os.path.exists(file):
        f = open(file, "w")
        f.write("S: You are an engineer in computer science.")
        f.close()

# Verbose mode
if args.verbose:
    verbose = True

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
