# To run and test the code you need to update 4 places:
# 1. Change MY_EMAIL/MY_PASSWORD to your own details.
# 2. Go to your email provider and make it allow less secure apps.
# 3. Update the SMTP ADDRESS to match your email provider.
# 4. Update birthdays.csv to contain today's month and day.
# See the solution video in the 100 Days of Python Course for explainations.

import os
import pandas
import datetime as dt
import random
import smtplib
my_email = os.environ.get("MY_EMAIL")
password = os.environ.get("PASSWORD")
recipient = ""
def random_letter():
    letters = ["letter_templates/letter_1.txt", "letter_templates/letter_2.txt", "letter_templates/letter_3.txt"]
    return random.choice(letters)
def get_letter(name):
    letter = random_letter()
    with open(letter, "r") as file:
        content = file.read()
        new_content = content.replace("[NAME]", name)
        return new_content

now = dt.datetime.now()
month = now.month
day = now.day
today_date = [month,day]
df = pandas.read_csv("birthdays.csv")
birthdays = df.to_dict("records")
for birthday in birthdays:
    if birthday["month"] == month and birthday["day"] == day:
        letter = get_letter(birthday["name"])
        recipient = birthday["email"]
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
                from_addr=my_email,
                to_addrs=recipient,
                msg=f"Subject:Birthday Wish\n\n {letter}"
            )
