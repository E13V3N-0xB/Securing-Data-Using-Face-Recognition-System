import tkinter as tk
from tkinter import * 
from tkinter import messagebox
import cv2
import os
import sys
import numpy as np
import FaceDetection
import warnings
from os import system
import os

warnings.filterwarnings("ignore")
faces=[]
labels=[]
names={}
dirpath = os.getcwd()
training_folder = dirpath+"/Face_Recognition_Script/training-data"





def createLables():
    dirs = os.listdir(training_folder)
    for users in dirs:
        lable = int(users[users.find("@")+1:len(users)])
        names[lable] = users[0:users.find("@")]
        subfolders = training_folder + "/" + users
        imagesName = os.listdir(subfolders)
        for image in imagesName:
            imagePath = subfolders + "/" + image
            face = cv2.imread(imagePath)
            face = cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
            #cv2.imshow("Training on this image...",face)
            #cv2.waitKey(10)
            #cv2.destroyAllWindows()
            faces.append(face)
            labels.append(lable)
    #print("Labels: "+ str(labels))
    #print("Total Number of Faces: "+str(len(faces)))
    #print(names)
face_recognizer = object
def trainDataLBPH():
    # create our LBPH face recognizer
    #face_recognizer = cv2.
    global face_recognizer
    if len(labels)>0:
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(faces, np.array(labels))
    else:
        print("No train data is present. Add train data using -train flag.")
        sys.exit()
def trainDataEigen():
    # or use EigenFaceRecognizer by replacing above line with
    if len(labels)>0:
        face_recognizer = cv2.face.createEigenFaceRecognizer()
        face_recognizer.train(faces, np.array(labels))
    else:
        print("No train data is present. Add train data using -train flag.")
        sys.exit()
def trainDataFisher():
    # or use FisherFaceRecognizer by replacing above line with
    if len(labels)>0:
        face_recognizer = cv2.face.createFisherFaceRecognizer()
        face_recognizer.train(faces, np.array(labels))
    else:
        print("No train data is present. Add train data using -train flag.")
        sys.exit()


def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)


def predict(test_img):
    img = test_img
    img, face, rect = FaceDetection.detect_faces(FaceDetection.haar_face_cascade,img,1.1)
    if face=="None":
        pass
    else:
        face = cv2.cvtColor(np.array(face,dtype=np.uint16),cv2.COLOR_BGR2GRAY)
        label,conf = face_recognizer.predict(np.array(face,dtype=np.uint16))
        if label==-1:
        	label_text = "unknown"
        else:
        	label_text = names[label]
    #print(face)
        draw_rectangle(img, rect)
        draw_text(img, label_text, rect[0], rect[1] - 5)
   # print(face)
    return img

def newUserTest():
    cap = cv2.VideoCapture(0)
    os.system('cls')
    previous_label = ""
    while (True):
        ret, frame = cap.read()
        #test = frame.copy()
        frame,frame_crop,rect = FaceDetection.detect_faces(FaceDetection.haar_face_cascade,frame,1.1)
        if frame_crop == "None":
            pass
        else:
            
            frame_crop = cv2.cvtColor(np.array(frame_crop, dtype=np.uint16), cv2.COLOR_BGR2GRAY)
            label, conf = face_recognizer.predict(np.array(frame_crop, dtype=np.uint16))
            if label == -1:
            	label_text = "unknown"
            else:
            	label_text = names[label]
            #label_text = names[label]
                # print(face)
            draw_rectangle(frame, rect)
            global pass_name
            if previous_label!=label_text:
                os.system('cls')
                previous_label = label_text
                print(label_text)
                if label_text==pass_name and pass_name!='':
                    sys.exit()
            draw_text(frame, label_text, rect[0], rect[1] - 5)
        cv2.imshow('Smile :) with different moods', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #cv2.imwrite("sample.jpg",test)
            break

    cap.release()
    cv2.destroyAllWindows()





def newUser(name):
#     name = input("Enter Your Name: ")
    dirs = os.listdir(training_folder)
    os.makedirs(training_folder+'/'+name+'@'+str(len(dirs)+1))
    cap = cv2.VideoCapture(0)
    i=0
    while (True):
        ret, frame = cap.read()
        test = frame.copy()
        frame,frame_crop,rect = FaceDetection.detect_faces(FaceDetection.lbp_face_cascade,frame)
        cv2.imshow('Smile :) with different moods', frame)
        cv2.waitKey(50)
        if frame_crop!="None" and i<100:
            print(training_folder+"/" + name + '@' + str(len(dirs)+1) + '/' + str(i) + '.jpg')
            cv2.imwrite(training_folder+"/" + name + '@' + str(len(dirs)+1) + '/' + str(i) + '.jpg', frame_crop)
            #cv2.imwrite("sample.jpg",test)
            i+=1
        elif i>=100:
            break

    cap.release()
    cv2.destroyAllWindows()


def validName(e1,inn):
    global name
    
    name=e1.get()
    if(name.isalpha()==False):
        messagebox.showinfo("Error", "Enter Alphabetical Name")
    else:
        inn.destroy()
        newUser(name)
        
    

    
    
def inName():
    from functools import partial
    inn= tk.Tk(className="Add Image Data");
    
    
#     Label(inn,text="Enter Your Roll Number : ",font=16).grid(row=1,column=1,sticky=E,padx=50)
#     e1=Entry(inn,width=25,font=16)
#     e1.grid(row=1,column=2,padx=50,pady=30,sticky=W)
    
    Label(inn,text="Enter Your Name : ",font=16).grid(row=2,column=1,sticky=E,padx=50)
    e2=Entry(inn,width=25,font=16)
    e2.grid(row=2,column=2,padx=50,pady=30,sticky=W)
    
    Button(inn,text="Submit",font=16,command=partial(validName,e2,inn)).grid(row=3,column=2,pady=30)
    
    inn.mainloop()
    
def Train():
    createLables();
    trainDataLBPH();
    


def lockUnlock():
    import subprocess
    subprocess.call([r'C:\Users\Tanuj Johal\Desktop\Windows-Folder-Unlock-Using-Face-Recognition-master\locker.bat'])

def main():
    
    root = tk.Tk(className="Main Page")  
    Label(root,text="Welcome to Face Recogination Attendance System",font=26).grid(row=1,column=1,sticky=E,padx=100,pady=40)
    
    Button(root,text="Train New User",font=15,command=inName).grid(row=2,column=1,pady=20)
    Button(root,text="Run and Train",font=15,command=Train).grid(row=3,column=1,pady=20)
#     Button(root,text="Train Data",font=15,command=TrainImages).grid(row=4,column=1,pady=20)
    Button(root,text="Check New User",font=15,command=newUserTest).grid(row=5,column=1,pady=20)
    Button(root,text="Lock/Unlock",font=15,command=lockUnlock).grid(row=6,column=1,pady=20)
    
    root.mainloop()

    
    

name='';
pass_name = '';
roll='';

main()
