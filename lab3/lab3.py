#lab3.py

# Starter code for lab 3 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.
# Please see the README in this repository for the requirements of this lab exercise

# Yanjie Li
# yanjiel5@uci.edu
# 70714268

from pathlib import Path

directory = Path(__file__).resolve().parent
file_path = directory / "pynote.txt"
file_initialization = open(file_path, "w")
file_initialization.write("I can't believe this program works!\nWow, two notes and it's still working. Huh.\n")
file_initialization.close()

def print_note():
    print("="*20)
    file_out = open(file_path,"r")
    content = file_out.readlines()
    for v in content:
        print(v)
    file_out.close()
    print("="*20)

def add_notes():
    new_note = ""
    while (new_note !="/q"):
        new_note = input("Please enter a new note (enter '/q' to exit, '/p' to print):")
        if (new_note =="/p"):
            print_note()
        elif (new_note !="/q"):
            add_line(new_note)

def add_line(new_line):
    file_in = open(file_path,"a")
    file_in.write(new_line+"\n")
    file_in.close()

def main():
    print("Welcome to PyNote!\nHere are your notes:\n")
    print_note()
    add_notes()

    


if __name__ == "__main__":
    main()
    print("End of this program")
    print("="*20)
