from logging import root
import tkinter as tk
import tkinter.font as font
from turtle import color
from PIL import Image, ImageTk
from rekam import add_member_gui, identify
from train import train
import cv2

root = tk.Tk()
root.geometry('1080x700')
root.title("-copyrigt by julius caesar_2011500721-")
root.iconphoto(False, tk.PhotoImage(file='gambar/ubl.png'))
root.maxsize(1080, 700)

frame1 = tk.Frame(root, bg='red')
frame1.pack(fill=tk.BOTH, expand=True)

# Judul
canvas = tk.Canvas(frame1, bg='#BBBC7C', height=100, width=1300)
canvas.grid(row=0, column=0, columnspan=5, pady=(0, 10))
judul = tk.Label(
    frame1, text="IMPLEMENTASI FACE RECOGNITION DENGAN METODE \nHAAR-CASCADE CLASSIFIER PADA SYSTEM KEAMANAN RUMAH", bg='#BBBC7C')
judul_font = font.Font(size=15, weight='bold')
judul['font'] = judul_font
judul.grid(row=0, column=0, pady=(10, 10), columnspan=5)

# Icon
icon = Image.open('gambar/ubl.png')
icon = icon.resize((80, 80), Image.LANCZOS)
icon = ImageTk.PhotoImage(icon)
label_icon = tk.Label(frame1, image=icon, bg='#BBBC7C')
label_icon.grid(row=0, column=3, pady=(0, 0), columnspan=5)

btn1_image = Image.open('gambar/org.png')
btn1_image = btn1_image.resize((50, 50), Image.LANCZOS)
btn1_image = ImageTk.PhotoImage(btn1_image)

btn2_image = Image.open('gambar/record.png')
btn2_image = btn2_image.resize((50, 50), Image.LANCZOS)
btn2_image = ImageTk.PhotoImage(btn2_image)

btn3_image = Image.open('gambar/lr.png')
btn3_image = btn3_image.resize((50, 50), Image.LANCZOS)
btn3_image = ImageTk.PhotoImage(btn3_image)

btn4_image = Image.open('gambar/mon.png')
btn4_image = btn4_image.resize((50, 50), Image.LANCZOS)
btn4_image = ImageTk.PhotoImage(btn4_image)

btn5_image = Image.open('gambar/exit.png')
btn5_image = btn5_image.resize((50, 50), Image.LANCZOS)
btn5_image = ImageTk.PhotoImage(btn5_image)

# Button Fonts
btn_font = font.Font(size=12)

# Buttons
canvas = tk.Canvas(frame1, bg='#BBBC7C', height=150, width=1300)
canvas.grid(row=2, column=0, columnspan=5, pady=(440, 10))

canvas = tk.Canvas(frame1, bg='white', height=100, width=300)
canvas.grid(row=2, column=0, columnspan=1, pady=(440, 20))

intructions = tk.Label(frame1, text="Welcome", fg='black', bg='#BBBC7C')
intructions.grid(row=2, column=0, columnspan=1, pady=(440, 10))
intructions_font = font.Font(size=15, weight='bold')
intructions['font'] = intructions_font

btn1 = tk.Button(frame1, text="deteksi & \n simpan gambar", fg="orange", bg='grey', command=add_member_gui, image=btn1_image, compound='left',
                 width=70, height=50, font=btn_font)
btn1.grid(row=2, column=1, padx=(10, 10), pady=(440, 5), sticky='we')

btn2 = tk.Button(frame1, text='train', fg='orange', bg='grey', command=train, image=btn2_image, compound='left',
                 width=70, height=50, font=btn_font)
btn2.grid(row=2, column=2, padx=(10, 10), pady=(440, 5), sticky='ew')

btn3 = tk.Button(frame1, text='Hasil', fg='orange', bg='grey', command=identify, image=btn3_image, compound='left',
                 width=70, height=50, font=btn_font)
btn3.grid(row=2, column=3, padx=(10, 10), pady=(440, 5), sticky='we')

btn4 = tk.Button(frame1, text='Fitur 4', fg='orange', bg='grey', command=train, image=btn4_image, compound='left',
                 width=70, height=50, font=btn_font)
btn4.grid(row=2, column=4, padx=(10, 250), pady=(440, 5), sticky='ew')

btn5 = tk.Button(frame1, height=50, width=50,
                 command=root.quit, image=btn5_image, bg='#BBBC7C')
btn5['font'] = btn_font
btn5.grid(row=0, column=0, padx=(20, 200), pady=(20, 30))

frame1.pack()
root.mainloop()
