"""
Violence Detection System
=========================
A real-time screen monitoring application that detects violent content
using a CNN model (ResNet-50) and takes action based on user age.

Author: Montajab Al-Hussein
Institution: Tishreen University - Applied Faculty
Year: 2022
"""

import time
import threading
import numpy as np
from ctypes import windll
from tkinter import *
import pyautogui
from keras.models import load_model
from keras.preprocessing import image


# ── Configuration ──────────────────────────────────────────────────────────────
MODEL_PATH = "models/models_9.h5"
CATEGORIES = ["gory", "not_gory"]
SCREENSHOT_REGION = (200, 100, 1000, 600)
IMAGE_SIZE = (200, 200)
COOLDOWN_ADULT = 20       # seconds to wait after detection (adult mode)
COOLDOWN_CHILD = 1        # seconds between checks (child mode)
MAX_VIOLATIONS_CHILD = 3  # violations before alert in child mode

# ── DPI Awareness (Windows) ────────────────────────────────────────────────────
windll.shcore.SetProcessDpiAwareness(1)

# ── Load Model ─────────────────────────────────────────────────────────────────
print("[INFO] Loading model...")
model = load_model(MODEL_PATH)
print("[INFO] Model loaded successfully.")


# ── Prediction Helper ──────────────────────────────────────────────────────────
def predict_screenshot(region=None):
    """Capture screenshot, preprocess, and return prediction index."""
    screenshot = pyautogui.screenshot('screenshot.jpg', region=region)
    img_array = image.img_to_array(screenshot.resize(IMAGE_SIZE))
    x = np.array([img_array])
    prediction = model.predict(x)
    return int(np.argmax(prediction, axis=1)[0])


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 1 — Age Verification
# ══════════════════════════════════════════════════════════════════════════════
class AgeVerificationScreen:
    def __init__(self):
        self.root = Tk()
        self.root.title("Violence Detection — Age Verification")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#0A0A2E")
        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        Label(
            self.root,
            text="🛡️ Violence Detection System",
            font=("Helvetica", 36, "bold"),
            fg="white", bg="#0A0A2E"
        ).pack(pady=80)

        Label(
            self.root,
            text="This application monitors your screen and protects you\n"
                 "and your children from violent content.",
            font=("Helvetica", 18),
            fg="#A0A0C0", bg="#0A0A2E",
            justify=CENTER
        ).pack(pady=20)

        Label(
            self.root,
            text="Are you older than 18 years?",
            font=("Helvetica", 24, "bold"),
            fg="white", bg="#0A0A2E"
        ).pack(pady=40)

        btn_frame = Frame(self.root, bg="#0A0A2E")
        btn_frame.pack()

        Button(
            btn_frame, text="✓  Yes", bg="#27AE60", fg="white",
            font=("Helvetica", 20, "bold"), bd=0,
            height=2, width=12, cursor="hand2",
            command=self._adult_mode
        ).pack(side=LEFT, padx=30)

        Button(
            btn_frame, text="✗  No", bg="#E74C3C", fg="white",
            font=("Helvetica", 20, "bold"), bd=0,
            height=2, width=12, cursor="hand2",
            command=self._child_mode
        ).pack(side=LEFT, padx=30)

    def _adult_mode(self):
        self.root.destroy()
        MonitorScreen(child_mode=False)

    def _child_mode(self):
        self.root.destroy()
        MonitorScreen(child_mode=True)


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 2 — Monitor Screen (Adult & Child Modes)
# ══════════════════════════════════════════════════════════════════════════════
class MonitorScreen:
    def __init__(self, child_mode=False):
        self.child_mode = child_mode
        self.violations = 0
        self.start_event = threading.Event()

        self.root = Tk()
        self.root.title("Violence Detection — Monitoring")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#0A0A2E")
        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        mode_label = "👶 Child Protection Mode" if self.child_mode else "🧑 Adult Mode"
        Label(
            self.root,
            text="🛡️ Protection from Violent Content",
            font=("Helvetica", 30, "bold"),
            fg="white", bg="#0A0A2E"
        ).pack(pady=60)

        Label(
            self.root, text=mode_label,
            font=("Helvetica", 18),
            fg="#F39C12", bg="#0A0A2E"
        ).pack()

        desc = (
            "Press START to begin monitoring.\n"
            "When violent content is detected, the screen will be covered immediately."
        )
        Label(
            self.root, text=desc,
            font=("Helvetica", 14),
            fg="#A0A0C0", bg="#0A0A2E",
            justify=CENTER
        ).pack(pady=30)

        btn_frame = Frame(self.root, bg="#0A0A2E")
        btn_frame.pack(pady=20)

        Button(
            btn_frame, text="▶  START", bg="#27AE60", fg="white",
            font=("Helvetica", 18, "bold"), bd=0,
            height=2, width=12, cursor="hand2",
            command=self._start
        ).pack(side=LEFT, padx=20)

        Button(
            btn_frame, text="■  STOP", bg="#E74C3C", fg="white",
            font=("Helvetica", 18, "bold"), bd=0,
            height=2, width=12, cursor="hand2",
            command=self._stop
        ).pack(side=LEFT, padx=20)

        Button(
            btn_frame, text="←  BACK", bg="#7F8C8D", fg="white",
            font=("Helvetica", 18, "bold"), bd=0,
            height=2, width=12, cursor="hand2",
            command=self._back
        ).pack(side=LEFT, padx=20)

        self.status_label = Label(
            self.root, text="● Status: Idle",
            font=("Helvetica", 16),
            fg="#95A5A6", bg="#0A0A2E"
        )
        self.status_label.pack(pady=20)

    def _start(self):
        if not self.start_event.is_set():
            self.status_label.config(text="● Status: Monitoring...", fg="#2ECC71")
            threading.Thread(target=self._monitor_loop, daemon=True).start()

    def _stop(self):
        self.start_event.clear()
        self.status_label.config(text="● Status: Stopped", fg="#E74C3C")

    def _back(self):
        self.start_event.clear()
        self.root.destroy()
        AgeVerificationScreen()

    def _monitor_loop(self):
        self.start_event.set()
        region = SCREENSHOT_REGION if not self.child_mode else None

        while self.start_event.is_set():
            prediction = predict_screenshot(region=region)
            print(f"[PREDICT] {CATEGORIES[prediction]}")

            if prediction == 0:  # gory detected
                self.violations += 1
                if self.child_mode and self.violations >= MAX_VIOLATIONS_CHILD:
                    self.root.after(0, self._show_child_alert)
                    self.start_event.clear()
                else:
                    self.root.after(0, self._show_adult_warning)
                    time.sleep(COOLDOWN_ADULT)
                    continue

            time.sleep(COOLDOWN_CHILD)

    def _show_adult_warning(self):
        AlertScreen(child_mode=False)

    def _show_child_alert(self):
        AlertScreen(child_mode=True)


