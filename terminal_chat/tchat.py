""" Terimal Chat powered by Firebase """
""" Rishabh Mehta
    Last update: 5/18/2020 """
#needs auth key
#needs ansync update

from os import system, name
from datetime import datetime
from firebase import firebase
from colorama import init, Fore, Back, Style

database_loc = 'https://quick-txt.firebaseio.com/'
firebase = firebase.FirebaseApplication(database_loc, None)
init(autoreset=True) #resets console styling after each output

#returns the time when the function called
def get_time():
    stamp = datetime.now()
    return stamp.strftime("%I:%M:%S %p") #HOUR:MINUTE:SECOND:AM/PM

""" Clears the ternimal console once called.
    Only garanteed to work for Windows, macOS, and linux OS """
def clear():
    #if running on windows
    if name == "nt":
        _ = system('cls')
    else: #running on macOS or linux
        _ = system('clear')

""" displays all of the contents from the database.
    If the database is empty nothing is printed. """
def display_chat(user_data):
    clear() #clear console before outputing messages
    messages = firebase.get(user_data[0], None) #dict of table key -> message
    if messages == None:
        return
    for key in messages:
        #if the message is sent by youself, output in blue
        if user_data[1] == messages[key][:messages[key].find(':')]:
            print(Fore.BLUE + messages[key])
        else:
            print(messages[key])

""" Displays the messages from the database,
    asks for user input,
    if #q the function is exited
    if not #r, the input will be written on the database,
    the function will be recurvisely called till #q is entered """
def chat_handle(user_data):
    display_chat(user_data)
    response = input("enter a message, refresh key (#r), or quit key (#q)> ")
    if response == "#q":
        return
    if response != "#r": #if not refreshing the page
        response = user_data[1] + ': ' + response + '  --sent at ' + get_time() + '--'
        firebase.post(user_data[0], response)
    chat_handle(user_data)

""" ask user for the chat room to join and the
    chat name. If the user inputs a chat room that currently exists in the database,
    the room will be created. """
def join_room():
    room = database_loc+input('Enter chat room name> ')
    name = input('Enter chat name> ')
    firebase.post(room, name+' joined the chat at '+get_time())
    return [room, name]

if __name__ == "__main__":
    print("** Terminal Chat **")
    user_data = join_room()
    chat_handle(user_data)
