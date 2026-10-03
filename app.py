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
WORDS = [
    "apple", "river", "tiger", "cloud", "lamp", "ocean", "pencil", "garden", "rocket", "window",
    "forest", "candle", "bridge", "orange", "planet", "guitar", "silver", "button", "castle", "dragon",
    "flower", "hammer", "island", "jungle", "kitten", "ladder", "magnet", "napkin", "pillow", "rabbit",
    "saddle", "tunnel", "violin", "wallet", "yellow", "zipper", "anchor", "basket", "coffee", "dolphin",
    "engine", "falcon", "glacier", "harbor", "iceberg", "jacket", "kernel", "lemon", "mirror", "needle",
    "office", "parrot", "quartz", "ribbon", "spider", "turtle", "umbrella", "valley", "walnut", "pepper",
    "mango", "bottle", "camera", "desert", "eagle", "fabric", "goblet", "helmet", "insect", "jigsaw",
    "kettle", "lantern", "marble", "nickel", "orchid", "pocket", "quiver", "robot", "sunset", "thunder",
    "unicorn", "velvet", "whistle", "yogurt", "zebra", "bamboo", "cactus", "diamond", "ember", "feather",
    "giraffe", "honey", "indigo", "jasmine", "koala", "lotus", "meadow", "noodle", "oyster", "puzzle",
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
def generate_password(length=16):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    while True:
        password = "".join(secrets.choice(characters) for _ in range(length))
        # Keep trying until the password has all 4 character types
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and any(c.isdigit() for c in password)
            and any(c in "!@#$%^&*" for c in password)
        ):
            return password

def generate_passphrase(word_count=5):
    words = [secrets.choice(WORDS).capitalize() for _ in range(word_count)]
    number = secrets.randbelow(100)
    return "-".join(words) + "-" + str(number)

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
    kind = request.form.get("kind", "random")
    if kind == "passphrase":
        password = generate_passphrase()
    else:
        try:
            length = int(request.form.get("length", 16))
        except ValueError:
            length = 16
        length = max(12, min(length, 64))
        password = generate_password(length)
    return render_template("index.html", generated=password)

if __name__ == "__main__":
    app.run(debug=True, port=5001)