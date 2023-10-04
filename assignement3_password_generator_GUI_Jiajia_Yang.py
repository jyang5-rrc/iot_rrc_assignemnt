import random
from guizero import App, Text, TextBox, PushButton, info

def do_generating():
    passwords = ["Your passwords:"]
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!?.,-'
    number = int(number_of_password.value)
    length = int(password_length.value)

    for p in range(number):
        password = ''

        for c in range(length):
            password += random.choice(chars)

        passwords.append(str(password))  

    string = "\n\n".join(passwords)  

    info("Passwords", string)

#set an app
app = App(title="Password Generator", width=500, height=300, layout="auto")

#widgets
Welcome_message = Text(app, text='\nWelcome to password generator', size=20, font="Times New Roman", color="lightblue")
number_asking = Text(app, text="\nHow many passwords?")
number_of_password = TextBox(app, width=30)
length_asking = Text(app, text="\n\nHow many character of each password?")
password_length = TextBox(app, width=30)
get_button = PushButton(app, command=do_generating, text="Get Password", align="bottom")
get_button.bg = "lightblue"

#execute
app.display()