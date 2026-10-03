import hashlib
import secrets
import string

import requests
from flask import Flask, render_template, request

app = Flask(__name__)

COMMON_PASSWORDS = {
    "password", "password123", "123456", "12345678", "123456789",
    "qwerty", "abc123", "iloveyou", "admin", "welcome",
    "letmein", "111111", "football", "monkey", "dragon",
}

ANIMALS = [
    "Tiger", "Panda", "Rabbit", "Monkey", "Elephant", "Giraffe", "Dolphin", "Penguin", "Koala", "Parrot",
    "Turtle", "Zebra", "Lion", "Bear", "Fox", "Wolf", "Owl", "Eagle", "Falcon", "Horse",
    "Donkey", "Camel", "Kangaroo", "Squirrel", "Hamster", "Kitten", "Puppy", "Goat", "Sheep", "Cow",
    "Duck", "Chicken", "Crow", "Otter", "Seal", "Whale", "Shark", "Crab", "Frog", "Lizard",
    "Snake", "Mouse", "Hedgehog", "Raccoon", "Moose", "Bat", "Peacock", "Rhino", "Hippo", "Cheetah",
]

FOODS = [
    "Mango", "Banana", "Apple", "Cookie", "Pizza", "Noodles", "Burger", "Cheese", "Honey", "Carrot",
    "Pancake", "Popcorn", "Cake", "Bread", "Rice", "Pasta", "Grapes", "Lemon", "Orange", "Peach",
    "Cherry", "Melon", "Berries", "Coconut", "Pumpkin", "Potato", "Tomato", "Corn", "Waffle", "Donut",
    "Muffin", "Pretzel", "Sandwich", "Chocolate", "Biscuit", "Sausage", "Salad", "Soup", "Mushroom", "Peanuts",
    "Almonds", "Pineapple", "Papaya", "Kiwi", "Plum", "Pear", "Olive", "Cupcake", "Jelly", "Candy",
]

VERBS = [
    "Eats", "Loves", "Wants", "Steals", "Finds", "Shares",
    "Smells", "Tastes", "Grabs", "Craves", "Likes", "Hides",
]


def check_strength(password):
    if not password:
        return "Weak", ["Please type a password first."]

    if password.lower() in COMMON_PASSWORDS:
        return "Weak", ["This is a very common password. Attackers try these first."]

    score = 0
    tips = []

    # Length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
        tips.append("Make it 12 characters or longer.")
    else:
        tips.append("Use at least 8 characters. 12 or more is better.")

    # Character types
    if any(c.islower() for c in password):
        score += 1
    else:
        tips.append("Add lowercase letters.")

    if any(c.isupper() for c in password):
        score += 1
    else:
        tips.append("Add uppercase letters.")

    if any(c.isdigit() for c in password):
        score += 1
    else:
        tips.append("Add numbers.")

    if any(not c.isalnum() for c in password):
        score += 1
    else:
        tips.append("Add symbols like ! @ # $.")

    # Score is 0 to 6
    if score >= 6:
        level = "Strong"
    elif score >= 4:
        level = "Medium"
    else:
        level = "Weak"

    return level, tips


def check_breach(password):
    """
    Returns how many times the password appears in known data leaks.
    Returns 0 if not found, and -1 if the check could not run.
    Only the first 5 characters of the hash are sent. The password is never sent.
    """
    sha1 = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    prefix = sha1[:5]
    suffix = sha1[5:]

    try:
        response = requests.get(
            f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5
        )
        response.raise_for_status()
    except requests.RequestException:
        return -1

    # The service returns many lines like "HASH_SUFFIX:COUNT"
    for line in response.text.splitlines():
        hash_suffix, count = line.split(":")
        if hash_suffix == suffix:
            return int(count)

    return 0


def generate_passphrase():
    animal = secrets.choice(ANIMALS)
    verb = secrets.choice(VERBS)
    food = secrets.choice(FOODS)
    number = secrets.randbelow(90) + 10  # a number from 10 to 99
    return f"{animal}-{verb}-{food}-{number}"

@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    tips = []
    breach = None
    if request.method == "POST":
        password = request.form.get("password", "")
        result, tips = check_strength(password)
        if password:
            breach = check_breach(password)
    return render_template("index.html", result=result, tips=tips, breach=breach)


@app.route("/generate", methods=["POST"])
def generate():
    suggestions = [generate_passphrase() for _ in range(3)]
    return render_template("index.html", suggestions=suggestions)

if __name__ == "__main__":
    app.run(debug=True, port=5001)