from tkinter import *
from ttkbootstrap import *
import ttkbootstrap as tb
import pandas as pd
import numpy
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
import joblib

model = joblib.load("CTFv7.joblib")

root = tb.Window(themename="superhero")
root.title("CTF")
root.geometry("750x750")


continent_dropdown = ["North America", "South America", "Europe", "Africa",
    "Asia", "Oceania"]
my_combo_continent = tb.Combobox(root, bootstyle="light", 
                                 values = continent_dropdown)
my_combo_continent.current()

gender_dropdown = ["Male", "Female"]
my_combo_gender = tb.Combobox(root, bootstyle="light", 
                                 values = gender_dropdown)
my_combo_gender.current()

race_dropdown = ["White", "Black", "Asian", "Hispanic", "Native"]
my_combo_race = tb.Combobox(root, bootstyle="light", 
                                 values = race_dropdown)
my_combo_race.current()


def changer():
    if my_combo_continent.get() == "North America":
        continent = 0
    elif my_combo_continent.get() == "South America":
        continent = 1
    elif my_combo_continent.get() == "Europe":
        continent = 2
    elif my_combo_continent.get() == "Africa":
        continent = 3
    elif my_combo_continent.get() == "Asia":
        continent = 4
    else:
        continent = 5
    
    age = float(my_entry_age.get())
    
    year = float(my_entry_year.get())
    
    if my_combo_gender.get() == "Male":
        gender = 0
    else:
        gender = 1
    
    if my_combo_race.get() == "White":
        race = 0
    elif my_combo_race.get() == "Black":
        race = 1
    elif my_combo_race.get() == "Asian":
        race = 2
    elif my_combo_race.get() == "Hispanic":
        race = 3
    else:
        race = 4

    
    findability = model.predict([[continent, age, year, gender, race]])
    
    if findability == "Easy":
        my_label_find.config(text="Easy")
    else:
        my_label_find.config(text="Hard")


my_label_title = tb.Label(text="Capture the Flag", font=("Helvetica", 28), 
                    bootstyle="light")
my_label_continent = tb.Label(text="Continent:", font=("Helvetica", 28), 
                    bootstyle="light")
my_entry_age=tb.Entry(root)
my_label_age = tb.Label(text="Age:", font=("Helvetica", 28), 
                    bootstyle="light")
my_entry_year=tb.Entry(root)
my_label_year = tb.Label(text="Year:", font=("Helvetica", 28), 
                    bootstyle="light")
my_label_gender = tb.Label(text="Gender:", font=("Helvetica", 28), 
                    bootstyle="light")
my_label_race = tb.Label(text="Race:", font=("Helvetica", 28), 
                    bootstyle="light")
my_label_find = tb.Label(text="Findability", font=("Helvetica", 28), 
                    bootstyle="light")
my_button = tb.Button(text="Submit",
                      bootstyle="success, outline", command=changer)


my_label_title.pack(pady=30)
my_label_continent.pack(pady=10)
my_combo_continent.pack(pady=10)
my_label_age.pack(pady=10)
my_entry_age.pack(pady=10)
my_label_year.pack(pady=10)
my_entry_year.pack(pady=10)
my_label_gender.pack(pady=10)
my_combo_gender.pack(pady=10)
my_label_race.pack(pady=10)
my_combo_race.pack(pady=10)
my_label_find.pack(pady=10)
my_button.pack(pady=10)

root.mainloop()
