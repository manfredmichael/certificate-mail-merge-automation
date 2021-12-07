import pandas as pd

from certificate_generator.generator import Generator
from certificate_generator import utils


attendance = pd.read_csv('data/Recipients.csv')
registered = pd.read_csv('data/Registered Attendees.csv')

email_attendance = attendance['Username']
email_registered = registered['Confirm you email...']

print(attendance.columns)
print(registered.columns)

print(email_attendance.iloc[:3])
print(email_registered.iloc[:3])
# for i, row in attendance.sample(5).iterrows():
#     print(row)

