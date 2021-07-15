import os
import pickle
import cv2
import face_recognition
from imutils import paths



def TrainImages():
    

    image_paths = list(paths.list_images(r"E:\face\GUICode\dataset_training")) #enter path address of folder containing all dataset images according to your PC directories.

    knownEncodings = []
    knownNames = []

    num_images = len(image_paths)

    for (i, image_path) in enumerate(image_paths):
        name = image_path.split(os.path.sep)[-2]
        print("[INFO] processing image (%s) %d/%d..." % (name, i + 1, num_images), end="\r")

        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        boxes = face_recognition.face_locations(image, model='cnn')

        encodings = face_recognition.face_encodings(image, boxes)

        for encoding in encodings:
            knownEncodings.append(encoding)
            knownNames.append(name)
 
    print("\n[INFO] serializing encodings...")
    data = {"encodings": knownEncodings, "names": knownNames}

    f = open(r"E:\face\GUICode\model_encodings.pickle", "wb") #enter path address of pickle file accodring your PC directories & folders.
    f.write(pickle.dumps(data))
    f.close()

    print("[INFO] DONE.")