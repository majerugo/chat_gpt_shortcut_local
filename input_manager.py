import subprocess

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