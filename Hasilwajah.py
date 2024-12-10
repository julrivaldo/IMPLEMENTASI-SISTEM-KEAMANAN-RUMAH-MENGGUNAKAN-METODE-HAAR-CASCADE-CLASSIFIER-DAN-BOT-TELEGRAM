from itertools import count
from operator import mod
import cv2
import os


def identify():
    cap = cv2.VideoCapture(0)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')

    paths = [os.path.join("terdeteksi", im) for im in os.listdir("dataset")]
    labelslist = {}
    for path in paths:
        label = path.split('/')[-1].split('-')[0]
        image_name = path.split('/')[-1].split('-')[2].split('.')[0]
        labelslist[image_name] = label

    print(labelslist)
    recog = cv2.face.LBPHFaceRecognizer_create()

    recog.read('train/model.xml')

    count_var = 0

    while True:
        _, frm = cap.read()

        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.3, 2)

        for x, y, w, h in faces:
            cv2.rectangle(frm, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frm[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey),
                              (ex+ew, ey+eh), (255, 0, 0), 2)

            label = recog.predict(roi_gray)

            if label[1] < 50:
                confidence = " {0}%".format(round(100-label[1]))
                (text_width, text_height), _ = cv2.getTextSize(
                    f"{labelslist[str(label[0])]} + {confidence}", cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
                cv2.putText(frm, f"{labelslist[str(label[0])]} + {confidence}",
                            (x + w // 2 - text_width // 2, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if label[1] >= 65:
                    count_var = count_var + 1
                    print(count_var)
                    count_var = mod(count_var)

            else:
                cv2.putText(frm, "tidak diketehui", (x, y),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

        cv2.imshow("identify", frm)

        if cv2.waitKey(1) & 0xFF == ord('n'):
            cv2.destroyAllWindows()
            cap.release()
            break
