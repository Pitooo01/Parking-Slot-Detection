# marker.py

import cv2
import pickle
import numpy as np
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
import os

Tk().withdraw()

video_path = askopenfilename(
    title="Pilih video parkiran",
    filetypes=[("Video Files", "*.mp4 *.avi *.mov *.mkv")]
)

if not video_path:
    print("Tidak ada video yang dipilih.")
    exit()

with open("selected_video.txt", "w") as f:
    f.write(video_path)

def get_pos_filename(video_path):
    base_name = os.path.basename(video_path)
    name, _ = os.path.splitext(base_name)
    return f"static/coordinate/CarParkPos_{name}.pkl"

pos_file = get_pos_filename(video_path)
posList = []
currentBox = []

def mouseClick(event, x, y, flags, param):
    global currentBox
    if event == cv2.EVENT_LBUTTONDOWN:
        currentBox.append((x, y))
        print(f"Titik {len(currentBox)}: {x}, {y}")

        if len(currentBox) == 4:
            posList.append(currentBox.copy())
            print(f"Tambah kotak: {currentBox}")
            currentBox = []

def tandai_koordinat(img):
    cv2.namedWindow("Tandai Kotak")
    cv2.setMouseCallback("Tandai Kotak", mouseClick)

    while True:
        img_copy = img.copy()

        for box in posList:
            pts = cv2.convexHull(np.array(box, dtype=np.int32))
            cv2.polylines(img_copy, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

        for pt in currentBox:
            cv2.circle(img_copy, pt, 5, (255, 0, 0), cv2.FILLED)

        cv2.imshow("Tandai Kotak", img_copy)
        key = cv2.waitKey(1)

        if key == ord('s'):
            with open(pos_file, 'wb') as f:
                pickle.dump(posList, f)
            print(f"✅ Semua kotak disimpan ke '{pos_file}'")

        elif key == ord('q'):
            print("🔄 Selesai menandai. Tutup jendela.")
            break

    cv2.destroyAllWindows()

if os.path.exists(pos_file):
    response = messagebox.askyesno(
        "Koordinat Ditemukan",
        "Koordinat sudah tersedia untuk video ini.\nApakah Anda ingin menandai ulang?"
    )
    if not response:
        print(f"[INFO] Menggunakan koordinat dari file {pos_file}")
        exit()

cap = cv2.VideoCapture(video_path)
success, img = cap.read()
cap.release()

if not success:
    print("Gagal membaca video.")
    exit()

print("[INFO] Tandai ulang koordinat parkir.")
tandai_koordinat(img)
