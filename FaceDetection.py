import cv2

haar_face_cascade = cv2.CascadeClassifier('C:\\Users\\Tanuj Johal\Desktop\\Windows-Folder-Unlock-Using-Face-Recognition-master\\Face_Recognition_Script\\haarcascade_frontalface_alt.xml')
lbp_face_cascade = cv2.CascadeClassifier('C:\\Users\\Tanuj Johal\\Desktop\\Windows-Folder-Unlock-Using-Face-Recognition-master\\Face_Recognition_Script\\lbpcascade_frontalface.xml')


def detect_faces(f_cascade, colored_img, scaleFactor=1.1):
    img_copy = colored_img
    # convert the test image to gray image as opencv face detector expects gray images
    gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
    # let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(gray, scaleFactor=scaleFactor, minNeighbors=5);
    # go over list of faces and draw them as rectangles on original colored img
    x=0
    y=0
    z=0
    w = 0
    if len(faces)==0:
        return img_copy,"None","None"
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
    return img_copy,img_copy[y:y+w, x:x+h], faces[0]

def staticFaceDetectHaar(img):
    test1 = cv2.imread(img)
    test1 = detect_faces(haar_face_cascade,test1)
    cv2.imshow('finanl',test1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def staticFaceDetectLbp(img):
    test1 = cv2.imread(img)
    test1 = detect_faces(lbp_face_cascade,test1)
    cv2.imshow('finanl',test1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def liveFaceDetectLbp():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        frame = detect_faces(lbp_face_cascade,frame,1.1)
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

def liveFaceDetectHaar():
    cap = cv2.VideoCapture(0)
    while(True):
        ret, frame = cap.read()
        frame = detect_faces(haar_face_cascade,frame,1.1)
        cv2.imshow("frame",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            #cv2.imwrite("sample.jpg",frame)
            break
    cap.release()
    cv2.destroyAllWindows()


#liveFaceDetectHaar()
#liveFaceDetectLbp()
