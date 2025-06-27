from flask import Flask, request, render_template, jsonify
import os
import cv2
import pickle

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
COORD_FOLDER = 'static/coordinate'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(COORD_FOLDER, exist_ok=True)

video_filename = ""

@app.route("/")
def index():
    return render_template("make_koordinat.html")

@app.route("/upload_video", methods=["POST"])
def upload_video():
    global video_filename
    file = request.files.get('video')
    if not file:
        return jsonify({"success": False, "message": "No file uploaded"})

    filename = file.filename
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(save_path)
    video_filename = os.path.splitext(filename)[0]

    # Ambil frame pertama
    cap = cv2.VideoCapture(save_path)
    success, frame = cap.read()
    cap.release()

    if not success:
        return jsonify({"success": False, "message": "Gagal ambil frame"})

    frame_image = f"{video_filename}_frame.jpg"
    frame_path = os.path.join(UPLOAD_FOLDER, frame_image)
    cv2.imwrite(frame_path, frame)

    height, width = frame.shape[:2]  # Ambil ukuran asli

    return jsonify({
        "success": True,
        "frame_image": frame_image,
        "frame_width": width,
        "frame_height": height
    })

@app.route("/save_coordinates", methods=["POST"])
def save_coordinates():
    global video_filename
    data = request.get_json()
    posList = data.get("posList", [])

    if not posList or not video_filename:
        return jsonify({"status": "error", "message": "Data tidak lengkap"})

    filename = f"{COORD_FOLDER}/CarParkPos_{video_filename}.pkl"
    with open(filename, "wb") as f:
        pickle.dump(posList, f)

    return jsonify({"status": "success", "saved_file": filename})

if __name__ == '__main__':
    app.run(port=8000, debug=True)
