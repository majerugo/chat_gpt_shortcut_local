import openai

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
    content = ""
    role = ""
    for line in lines:
        if line[0] == "S":
            if role == "":
                role = "system"
            else:
                histo.append({"role": role, "content": content})
                content = ""
                role = "system"
            content += line[3:]
        elif line[0] == "U":
            if role == "":
                role = "user"
            else:
                histo.append({"role": role, "content": content})
                content = ""
                role = "user"
            content += line[3:]
        elif line[0] == "A":
            if role == "":
                role = "assistant"
            else:
                histo.append({"role": role, "content": content})
                content = ""
                role = "assistant"
            content += line[3:]
        else:
            content += line
    histo.append({"role": role, "content": content})
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
            f.write("S: " + msg["content"]+ "\n")
        elif msg["role"] == "user":
            f.write("U: " + msg["content"]+ "\n")
        elif msg["role"] == "assistant":
            f.write("A: " + msg["content"]+ "\n")
    f.close()

def sumarrize(msg, file, text, verbose, client):
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
    