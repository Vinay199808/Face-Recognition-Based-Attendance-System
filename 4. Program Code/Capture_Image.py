
import cv2

# counting the numbers


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

#capturing images for dataset
    
def takeImages():
    
    cascade = cv2.CascadeClassifier(r"E:\face\GUICode\haarcascade_frontalface_default.xml") #enter the address of HAAR CASCADE file according to your PC folder names & directories.
    name = input("Enter Your rollNO_Name: ")

    cam = cv2.VideoCapture(0)

    cv2.namedWindow("capture faces")

    for i in range(1, 50):
        ret, frame = cam.read()
        if not ret:
            break

        cv2.imshow("capture faces", frame)
        k = cv2.waitKey(1)

        if k % 256 == 27 :
                break
        #print("\nEscape hit, closing...")

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cascade.detectMultiScale(frame)

        for f in faces:
            x, y, w, h = [ v for v in f ]

            sub_face = frame[y:y+h + 50, x:x+w + 50]

            img_name = "data/%s.%s.jpg" % (i, name)

            cv2.imwrite(img_name, sub_face)

    cam.release()

    cv2.destroyAllWindows()
    

