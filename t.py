from argparse import FileType
from tkinter import filedialog
from tkinter import messagebox
import winsound
import cv2
import os
import time
import numpy as np
import tkinter as tk
import tkinter.font as font
import telepot
from PIL import Image, ImageTk

bot = telepot.Bot("6949241978:AAFESYlq-z6P-6HUtuC91Cf3QWUwde9Oils")

cap = None


def show_info_box():
    messagebox.showinfo("Information", "Cara Penggunaan\n\n"
                        '1). Masukkan nama dan id di dalam kolom klik ENTER\n\n'
                        '2). Setelah memasukan nama dan id akan memunculkan camera yang akan mendeteksi wajah\n\n'
                        '3). Image akan tersimpan di folder dataset sebanyak 350 image\n\n'
                        '4). Klik Latih wajah sesudah deteksi wajah\n\n'
                        '5). Klik button HASIL untuk pengenalan wajah\n\n'
                        '6). Klik button hasil akhir untuk mengetahui wajah yang terdeteksi dan tidak terdeteksi\n\n')


def collect_data(name, ids):
    global cap
    count = 1
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Create directories if they don't exist
    face_dir = f"dataset/{name}/wajah/"
    eye_dir = f"dataset/{name}/mata/"
    os.makedirs(face_dir, exist_ok=True)
    os.makedirs(eye_dir, exist_ok=True)

    def show_frame():
        global cap
        nonlocal count
        _, frm = cap.read()
        gray = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

        # Adjusting parameters for better face detection
        faces = face_cascade.detectMultiScale(
            gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

        for x, y, w, h in faces:
            cv2.rectangle(frm, (x, y), (x+w, y+h), (0, 255, 0), 2)
            roi_gray = gray[y:y+h, x:x+w]
            roi_color = frm[y:y+h, x:x+w]

            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roi_color, (ex, ey),
                              (ex+ew, ey+eh), (255, 0, 0), 2)

                # Save face with eyes detected
                # Save face with eyes detected
                face = frm[y:y+h, x:x+w]
                cv2.imwrite(
                    f"{face_dir}/{name}-face-{count}-{ids}.jpg", roi_gray)
                cv2.imwrite(
                    f"dataset/wajah/{name}-{count}-{ids}.jpg", roi_gray)

                # Save eyes detected separately
                eye = roi_gray[ey:ey+eh, ex:ex+ew]
                cv2.imwrite(
                    f"{eye_dir}/{name}-eye-{count}-{ids}.jpg", eye)
                cv2.imwrite(f"dataset/mata/{name}-{count}-{ids}.jpg", eye)

                count += 1

            cv2.putText(frm, f"{count}", (20, 20),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 3)

            # Convert frame to RGB format and PIL Image
            frm_rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
            frm_pil = Image.fromarray(frm_rgb)
            frm_photo = ImageTk.PhotoImage(frm_pil)

            # Update label with the new image
            label.config(image=frm_photo)
            label.image = frm_photo

        if cv2.waitKey(1) == 27 or count > 350:
            # Set label to white image
            gray_value = 128
            gray_image = np.ones((480, 640, 3), dtype=np.uint8) * gray_value
            gray_image_pil = Image.fromarray(gray_image)
            gray_image_tk = ImageTk.PhotoImage(gray_image_pil)
            label.config(image=gray_image_tk)
            label.image = gray_image_tk

            cv2.destroyAllWindows()  # Close OpenCV window
            cap.release()  # Release camera
            winsound.Beep(900, 1000)
            intructions.config(
                text="Rekam Data Telah Selesai!\ndisimpan sebanyak 350 foto!")
            return
        # Update frame after 10 ms
        label.after(10, show_frame)

    # Start showing frames
    show_frame()


