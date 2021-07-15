
import pickle
import time
from collections import Counter
import csv
import cv2
import face_recognition
from IPython.display import clear_output
import datetime
FONT = cv2.FONT_HERSHEY_SIMPLEX

def recognize_attendence():
    clas = input("Enter class year & division:")
    sub = input("\nEnter subject name:")
    room = input("\nEnter room number:")
    print("[INFO] loading encodings...")
    data = pickle.loads(open(r"E:\face\GUICode\model_encodings.pickle", "rb").read()) #enter path address of pickle file according to your PC libraries and folders.

    print("[INFO] recognizing faces...")

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    cv2.namedWindow("recognize faces")

    num_names = Counter(data['names'])
    present_name = list()

    while True:
        ret, image = cam.read()
        if not ret:
            break
        k = cv2.waitKey(1)

        if k % 256 == 27:
            print("\nEscape hit, closing...")
            break

        clear_output(wait=True)

        boxes = face_recognition.face_locations(image, model='hog')
        encodings = face_recognition.face_encodings(image, boxes)
        names, present_name = [], []

        # TO find faces & add names in CSV file. Enter the path for CSV file according to your PC libraries & folders. Don't use default mentioned ones.
        with open(r"E:\face\GUICode\innovators.csv", mode='w',newline='') as file:
            file_writer = csv.DictWriter(file,delimiter=',',fieldnames =["NAMES","ROLL NO.","DATE","TIME","CLASS","SUBJECT","ROOM NO."])
            file_writer.writeheader()
            for encoding in encodings:
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                num_prop = 0

                if True in matches:
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    name = max(counts, key=counts.get)
                    num_prop = counts[name] / num_names[name]

                    print("[INFO] detected %s with '%f' accuracy ..." %
                          (name, num_prop))
                
                    x = datetime.datetime.now()
                    date = x.strftime("%x")
                    kal = x.strftime("%X")
                    roll_no = name[:2]
                    naya_name = name[3:]
                
                
                    file_writer.writerow({'NAMES':naya_name,'ROLL NO.':roll_no,'DATE':date,'TIME':kal,'CLASS':clas,'SUBJECT':sub,'ROOM NO.':room})


            
                if(num_prop > 0.9):
                    t = time.strftime('%Y-%m-%d %H:%M:%S')

    #             if name not in present_name:
    #                 q = "INSERT INTO attendance(name, timestamp) values ('" + \
    #                     name + "', '" + t + "');"
    #                 mycursor.execute(q)

                    print("[INFO] Found %s (%f)." % (name, num_prop))

                    present_name.append(name)

                names.append(name if num_prop > 0.85 else "Unknown")

        # draw rectangle over found faces
            for ((top, right, bottom, left), name) in zip(boxes, names):

                left, top, right, bottom = left , top , right, bottom 

                cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)

                s = cv2.getTextSize(name, FONT, 0.5, 1)

                cv2.rectangle(image, (left, top), (left + s[0][0] + 20,  top + s[0][1] + 10), (255, 0, 0), -1)
                name = name.replace("_", " ")
                name = name.title()

                cv2.putText(image, name, (left + 20, top + 10 + s[0][1]), FONT, 0.5, (255, 255, 255), 2)


            cv2.imshow("recognize faces", image)

        
    cam.release()

    cv2.destroyAllWindows()

