# 🚗 Automatic Parking Detection with Flask, OpenCV, and CvZone ()

Welcome to the Automatic **Parking Detection project**, an intelligent web-based system that can **detect empty or occupied parking slots in real-time** using video footage of the parking area. This system is suitable for **parking monitoring in public areas, buildings, or malls** with a modern and interactive interface.

## ✨ Top Features

- ✅ Upload recorded parking lot videos directly via the web
- 🟩 Mark parking slots interactively (click 4 dots on the canvas)
- 🧠 Real-time empty/filled slot detection
- 📈 Threshold can be adjusted to set detection sensitivity
- 📦 Storage of parking lot coordinates in `.pkl` file
- 🔁 Looping video display without reloading

## 🖥️ Initial Display Interface

![image](https://github.com/user-attachments/assets/cee4fc9c-f0c9-476c-afbb-1e3690e5c8f6)

> The live video feed will display the parking area and the status of each parking slot in the form of colored boxes:
> - 🟩 Green = Empty
> - 🟥 Red = Filled

## 🚀 How to Run the App

### 1. Clone Repository
```bash
git clone https://github.com/Pitooo01/Parking-Slot-Detection.git
cd Parking-Slot-Detection
```

### 2. Install Dependencies
Make sure you are using Python 3.7+ 
```bash
pip install -r requirements.txt
```

### 3. Run the Server
```bash
python main.py
```

Open a browser and access:
📍 [http://localhost:8000](http://localhost:8000)

## 📂 Directory Structure

```
.
├── static/
│   ├── uploads/          # Where uploaded videos are stored
│   └── coordinate/       # Parking coordinates file saved (.pkl format)
├── templates/
│   └── index.html        # Main Page
├── main.py               # Flask backend main file
└── README.md             # Documentation of this project
└── requirements.txt      # Libraries that need to be installed
```

## ⚠️ Important Notes

- Make sure you already have `car.png` as a favicon in the `static/` folder
- Use a video of the parking lot that is clear enough for accurate detection
- When marking a slot, click 4 dots to form a square (order doesn't matter)

## 🧠 Technology Used

- **Flask**: Python backend web framework
- **OpenCV**: Image detection and video processing
- **CvZone**: OpenCV visualization add-on library
- **HTML/CSS + JS (Toastr + jQuery)**: Modern & responsive interface

## 📸 Sample Detection Results

![image](https://github.com/user-attachments/assets/2c85db66-ce7e-45d2-bae7-5c87927137fb)

## 🙌 Contribution

This project is open source. If you want to add new features, fix bugs, or improve the look - please fork this repo and pull request!

## 🧑‍💻 Developer

**ALFITO DWITAMA**  
📫 Email: alfito.dwitama@gmail.com
📷 Instagram: [@alfitodwitamaaa](https://www.instagram.com/alfitodwitamaaa)

---

> “Technology is not just about sophistication, but how it solves real problems.” 🚀