# ══════════════════════════════════════════════════════════════════════════════
# SCREEN 3 — Alert Screen
# ══════════════════════════════════════════════════════════════════════════════
class AlertScreen:
    def __init__(self, child_mode=False):
        self.child_mode = child_mode
        self.root = Tk()
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#8B0000")
        self.root.title("⚠️ Violent Content Detected")
        self._build_ui()
        self.root.mainloop()

    def _build_ui(self):
        Label(
            self.root,
            text="⚠️ WARNING",
            font=("Helvetica", 60, "bold"),
            fg="white", bg="#8B0000"
        ).pack(pady=80)

        if self.child_mode:
            msg = (
                "Violent content has been detected multiple times.\n"
                "Please notify a parent or guardian immediately."
            )
        else:
            msg = (
                "This screen may contain violent or gory content.\n"
                "We advise you to close the window.\n\n"
                "Monitoring will resume in 40 seconds."
            )

        Label(
            self.root, text=msg,
            font=("Helvetica", 22),
            fg="white", bg="#8B0000",
            justify=CENTER
        ).pack(pady=30)

        Button(
            self.root, text="✓  I Understand — Close",
            bg="white", fg="#8B0000",
            font=("Helvetica", 18, "bold"), bd=0,
            height=2, width=25, cursor="hand2",
            command=self.root.destroy
        ).pack(pady=40)


# ══════════════════════════════════════════════════════════════════════════════
# Entry Point
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    AgeVerificationScreen()
