from conversation_logger import put_histo_in_file

import subprocess
import markdown
import webbrowser
import os
import tkinter as tk

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

def md_to_html(input):
    return markdown.markdown(input, extensions=["fenced_code", "codehilite"])

def refactor_histo(histo):
    """
    Put the history of the chat in the file
    args:
        histo: the history of the chat
        file: the file where to put the history
    """
    refactored_histo = []
    i = 1
    for msg in histo:
        if msg["role"] == "system":
            refactored_histo.append("##### System\n" + "" + msg["content"] + "\n")
        elif msg["role"] == "user":
            refactored_histo.append("##### You\n" + "" + msg["content"] + "\n")
        elif msg["role"] == "assistant":
            refactored_histo.append("##### ChatGPT3.5 turbo\n" + "" + msg["content"] + "\n")
        i += 1
    return refactored_histo


def display_new_response(output, histo_parse, filename):
    """
    Display the new response
    args:
        output: the output of GPT-3
        histo_parse: the history of the chat
    """
    put_histo_in_file(histo_parse, filename)
    tab_count = filename.count("/")
    filename = filename.split("/")[tab_count - 1].split(".")[0]
    refactored_histo = refactor_histo(histo_parse)
    refactored_histo.append("##### ChatGPT3.5 turbo\n" + output)

    # print("\n".join(refactored_histo))

    # Display the new response
    html_text = md_to_html("\n".join(refactored_histo))
    file = "conversations_html/" + filename + ".html"
    file = os.path.abspath(file)
    
    f = open(file, "w")
    f.write(html_text)
    f.close()
    webbrowser.open("file://" + file)
    return file