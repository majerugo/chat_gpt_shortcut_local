# Chat gpt shortcut

This script is a shortcut to use gpt3 by just selecting text and pressing a shortcut.
This will send the text to the gpt3 engine and put the result in your clipboard.

## Requirements

### Warning

`keybord` library force you to use `sudo` to run the script.
So you have to be careful with the script you run and to sudo pip install all the libraries.

```bash
sudo pip install openai # OpenAI API
sudo pip install keyboard # Keyboard shortcuts
sudo apt-get install xclip # Clipboard
```

## Setup


Create an account on https://platform.openai.com/docs/overview and get your API key.
After that put your API key in a environment variable called OPENAI_API_KEY.

You need to be root to set the environment variable otherwise the script will not be able to access it.

```bash
sudo -s
export OPENAI_API_KEY='your_api_key'
```

If you doesn't want to put your API key in a environment variable you can call script with the argument `--api_key` or `-k`.

```bash
sudo python chat_gpt_shortcut.py --api_key your_api_key

```

After that you can run the script with python.

```bash
sudo python chat_gpt_shortcut.py
```

## Usage

Select some text `ctrl + c` and press the shortcut `ctrl + alt + a` to send the text to the gpt3 engine.
The result will be put in your clipboard.

If the program is running without argument it will start a new conversation.
This will create a new text file in the `conversations` folder.

To leave the program you can press `esc`.

It exists one argument `--histo` to give a previous conversation to the engine.
This argument is a path to a text file with the conversation.

```bash
sudo python chat_gpt_shortcut.py --histo path_to_file
```

For more information about the script you can use the help argument.

```bash
sudo python chat_gpt_shortcut.py --help
```