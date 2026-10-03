# Password Checker

A small Flask web app that checks how strong a password is, checks whether it has appeared in known data leaks, and generates strong passwords and passphrases.

## Features
- Strength checker (length, character types, common-password list)
- Breach check using the Have I Been Pwned "Pwned Passwords" service
- Random password generator using Python's `secrets` module
- Passphrase generator (easy-to-remember passwords)

## How the breach check works
The password is hashed with SHA-1. Only the first 5 characters of the hash are sent to the service. The service returns all leaked hashes that start with those 5 characters, and the app compares the rest locally. The real password and the full hash never leave the computer. This technique is called k-anonymity.

## Threats it addresses
- Weak and common passwords
- Passwords already leaked in data breaches (used in credential-stuffing attacks)

## Security notes
- The password is sent with POST, so it does not appear in the URL.
- Passwords are never stored or logged.
- `secrets` is used instead of `random` because it uses secure randomness from the operating system.
- SHA-1 is used here only because the breach service requires it, not for storing passwords.

## Limitations
- The strength rules are simple. They do not detect keyboard patterns or personal information.
- The common-password list is small.
- The passphrase word list has 100 words. Real tools use about 7,776.
- The breach check needs an internet connection.
- It runs on Flask's development server and is not meant for production.

## How to run (Windows)
```
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe app.py
```
Then open http://127.0.0.1:5001

## Future improvements
- Larger common-password list and pattern detection
- Bigger passphrase word list
- Live strength meter using JavaScript