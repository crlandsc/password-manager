from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():

    #Password Generator Project
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]  # Random letters
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]  # Random symbols
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]  # Random numbers

    password_list = password_letters + password_symbols + password_numbers  # add the letters, symbols, & numbers into a single list
    shuffle(password_list)  # shuffle the list to create a random password

    password = "".join(password_list)  # turn into a string

    pyperclip.copy(password)
    password_input.delete(0, END)
    password_input.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    # Save each entry to a variable
    new_website = website_input.get()
    new_email = email_username_input.get()
    new_password = password_input.get()
    #create dictionary for json
    new_data = {
        new_website: {
            "email": new_email,
            "password": new_password,
        }}

    if len(new_website) == 0 or len(new_email) == 0 or len(new_password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            # Write entry to file
            with open("Passwords.json", "r") as data_file:
                # Read old data
                data = json.load(data_file)
                # Update old data with new data
                data.update(new_data)
        except FileNotFoundError:
            with open("Passwords.json", "w"):
                data = new_data
        finally:
            with open("Passwords.json", "w") as data_file:
                # Save updated data
                json.dump(data, data_file, indent=4)

        # Erase entries
        website_input.delete(0, END)
        password_input.delete(0, END)


# ---------------------------- FIND PASSWORD ------------------------------- #


def find_password():
    search_website = website_input.get()
    try:
        with open("Passwords.json", "r") as data_file:
            # Read old data
            data = json.load(data_file)
            email_details = data[search_website]["email"]
            password_details = data[search_website]["password"]
            website_details = f"Email:  {email_details} \nPassword:  {password_details}"
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found.")
    except KeyError:
        messagebox.showerror(title="Error", message="No details for the website exists.")
    else:
        messagebox.showinfo(title=search_website, message=website_details)


# ---------------------------- UI SETUP ------------------------------- #


FONT_NAME = "Arial"
FONT_SIZE = 10

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
window.minsize(width=520, height=400)  # minimum size the window can shrink to

# MyPass Canvas
canvas = Canvas(width=200, height=200)  # create canvas
logo_img = PhotoImage(file="logo.png")  # import photo image
canvas.create_image(100, 100, image=logo_img)  # place image
canvas.grid(column=1, row=0)


# --- Labels ---
# Website Label
website_label = Label(text="Website:", font=(FONT_NAME, FONT_SIZE))
website_label.grid(column=0, row=1)

# Email/Username Label
email_username_label = Label(text="Email/Username:", font=(FONT_NAME, FONT_SIZE))
email_username_label.grid(column=0, row=2)

# Password Label
password_label = Label(text="Password:", font=(FONT_NAME, FONT_SIZE))
password_label.grid(column=0, row=3)


# --- Entries ---
# Website Entry
website_input = Entry(width=34)
website_input.focus()
website_input.grid(column=1, row=1) #, columnspan=2)

# Email/Username Entry
email_username_input = Entry(width=53, justify="left")
email_username_input.insert(0, "crlandschoot@gmail.com")
email_username_input.grid(column=1, row=2, columnspan=2)

# Password Entry
password_input = Entry(width=34, justify="left")
password_input.grid(column=1, row=3)


# --- Buttons ---
# Search Button
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

# Generate Password Button
generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3)

# Add Password Button
add_password_button = Button(text="Add", width=45, command=save)
add_password_button.grid(column=1, row=4, columnspan=2)


window.mainloop()
