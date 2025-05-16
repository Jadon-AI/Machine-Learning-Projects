from cv2 import VideoCapture, imshow, imwrite, waitKey, destroyWindow
from MLtoPico_Prediction import *
import os
from time import sleep

list = []


def cheese(Photos, Wait):    
    dir = f"{os.getcwd()}"
    
    for i in range(Photos):
        cam = VideoCapture(0)
        
        sleep(Wait)
        result, image = cam.read()

        if result:
            imshow(f"test_pic{i+1}", image)
            imwrite(f"{dir}/test_pic{i+1}.png", image)

        else:
            print("NEIN")
        
        img_path = f"{dir}/test_pic{i+1}.png"
        predicted_class = predict_image(img_path)
        print(predicted_class)
        list.append(predicted_class)
        
        waitKey(Wait*1000)
        destroyWindow(f"test_pic{i+1}")

        try:
            os.remove(img_path)
        except:
            pass

    return list


cheese(Photos=5, Wait=1)
print(list)

file_path = "list.txt"

with open(file_path, "w") as file:
    for item in list:
        file.write(item + "\n")
