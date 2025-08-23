import requests
import hashlib
import random
import string
import tkinter as tk
from tkinter import ttk, messagebox , PhotoImage



# Password Leak Checker Functions

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f"Error fetching: {res.status_code}, check the API and try again")
    return res


def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return int(count)
    return 0


def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)



# Password Generator Function

def generate_password(length=12):
    chars = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(chars) for _ in range(length))



# GUI Functions

def check_password():
    password = pass_input.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password to check.")
        return

    count = pwned_api_check(password)
    if count:
        messagebox.showerror("Compromised!", f"'{password}' was found {count} times.\nYou should change it!")
    else:
        messagebox.showinfo("Safe", f"'{password}' was NOT found. OK to use!")


def generate_password_gui():
    try:
        length = int(length_input.get())
    except ValueError:
        length = 12  # default

    password = generate_password(length)
    pass_generated.delete(0, tk.END)
    pass_generated.insert(0, password)

    ##Autmoatically checks if passsword was pawned 
    try:
    	count = pwned_api_check(password)
    	if count:
    		messagebox.showwarning("Alert! Compromised password",
    			f'please generate a new password . Above password was found {count} times in leaked passwords . Thanks')

    	else:
    		messagebox.showinfo(
    			'Recommended Password ',
    			f'The generated password {password} was found {count} times in leaked passwords. OK to use')
    except Exception as e:
    	messagebox.showerror("Error", f'Could not check password: {e}')		



### Tkinter App

window = tk.Tk() ### instantiate an instance of a window 
window.title(" Password Tool")
window.geometry("450x250")

icon = PhotoImage(file='icon.gif')
window.iconphoto(True, icon)


tab_nav = ttk.Notebook(window)

# Tab 1: Check Password
tab1 = ttk.Frame(tab_nav)
tab_nav.add(tab1, text="Check Password")

lbl1 = tk.Label(tab1, text="Enter Password:", font=("Arial", 12))
lbl1.pack(pady=10)

pass_input = tk.Entry(tab1, show="*", width=30, font=("Arial", 12))
pass_input.pack(pady=5)

btn_check = tk.Button(tab1, text="Check Password", command=check_password, bg="red", fg="white", font=("Arial", 12))
btn_check.pack(pady=10)

# Tab 2: Generate Password
tab2 = ttk.Frame(tab_nav)
tab_nav.add(tab2, text="Generate Password")

lbl2 = tk.Label(tab2, text="Enter Length:", font=("Arial", 12))
lbl2.pack(pady=10)

length_input = tk.Entry(tab2, width=10, font=("Arial", 12))
length_input.insert(0, "12")
length_input.pack(pady=5)

btn_generate = tk.Button(tab2, text="Generate", command=generate_password_gui, bg="green", fg="white", font=("Arial", 12))
btn_generate.pack(pady=10)

pass_generated = tk.Entry(tab2, width=30, font=("Arial", 12))
pass_generated.pack(pady=5)


tab_nav.pack(expand=1, fill="both")
footer_label = tk.Label(window, text="Made by Musa", font=("Arial", 10), fg="red")
footer_label.pack(side="bottom", pady=5)

window.mainloop()