def add_member_gui():

    def start_data_collection():
        name = entry_name.get()
        ids = entry_id.get()
        collect_data(name, ids)

    def clear_entries():
        # Menghapus teks di dalam entry_name dan id
        entry_name.delete(0, tk.END)
        entry_id.delete(0, tk.END)

    add_member_window = tk.Toplevel()
    add_member_window.title("Tambahkan Orang")
    add_member_window.config(bg='grey')

    # Menghitung posisi tengah jendela utama
    window_width = 600
    window_height = 400
    screen_width = add_member_window.winfo_screenwidth()
    screen_height = add_member_window.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (window_width / 2))
    y_coordinate = int((screen_height / 2) - (window_height / 2))

    add_member_window.geometry(
        f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
    add_member_window.maxsize(600, 400)

    label_name = tk.Label(add_member_window, text="Nama:            ",
                          bg='grey', font=('Arial', 12))
    label_name.grid(row=0, column=0, padx=(20, 10), pady=(50, 5), sticky="se")

    entry_name = tk.Entry(add_member_window, width=20)
    entry_name.grid(row=0, column=1, padx=(0, 20), pady=(50, 5), sticky="se")

    label_id = tk.Label(add_member_window, text="ID:                ",
                        bg='grey', font=('Arial', 12))
    label_id.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="se")

    entry_id = tk.Entry(add_member_window, width=20)
    entry_id.grid(row=1, column=1, padx=(0, 20), pady=(0, 20), sticky="se")

    button_collect = tk.Button(add_member_window, text="Masuk",
                               command=start_data_collection, height=2, width=15)
    button_collect.grid(row=2, column=0, columnspan=2,
                        padx=20, pady=(0, 20), sticky="ew")

    button_clear = tk.Button(
        add_member_window, text="Bersihkan", command=clear_entries, height=2, width=15)
    button_clear.grid(row=3, column=0, padx=20, pady=(0, 20), sticky="s")

    button_exit = tk.Button(add_member_window, text="Keluar",
                            command=add_member_window.destroy, height=2, width=15)
    button_exit.grid(row=3, column=1, padx=20, pady=(0, 20), sticky="se")


# Latih wajah
def select_folders():
    try:
        folder1 = filedialog.askdirectory()
        if not folder1:
            return []
        folder2 = filedialog.askdirectory()
        if not folder2:
            return []
        return [folder1, folder2]
    except:
        return []


def train():
    recog = cv2.face.LBPHFaceRecognizer_create()

    dataset_folders = select_folders()
    if not dataset_folders:
        intructions.config(
            text='Harap pilih folder yang\n akan di latih')
        return

    dataset_faces = dataset_folders[0]
    dataset_eyes = dataset_folders[1]

    # Load face images
    face_paths = [os.path.join(dataset_faces, im)
                  for im in os.listdir(dataset_faces)]
    faces = []
    ids = []
    labels = []
    for path in face_paths:
        parts = os.path.basename(path).split('-')
        if len(parts) >= 3 and parts[2].split('.')[0].isdigit():
            labels.append(parts[0])
            ids.append(int(parts[2].split('.')[0]))
            faces.append(cv2.imread(path, 0))
        else:
            print(f"Invalid file format wajah: {path}")

    # Load eye images if dataset_eyes is not empty
    if dataset_eyes:
        eye_paths = [os.path.join(dataset_eyes, im)
                     for im in os.listdir(dataset_eyes)]
        for path in eye_paths:
            parts = os.path.basename(path).split('-')
            if len(parts) >= 3 and parts[2].split('.')[0].isdigit():
                labels.append(parts[0])
                ids.append(int(parts[2].split('.')[0]))
                faces.append(cv2.imread(path, 0))
            else:
                print(f"Invalid file format mata: {path}")

    if faces:
        recog.train(faces, np.array(ids))
        recog.save('train/model.xml')
        winsound.Beep(900, 1000)
        intructions.config(text="Latih Wajah selesai!")
    else:
        intructions.config(text='Gambar train tidak ditemukan.')


# Hasil Wajah
image_sent_time = time.time()


