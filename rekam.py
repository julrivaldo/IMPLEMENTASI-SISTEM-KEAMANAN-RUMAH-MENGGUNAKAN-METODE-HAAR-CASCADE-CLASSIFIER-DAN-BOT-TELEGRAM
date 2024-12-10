from dis import Instruction
import winsound
import cv2
import os
import numpy as np
import tkinter as tk
import tkinter.font as font
from Hasilwajah import identify
from tkinter import messagebox


def selesai1():
    messagebox.showinfo(
        "Informasi", "Rekam Data Telah Selesai! \n dan disimpan sebanyak 200 foto")


def collect_data(name, ids):
    count = 1
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')

    while True:
        _, frm = cap.read()

        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray, 1.4, 1)
        eyes = eye_cascade.detectMultiScale(gray, 1.3, 2)

        for x, y, w, h in faces:
            cv2.rectangle(frm, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frm[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey),
                              (ex+ew, ey+eh), (255, 0, 0), 2)

            cv2.imwrite(f"dataset/{name}-{count}-{ids}.jpg", roi_gray)
            count = count + 1
            cv2.putText(frm, f"{count}", (20, 20),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)
            cv2.imshow("new", roi_color)

        cv2.imshow("identify", frm)

        if cv2.waitKey(1) == 27 or count > 200:
            cv2.destroyAllWindows()
            cap.release()
            winsound.Beep(900, 1000)
            selesai1()
            break


def add_member_gui():

    def start_data_collection():
        name = entry_name.get()
        ids = entry_id.get()
        collect_data(name, ids)

    add_member_window = tk.Toplevel()
    add_member_window.title("Tambahkan orang")
    add_member_window.geometry("600x400")
    add_member_window.maxsize(600, 400)
    add_member_window.config(bg='red')

    label_name = tk.Label(add_member_window, text="nama:", bg='red')
    label_name.pack(pady=(10, 5))
    entry_name = tk.Entry(add_member_window)
    entry_name.pack(pady=(0, 5))

    label_id = tk.Label(add_member_window, text="id:", bg='red')
    label_id.pack()
    entry_id = tk.Entry(add_member_window)
    entry_id.pack(pady=(0, 10))

    button_collect = tk.Button(add_member_window, text="Collect Data",
                               command=start_data_collection)
    button_collect.pack()

    return
