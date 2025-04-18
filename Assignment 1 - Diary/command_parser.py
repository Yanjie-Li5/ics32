# Starter code for assignment 1 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# Yanjie Li
# yanjiel5@uci.edu
# 70714268

from shlex import split
import notebook
import pathlib 
import sys
import json

loaded = False

def parser(user_input):
    command_line = split(user_input) #[Command type] [Directory] [[-]OPTION] [Name]
    command_line = placeholder(command_line)
    command_type = command_line[0]
    raw_Directory = command_line[1] # this could be an absolute or relative path
    fin_directory = directory_parser(raw_Directory) # this create a Path Object with abs. path
    option = command_line[2]
    diary_name = command_line[3]
    info = (command_type,fin_directory,option,diary_name) # a tuple store information
    return info

def directory_parser(raw_path):
    user_path = pathlib.Path(raw_path) #create path object from user's string
    if user_path.is_absolute():
        return user_path
    else:
        return pathlib.Path(raw_path).resolve()

def placeholder(alist): #Force to be length of 4
    length = len(alist)
    if length < 4:
        alist += ["Empty"] * (4-length)
        return alist
    else:
        return alist

def command_type_checker(info_tuple,OBJ): #0:command_type, 1:fin_directory, 2:option, 3:diary_name; OBJ is for loaded notebook
    command = info_tuple[0]
    directory = info_tuple[1] #this is a pathlib object, this could be a directory or direct to file
    diary_name = info_tuple[3]
    if command.upper() == "C": 
        return c_command(directory,diary_name,info_tuple)
    elif command.upper() == "D":
        d_command(directory,diary_name)
    elif command.upper() == "O":
        obj = o_command(directory)
        return obj # a notebook instantiation
    elif command.upper() == "P":
        p_command()
    else:
        print("Error command")

def c_command(directory,diary_name,info):
    if "Empty" in info:
        print("ERROR")
        return
    username_in = input("Please enter the user name of the notebook...")
    q_command(username_in)
    password_in = input("Please enter a password to protect access to the notebook...")
    q_command(password_in)
    bio_in = input("Please enter a brief description of the user...")
    q_command(bio_in)
    #def __init__(self, username: str, password: str, bio: str):
    new_notebook = notebook.Notebook(username=username_in, password=password_in, bio=bio_in)# create object
    if directory.suffix  != ".json":
        notebook_path = directory / (diary_name+".json")
    new_notebook.save(notebook_path) # create actually json file
    print(notebook_path, "CREATED")
    print("C command automatically loads the file created, please enter name and password...")
    return o_command(notebook_path)

def d_command(directory,diary_name):
    if directory.is_file() and directory.suffix == ".json":
        directory.unlink()
        print(directory,"DELETED")
    else:
        print("The file is not a .json file or the file does not exist...")

def o_command(directory): #accept a path direct to file not its dictionary
    if directory.is_file() and directory.suffix == ".json": # a dictionary
        nm = input("")
        q_command(nm)
        pw = input("")
        q_command(pw)
        with open(directory, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data["username"] == nm and data["password"] == pw:
                notebook_obj = notebook.Notebook("","","")
                notebook_obj.load(path=directory)
                print("Notebook loaded.")
                print(notebook_obj.username)
                print(notebook_obj.bio)
                return notebook_obj
            else:
                print("ERROR, enter name and password again...")
                return o_command(directory)
    else:
        print("The file doesn't exist or it is not a valid JSON file")

def q_command(input):
    if input.upper() == "Q":
        print("End")
        sys.exit()

def p_command(command_line,notebook_obj):
    command_combination = split(command_line[2:])
    for index in range(len(command_combination)):
        if command_combination[index] == "-usr":
            try:
                print(notebook_obj.username)
            except:
                print("Error, -usr")
                return
        elif command_combination[index] == "-pwd":
            try:
                print(notebook_obj.password)
            except:
                print("Error, -pwd")
                return    
        elif command_combination[index] == "-bio":
            try:
                print(notebook_obj.bio)
            except:
                print("Error, -bio")
                return 
        elif command_combination[index] == "-diaries":
            try:
                for i in range(len(notebook_obj.get_diaries())):
                    print(str(i)+":", notebook_obj.get_diaries()[i].get_entry())
            except:
                print("Error, -diaries")
                return
        elif command_combination[index] =="-diary":
            try:
                print(notebook_obj.get_diaries()[int(command_combination[index+1])].get_entry())
            except:
                print("Error, -diary [ID]")
                return
        elif  command_combination[index] == "-all":
            try:
                print(notebook_obj.username)
                print(notebook_obj.password)
                print(notebook_obj.bio)
                for i in range(len(notebook_obj.get_diaries())):
                    print(str(i)+":", notebook_obj.get_diaries()[i].get_entry())
            except:
                print("Error, -all")
                return

def e_command(command_line,notebook_obj,path): # [COMMAND] [INPUT] [[-]OPTION] [INPUT]
    command_combination = split(command_line[2:])
    for index in range(0,len(command_combination),2):
        if command_combination[index] == "-usr":
            try:
                notebook_obj.username = command_combination[index+1]
                notebook_obj.save(path)
            except:
                print("Error, -usr")
                return
        elif command_combination[index] == "-pwd":
            try:
                notebook_obj.password = command_combination[index+1]
                notebook_obj.save(path)
            except:
                print("Error, -pwd")
                return    
        elif command_combination[index] == "-bio":
            try:
                notebook_obj.bio = command_combination[index+1]
                notebook_obj.save(path)
            except:
                print("Error, -bio")
                return 
        elif command_combination[index] == "-add":
            try:
                new_diary = notebook.Diary(entry=command_combination[index+1])
                notebook_obj.add_diary(diary=new_diary)
                notebook_obj.save(path)
            except:
                print("Error, -add")
                return
        elif command_combination[index] == "-del":
            try:
                notebook_obj.del_diary(index=int(command_combination[index+1]))
                notebook_obj.save(path)
            except:
                print("Error, -del")
                return
           