def identify():
    global cap, label_p
    dataset_face_path = "dataset/wajah"
    dataset_eye_path = "dataset/mata"
    if not os.listdir(dataset_face_path) or not os.listdir(dataset_eye_path):
        # Tampilkan pesan jika dataset wajah atau mata kosong
        intructions.config(text='Maaf, dataset wajah atau mata kosong')
        return
    cap = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_eye.xml')

    paths_face = [os.path.join("TERDETEKSI", im)
                  for im in os.listdir(dataset_face_path)]
    paths_eye = [os.path.join("TERDETEKSI", im)
                 for im in os.listdir(dataset_eye_path)]

    labelslist = {}
    for path in paths_face:
        label = path.split('/')[-1].split('-')[0]
        image_name = path.split('/')[-1].split('-')[2].split('.')[0]
        labelslist[image_name] = label

    for path in paths_eye:
        label = path.split('/')[-1].split('-')[0]
        image_name = path.split('/')[-1].split('-')[2].split('.')[0]
        labelslist[image_name] = label

    print(labelslist)
    model_path = 'train/model.xml'
    if not os.path.exists(model_path):
        intructions.config(text="Train model belum di buat")
        return
    recog = cv2.face.LBPHFaceRecognizer_create()
    recog.read(model_path)

    image_sent = False  # Variabel untuk melacak apakah gambar sudah dikirim atau tidak

    def show_frame():
        # Menggunakan nonlocal agar bisa mengakses variabel dari luar fungsi show_frame
        nonlocal image_sent
        image_sent_time = time.time()
        global cap, label_p
        _, frm = cap.read()

        if frm is None:
            return

        gray2 = cv2.cvtColor(frm, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray2, 1.3, 2)
        if len(faces) > 0:
            image_sent = False  # Reset variabel ketika wajah terdeteksi
            for x, y, w, h in faces:
                cv2.rectangle(frm, (x, y), (x+w, y+h), (0, 255, 0), 2)
                roi_gray = gray2[y:y+h, x:x+w]
                roi_color = frm[y:y+h, x:x+w]

                eyes = eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey),
                                  (ex+ew, ey+eh), (255, 0, 0), 2)

                label = recog.predict(roi_gray)

                if label[1] < 50:
                    confidence = " {0}%".format(round(100-label[1]))
                    scale = 0.7  # Ubah nilai skala font
                    (text_width, text_height), _ = cv2.getTextSize(
                        f"{labelslist[str(label[0])]} + {confidence}", cv2.FONT_HERSHEY_SIMPLEX, scale, 2)
                    text_y = y + h + text_height + 10  # Menggeser teks ke bawah kotak deteksi wajah
                    cv2.putText(frm, f"{labelslist[str(label[0])]} + {confidence}",
                                (x + w // 2 - text_width // 2, text_y), cv2.FONT_HERSHEY_SIMPLEX, scale, (0, 0, 255), 2)

                    if label[1] > 50:
                        count_var = count_var + 1
                        print(count_var)
                        count_var = count_var % 10  # membuatnya kembali ke 0 setelah mencapai 10

                    else:
                        intructions.config(
                            text='terdeteksi')  # diatas 50%
                        cv2.imwrite("dikenal/dikenal.jpg", frm)
                else:
                    if not image_sent:
                        confidence = " {0}%".format(round(100-label[1]))
                        cv2.putText(frm, f"tidak dikenal {confidence}", (x, y),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        cv2.imwrite("tidak_dikenal/tidak_dikenal.jpg", frm)
                        bot.sendPhoto("1354267423", photo=open(
                            "tidak_dikenal/tidak_dikenal.jpg", 'rb'))

                        frame_width = 640
                        frame_height = 480
                        out = cv2.VideoWriter('tidak_dikenal/video_tidak.avi', cv2.VideoWriter_fourcc(
                            *'XVID'), 30, (frame_width, frame_height))

                        # Mendefinisikan koordinat (x, y) untuk teks
                        x = 50
                        y = 50

                        # Menghitung jumlah frame yang diperlukan untuk 10 detik
                        jumlah_frame = 30 * 5  # 30 fps * 10 detik

                        # Looping untuk membuat video
                        for i in range(jumlah_frame):
                            # Menangkap frame dari kamera
                            ret, frame = cap.read()
                            if not ret:
                                break  # Keluar dari loop jika tidak dapat menangkap frame

                            # Deteksi wajah
                            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                            faces = face_cascade.detectMultiScale(
                                gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100))

                            # Menggambar kotak wajah di sekitar wajah yang terdeteksi
                            for x, y, w, h in faces:
                                cv2.rectangle(
                                    frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

                            # Tambahkan teks "tidak dikenal" ke frame
                            cv2.putText(frame, "tidak dikenal", (x, y),
                                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

                            # Menyimpan frame ke video
                            out.write(frame)

                    bot.sendVideo("1354267423", open(
                        "tidak_dikenal/video_tidak.avi", 'rb'))

                    # Menutup VideoWriter dan jendela tampilan
                    out.release()
                    cap.release()
                    cv2.destroyAllWindows()

                    image_sent = True
                    intructions.config(
                        text='tidak dikenal')  # dikarenakan dibawah 50%
                    cap.release()
                    label_p.destroy()
                    return  # Menambahkan perintah return untuk menghentikan proses

        frm_rgb = cv2.cvtColor(frm, cv2.COLOR_BGR2RGB)
        frm_pil = Image.fromarray(frm_rgb)
        frm_photo = ImageTk.PhotoImage(frm_pil)

        if frm_photo is not None:
            label_p.config(image=frm_photo)
            label_p.image = frm_photo

        label_p.after(10, show_frame)

    label_p = tk.Label(frame1, bg='grey')
    label_p.place(relx=0.5, rely=0.47, anchor=tk.CENTER)
    label_p.config(width=800, height=400)
    show_frame()


def deteksi_akhir():
    global label_d, label_t
    img_0 = cv2.imread('dikenal\dikenal.jpg')
    img_1 = cv2.imread('tidak_dikenal/tidak_dikenal.jpg')

    def show_frame():
        nonlocal img_0, img_1
        if label_d is not None:
            # Konversi gambar OpenCV ke gambar Tkinter
            img_rgb_0 = cv2.cvtColor(img_0, cv2.COLOR_BGR2RGB)
            img_pil_0 = Image.fromarray(img_rgb_0)
            img_tk_0 = ImageTk.PhotoImage(image=img_pil_0)

            label_d.config(image=img_tk_0)
            label_d.image = img_tk_0

            if label_t is not None:
                # Konversi gambar OpenCV ke gambar Tkinter
                img_rgb_1 = cv2.cvtColor(img_1, cv2.COLOR_BGR2RGB)
                img_pil_1 = Image.fromarray(img_rgb_1)
                img_tk_1 = ImageTk.PhotoImage(image=img_pil_1)

                # Tampilkan gambar di dalam frame
                label_t.config(image=img_tk_1)
                label_t.image = img_tk_1
                intructions.config(text="Gambar Akhir")

    label_d = tk.Label(frame1, bg='grey')
    label_d.place(relx=0.25, rely=0.46, anchor='center')
    label_d.config(width=480, height=430)

    # Label to display the video feed
    label_t = tk.Label(frame1, bg='grey')
    label_t.place(relx=0.75, rely=0.46, anchor='center')
    label_t.config(width=480, height=430)

    show_frame()

# Fungsi untuk mematikan kamera


def stop_camera():
    # Pastikan menggunakan variabel cap yang sama dengan yang digunakan untuk capture video
    global cap, label_p, label_d, label_t
    if cap is not None:
        cap.release()  # Membebaskan kamera
        intructions.config(text="Kamera dimatikan")

        if label_p is not None:
            # Set label_p to gray image
            gray_value = 128
            gray_image = np.ones((480, 640, 3), dtype=np.uint8) * gray_value
            gray_image_pil = Image.fromarray(gray_image)
            gray_image_tk = ImageTk.PhotoImage(gray_image_pil)
            if label_p.winfo_exists():  # Periksa apakah label_p masih ada sebelum mengkonfigurasinya
                label_p.config(image=gray_image_tk)
                label_p.image = gray_image_tk
                label_p.destroy()
                label_p = None  # Atur label_p menjadi None setelah dihancurkan

    if label_t is not None:
        # Set label_t to gray image
        gray_value = 128
        gray_image = np.ones((480, 640, 3), dtype=np.uint8) * gray_value
        gray_image_pil = Image.fromarray(gray_image)
        gray_image_tk = ImageTk.PhotoImage(gray_image_pil)
        if label_t.winfo_exists():  # Periksa apakah label_t masih ada sebelum mengkonfigurasinya
            label_t.config(image=gray_image_tk)
            label_t.image = gray_image_tk
            label_t.destroy()
            label_d.destroy()
            intructions.config(text="Gambar di Hapus")


# GUI
root = tk.Tk()
root.geometry('1080x700')
root.title("-copyrigt by julius caesar_2011500721-")
root.iconphoto(False, tk.PhotoImage(file='gambar/ubl.png'))
root.maxsize(1080, 700)

frame1 = tk.Frame(root, bg='grey')
frame1.pack(fill=tk.BOTH, expand=True)


# Label to display the video feed
label = tk.Label(frame1, bg='grey')
label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
label.config(width=640, height=480)

# Judul
canvas = tk.Canvas(frame1, bg='#BBBC7C', height=100, width=1080)
canvas.grid(row=0, column=0, columnspan=5, pady=(0, 10))
canvas.place(relx=0.5, rely=0, anchor='n')

judul = tk.Label(
    frame1, text="IMPLEMENTASI PENGENALAN WAJAH DAN MATA \nPADA SISTEM KEAMANAN RUMAH DENGAN METODE\n HAAR CASCADE CLASIFIER DAN BOT TELEGRAM SEBAGAI INFORMASI", bg='#BBBC7C')
judul_font = font.Font(size=15, weight='bold')
judul['font'] = judul_font
judul.grid(row=2, column=0, pady=(10, 10), columnspan=5)
judul.place(relx=0.5, rely=0.03, anchor='n')


# Icon
icon = Image.open('gambar/ubl.png')
icon = icon.resize((80, 80), Image.LANCZOS)
icon = ImageTk.PhotoImage(icon)
label_icon = tk.Label(frame1, image=icon, bg='#BBBC7C')
label_icon.grid(row=0, column=3, pady=(0, 0), columnspan=5)

btn1_image = Image.open('gambar/fce.png')
btn1_image = btn1_image.resize((50, 50), Image.LANCZOS)
btn1_image = ImageTk.PhotoImage(btn1_image)

btn2_image = Image.open('gambar/trn.png')
btn2_image = btn2_image.resize((50, 50), Image.LANCZOS)
btn2_image = ImageTk.PhotoImage(btn2_image)

btn3_image = Image.open('gambar/hsl.png')
btn3_image = btn3_image.resize((50, 50), Image.LANCZOS)
btn3_image = ImageTk.PhotoImage(btn3_image)

btn4_image = Image.open('gambar/cmr.png')
btn4_image = btn4_image.resize((50, 50), Image.LANCZOS)
btn4_image = ImageTk.PhotoImage(btn4_image)

btn5_image = Image.open('gambar/exit.png')
btn5_image = btn5_image.resize((50, 50), Image.LANCZOS)
btn5_image = ImageTk.PhotoImage(btn5_image)

btn6_image = Image.open('gambar/lr.png')
btn6_image = btn6_image.resize((50, 50), Image.LANCZOS)
btn6_image = ImageTk.PhotoImage(btn6_image)

btn7_image = Image.open('gambar/info.png')
btn7_image = btn7_image.resize((50, 50), Image.LANCZOS)
btn7_image = ImageTk.PhotoImage(btn7_image)


# Button Fonts
btn_font = font.Font(weight="bold", size=12)
# canvas
canvas = tk.Canvas(frame1, bg='#BBBC7C', height=150, width=1080)
canvas.grid(row=2, column=0, columnspan=5, pady=(440, 10))
canvas.place(relx=0.5, rely=1, anchor='s')
# copyright
cpy = tk.Label(
    frame1, text='copyright by julius Caesar Rivaldo - 2011500721', bg='#BBBC7C')
cpy_font = font.Font(size=10, weight='bold')
cpy['font'] = cpy_font
cpy.grid(row=2, column=4, pady=(10, 10), columnspan=5)
cpy.place(relx=0.70, rely=0.80, anchor='w')

canvas = tk.Canvas(frame1, bg='white', height=100, width=300)
canvas.grid(row=2, column=0, columnspan=1, pady=(440, 20))
# intruksi
intructions = tk.Label(frame1, text="Selamat datang", fg='black', bg='white')
intructions.grid(row=2, column=0, columnspan=1, pady=(440, 10))
intructions_font = font.Font(size=15, weight='bold')
intructions['font'] = intructions_font

# Buttons
btn1 = tk.Button(frame1, text='Pengambilan \nData', fg="black", bg='grey', command=add_member_gui, image=btn1_image, compound='left',
                 width=170, height=40, font=(btn_font))
btn1.grid(row=2, column=1, padx=(10, 10), pady=(440, 5), sticky='we')


btn2 = tk.Button(frame1, text=' Latih\n wajah', fg='black', bg='grey', command=train, image=btn2_image, compound='left',
                 width=150, height=40, font=btn_font)
btn2.grid(row=2, column=2, padx=(10, 10), pady=(440, 5), sticky='ew')

btn3 = tk.Button(frame1, text='Pengenalan\nWajah', fg='black', bg='grey', command=identify, image=btn3_image, compound='left',
                 width=150, height=40, font=btn_font)
btn3.grid(row=2, column=3, padx=(10, 10), pady=(440, 5), sticky='we')

btn4 = tk.Button(frame1, text='Matikan \n camera', fg='black', bg='grey', command=stop_camera, image=btn4_image, compound='left',
                 width=150, height=40, font=btn_font)
btn4.grid(row=2, column=4, padx=(10, 250), pady=(440, 5), sticky='ew')

btn5 = tk.Button(frame1, height=50, width=50,
                 command=root.quit, image=btn5_image, bg='#BBBC7C')
btn5['font'] = btn_font
btn5.grid(row=0, column=0, padx=(20, 200), pady=(20, 30))

btn6 = tk.Button(frame1, text=' Hasil\nAkhir', fg='black', bg='grey', command=deteksi_akhir, image=btn6_image, compound='left',
                 width=150, height=40, font=btn_font)
btn6.grid(row=2, column=1, padx=(10, 10), pady=(540, 5), sticky='we')

btn7 = tk.Button(frame1, text='Informasi', fg='black', bg='grey', command=show_info_box, image=btn7_image, compound='left',
                 width=150, height=40, font=btn_font)
btn7['font'] = btn_font
btn7.grid(row=2, column=2, padx=(10, 10), pady=(540, 5), sticky='we')


frame1.pack()
root.mainloop()
