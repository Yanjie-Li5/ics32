# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Yanjie Li
# yanjiel5@uci.edu
# 70714268
import command_parser
import os
from pathlib import Path

#Notice that, since the intructions don't include any 

#Initialization
current_directory = script_path = Path(__file__).resolve().parent
os.chdir(current_directory)

def main():
    loaded_notebook = None #this will a notebook object from provided module
    loaded_path = None #this will store a path object from pathlib (this might be the directory or path to file directly)
    running = ""
    while(running.upper() != "Q"):
        if loaded_notebook is not None:
            print("File is loading, you can use E and P commands now...")
        #user_input = input("Please enter the command...\n")
        user_input = input()
        if user_input.upper() != "Q": #check Q command
            if user_input[0:1].upper() == "E":#check E command                                                   #\0_0/ what can i say: module programming time
                command_parser.e_command(user_input,loaded_notebook,loaded_path)# do e command
                print("Edits are saved...")
            elif user_input[0:1].upper() == "P":#check P command
                command_parser.p_command(user_input,loaded_notebook)# do p command
            else: 
                information = command_parser.parser(user_input) #for C,O,D,Q commands; this generate a tuple with 0:command_type, 1:fin_directory(path object), 2:option, 3:diary_name
                notebook_obj = command_parser.command_type_checker(information,loaded_notebook) #preserve the notebook object
                if loaded_notebook is None and user_input[0:1].upper() == "O": 
                    loaded_notebook = notebook_obj
                    loaded_path = information[1] # this will store path to file directly (pathlib object)
                elif loaded_notebook is None and user_input[0:1].upper()=="C":
                    loaded_notebook = notebook_obj # this will store directory, or the intended path's directory, parent or that folder... (pathlib object)
                    loaded_path = information[1] / (information[3]+".json") #need modify path since this is the first time (pathlib object)
        else:
            running = user_input
        print()

if __name__=="__main__":
    main()
    print("End")

#Check Section, Ignore This
#C "Z:\ICS32\Assignment 1 - Diary\a1-diary-starter" -n my_diary
#C "Sub" -n my_diary
#D "Z:\ICS32\Assignment 1 - Diary\a1-diary-starter\my_diary.json"
#D "Sub\2.txt"
#D "Sub\my_diary.json"
#O "Z:\ICS32\Assignment 1 - Diary\a1-diary-starter\my_diary.json"
#E -usr Bob -pwd "2"
#E -usr jay -pwd "1"
#E -add "I had such a cool day at Six Flags with my friends"
#E -add "this is for P test" -add "another input" -add "this is the last"
#P -bio -usr -diary 0
