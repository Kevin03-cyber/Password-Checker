# Password Checker

A small Flask web app that checks how strong a password is, checks whether it has appeared in known data leaks, and suggests memorable passwords.

<img width="1882" height="977" alt="image" src="https://github.com/user-attachments/assets/a70c61f7-5898-4dc7-a22f-f1e55e8a1026" />
<img width="1887" height="977" alt="image" src="https://github.com/user-attachments/assets/8adc736e-958a-488c-88c1-fe162ba42e78" />
<img width="1875" height="975" alt="image" src="https://github.com/user-attachments/assets/137691a6-fcdb-44fe-9f41-ade4581f8bbc" />




## Features
- **Strength checker:** scores a password as Weak, Medium, or Strong using its length, character types, and a list of very common passwords. It also gives tips to improve it.
- **Breach check:** tells you how many times a password appears in known data leaks, using the Have I Been Pwned "Pwned Passwords" service.
- **Memorable suggestions:** creates three easy-to-remember passwords at a time, like `Panda-Loves-Pancake-47` (Animal-Verb-Food-Number), with a Copy button for each.
- **Dark user interface** with a show/hide button for the password box.

## How the breach check works
1. The password is hashed with SHA-1.
2. Only the **first 5 characters** of the hash are sent to the service.
3. The service returns all leaked hashes that start with those 5 characters.
4. The app compares the rest of the hash locally.

The real password and the full hash never leave the computer. This technique is called **k-anonymity**.

## Threats it addresses
- Weak and very common passwords
- Passwords already exposed in data breaches, which attackers reuse in credential-stuffing attacks

## Security notes
- The password is sent with POST, so it never appears in the URL.
- Passwords are never stored or logged.
- Suggestions are built with Python's `secrets` module, not `random`, because `secrets` uses secure randomness from the operating system.
- SHA-1 is used only because the breach service requires it for lookups. It is not used to store passwords.

## Limitations
- The strength rules only look at length and character types. They do not detect keyboard patterns, names, or dates, so a predictable password can still be rated Strong.
- The common-password list is small.
- The memorable suggestions use small word lists (50 animals, 12 verbs, 50 foods) plus a 2-digit number. That gives only about 2.7 million combinations (roughly 21 bits), which is easy to remember but weak against offline cracking. They are fine for a demo and low-importance accounts, not for email or banking.
- The breach check needs an internet connection.
- It runs on Flask's development server and is not meant for production.

## Tech stack
Python, Flask, Requests, HTML, CSS, and JavaScript.

## Project structure
```
password_checker/
    app.py
    requirements.txt
    README.md
    templates/
        index.html
```

## How to run (Windows)
```
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```
Then open http://127.0.0.1:5001 in your browser.

## Future improvements
- Score passwords by estimated entropy instead of simple rules
- Detect keyboard patterns and common substitutions like `P@ssw0rd`
- Use a much larger word list (for example, the 7,776-word Diceware list)
- Add a live strength meter that updates as you type
