from flask import Flask, render_template, request
from datetime import datetime, date
import random

app = Flask(__name__)

def get_lucky_number():
    return random.randint(1, 100)


def days_to_birthday(dob):
    today = date.today()
    dob = datetime.strptime(dob, "%Y-%m-%d").date()
    next_birthday = date(today.year, dob.month, dob.day)
    if next_birthday < today:
        next_birthday = date(today.year + 1, dob.month, dob.day)
    return (next_birthday - today).days

def calculate_age(dob):
    today = datetime.today()
    birth_date = datetime.strptime(dob, "%Y-%m-%d")
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

def is_birthday_today(dob):
    today = date.today()
    birth_date = datetime.strptime(dob, "%Y-%m-%d").date()
    return (today.month, today.day) == (birth_date.month, birth_date.day)

def get_zodiac_sign(dob):
    month, day = map(int, dob.split('-')[1:])
    zodiac_signs = [
        (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 20, "Pisces"), (4, 20, "Aries"),
        (5, 21, "Taurus"), (6, 21, "Gemini"), (7, 22, "Cancer"), (8, 23, "Leo"),
        (9, 23, "Virgo"), (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
        (12, 31, "Capricorn")
    ]
    for m, d, sign in zodiac_signs:
        if (month, day) <= (m, d):
            return sign

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        dob = request.form['dob']
        age = calculate_age(dob)
        zodiac = get_zodiac_sign(dob)
        days_to_bday = days_to_birthday(dob)
        is_birthday = is_birthday_today(dob)
        lucky_number = get_lucky_number()
        message = f"Greetings, {name}! You're {age} years old with the zodiac sign {zodiac}. Your next birthday is in {days_to_bday} days. Your lucky number is {lucky_number}!"
        if is_birthday:
            message += "Happy Birthday!"
        else:
            message += f"There are {days_to_bday} days until your next birthday."
        return render_template('result.html', message=message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

