import cv2
from cvzone.PoseModule import PoseDetector
import os
import requests


cap = cv2.VideoCapture(0)  # webcam
cap.set(3, 800)
cap.set(4, 600)

detector = PoseDetector()
people = False
img_count, breakcount = 0, 0

path = 'tidak_dikenal/'
url = 'https://api.telegram.org/bot'
token = "6949241978:AAFESYlq-z6P-6HUtuC91Cf3QWUwde9Oils"  # replace token bot
chat_id = "1354267423"  # replace chat ID
caption = "Ada Maling Terdeteksi !!"

while True:
    success, img = cap.read()
    img = detector.findPose(img, draw=False)
    lmList, bboxInfo = detector.findPosition(img, bboxWithHands=False)

    img_name = f'image_{img_count}.png'

    if bboxInfo:
        breakcount += 1

        if breakcount >= 30:
            if people == False:
                img_count += 1
                cv2.imwrite(os.path.join(path, img_name), img)
                files = {'photo': open(path + img_name, 'rb')}
                resp = requests.post(url + token + '/sendPhoto?chat_id=' +
                                     chat_id + '&caption=' + caption + '', files=files)
                print(resp.status_code)
                people = not people

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('n'):
        cv2.destroyAllWindows()
        cap.release()
        break
