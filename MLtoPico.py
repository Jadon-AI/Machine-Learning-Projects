from machine import Pin
from utime import sleep

file = open("list.txt")
data = file.read()
data_into_list = data.split("\n")
data_into_list_count_faces = data_into_list.count("Faces")
data_into_list_count_apples = data_into_list.count("Apples")


def Led(x):
    led = Pin(25, Pin.OUT)

    if data_into_list_count_faces > 0:
        print("LED starts flashing...")
        for i in range(x):
            led.value(1)
            sleep(0.5)
            led.value(0)
            sleep(0.5)
            
            print(i+1)

        print("LED stopped flashing")

    else:
        print("Only Apples were shown")


Led(data_into_list_count_faces)
