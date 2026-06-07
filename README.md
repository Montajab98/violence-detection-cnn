# 🛡️ Violent Content Detection System

> A real-time screen monitoring application that detects violent content using Deep Learning (CNN + ResNet-50) and protects users — especially children — from being exposed to gory scenes.

![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=flat&logo=python&logoColor=white)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.10-FF6F00?style=flat&logo=tensorflow&logoColor=white)
![Keras](https://img.shields.io/badge/Keras-2.10-D00000?style=flat&logo=keras&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-5C3EE8?style=flat&logo=opencv&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

---

## 📌 Overview

This project was developed as a **Bachelor's graduation project** at Tishreen University (2022). It addresses the growing problem of children and users being exposed to violent content online by building an **AI-powered real-time screen monitor** that:

- Captures periodic screenshots of the user's screen
- Classifies each screenshot as **violent (gory)** or **non-violent** using a trained CNN
- Takes automatic protective action based on the **user's age group**

**Test Accuracy: 98%** on held-out validation set.

---

## 🧠 Model Architecture

The system uses **Transfer Learning** with **ResNet-50 v1.5** as the backbone, fine-tuned for binary classification:

```
ResNet-50 (pretrained, frozen)     → Feature extraction (2048-dim)
Conv2D (32 filters, 3×3) + ReLU   → Spatial feature learning
Conv2D (64 filters, 5×5) + ReLU   → Deep feature learning
MaxPooling2D + Dropout(0.2)        → Dimensionality reduction
Flatten                            → Vector representation
Dense(128) + Dropout(0.5)          → Classification head
Dense(2) + Softmax                 → Binary output: gory / not_gory
```

**Total Parameters:** 24,302,946  
**Trainable Parameters:** 715,234

---

## 📊 Dataset

| Property | Value |
|---|---|
| Total images (original) | 2,200 |
| After augmentation | 4,400 |
| Train split | 80% (3,520 images) |
| Test split | 20% (880 images) |
| Image size | 200 × 200 px |
| Classes | `gory` / `not_gory` |

**Data collection:** Screenshots were captured from video content and manually labeled into two categories — violent (blood/injury scenes) and non-violent (people, nature, neutral scenes).

**Augmentation:** Image rotation applied to double the dataset size.

---

## 🔬 Experiments & Results

| Scenario | Model | Epochs | Augmentation | Notes |
|---|---|---|---|---|
| 1 | MLP baseline | 4 | No | Baseline |
| 2 | MLP | 4 | Yes | Improved |
| 3 | Xception | 4 | Yes | Better features |
| 4 | Xception | 10 | Yes | Higher accuracy |
| 5 | Xception | 20 | Yes | Best Xception |
| 6 | **ResNet-50** | **4** | **Yes** | **Selected ✓** |
| 7 | ResNet-50 | 10 | Yes | Diminishing returns |

**ResNet-50** was selected for its superior performance on our dataset with optimal training time.

---

## 🖥️ Application Screens

### Screen 1 — Age Verification
User identifies their age group. Routes to either **Adult Mode** or **Child Protection Mode**.

### Screen 2 — Monitoring Dashboard
Real-time monitoring control with START / STOP / BACK buttons and live status indicator.

### Screen 3 — Alert Screen
Full-screen warning overlay when violent content is detected:
- **Adult Mode:** Screen covered + 40-second cooldown before resuming
- **Child Mode:** Screen covered + audible alert after 3 violations

---

## 🛠️ Tech Stack

| Category | Tools |
|---|---|
| Deep Learning | TensorFlow, Keras |
| Pretrained Model | ResNet-50 v1.5 |
| Image Processing | OpenCV, Pillow, NumPy |
| Screen Capture | PyAutoGUI |
| GUI | Tkinter |
| Platform | Windows (Python 3.10) |

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10
- Windows OS (for screen capture and Tkinter)
- NVIDIA GPU recommended for training

### Installation

```bash
# Clone the repository
git clone https://github.com/Montajab98/violence-detection.git
cd violence-detection

# Install dependencies
pip install -r requirements.txt
```

### Run the Application

```bash
# Place your trained model in the models/ folder
# then run:
python src/app.py
```

---

## 📁 Project Structure

```
violence-detection/
├── src/
│   └── app.py              # Main application
├── models/
│   └── models_9.h5         # Trained ResNet-50 model (not included — see note)
├── docs/
│   └── images/             # Screenshots and diagrams
├── requirements.txt
└── README.md
```

> **Note:** The trained model file (`.h5`) is not included due to file size. The model was trained using Google Colaboratory with ResNet-50 pretrained weights from ImageNet.

---

## 🎯 Key Challenges

- **Data scarcity:** Violent image datasets are restricted/censored — data was collected manually
- **Compute limitations:** No local GPU available; Google Colab was used for training
- **Real-time performance:** Balancing detection speed with system resource consumption

---

## 🔮 Future Work

- Expand dataset (10,000+ images) for higher accuracy
- Add video stream support (not just screenshots)
- Implement 3-level severity classification: mild / moderate / severe
- Deploy as a browser extension or OS-level service
- Reduce model size for edge deployment

---

## 👨‍💻 Author

**Montajab Al-Hussein**  
AI Engineer | Head of AI & Robotics Department  
📍 Sharjah, UAE 🇦🇪

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://www.linkedin.com/in/montajab-al-hussein)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-181717?style=flat&logo=github)](https://github.com/Montajab98)

---

## 📄 License

This project is licensed under the MIT License.

---

*Graduation Project — Tishreen University, Applied Faculty, Department of Computer Technology, 2022*
