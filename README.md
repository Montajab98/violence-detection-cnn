# Violent Content Detection — Graduation Project

A Windows desktop application that periodically captures the screen, classifies the image using a saved Keras model, and displays a warning when the predicted class is `gory`.

Developed as a Bachelor's graduation project at Tishreen University in 2022. The published repository contains the application code, not a complete reproducible training pipeline.

## What is included

- `app.py`: Tkinter age selection, monitoring controls, screenshot inference, and warning windows.
- `requirements.txt`: the application's pinned Python dependencies.
- `.gitignore`: excludes model weights, datasets, runtime screenshots, environments, and caches.

The code loads `models/models_9.h5`. **The trained model, training notebook, dataset, and evaluation artifacts are not included.** You need compatible trained weights before the application can run; there is currently no published download in this repository.

## Requirements

- Windows and Python 3.10 for the pinned dependency stack.
- A desktop session that allows screen capture.
- Compatible Keras model weights with the expected preprocessing and class order.

The Windows restriction comes from the `ctypes.windll` DPI-awareness call. This version is not directly portable to macOS or Linux. A GPU is not specified as a requirement by the application code.

## Setup

```sh
git clone https://github.com/Montajab98/violence-detection-cnn.git
cd violence-detection-cnn
python -m venv .venv
```

Activate on Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Place trusted, compatible weights at `models/models_9.h5`, then run from the repository root:

```sh
python app.py
```

Without the weights, loading the application will fail. Only load model files from a trusted source.

## Inference flow

```text
Screen capture -> resize to 200 x 200 -> convert to NumPy array
               -> model.predict -> highest-scoring class -> warning if gory
```

The code expects class order `gory`, `not_gory`. It does not normalize pixels in the application before prediction; compatibility with the original training preprocessing must be checked against the supplied model.

Adult mode captures the configured screen region; child mode captures the full screen and counts detections. Screenshots are also saved as `screenshot.jpg`, which is overwritten during inference. Use a controlled demo screen without private information.

## Historical results and verification limits

Earlier documentation reported **98% accuracy** and described a ResNet-50 training experiment. Those results cannot be independently reproduced from this repository because the training code, weights, split manifest, and evaluation output are absent. Treat the figure as a historical reported result, **not a verified benchmark**.

Before citing a measured result, publish the evaluation procedure and artifacts: source-level train/validation/test separation, augmentation applied after separation, class balance, confusion matrix, precision, recall, F1, and the evaluated model version. Similar frames from the same video should not cross evaluation splits.

## Known limitations

- This is an educational prototype, not a validated child-safety or content-filtering product. False positives and false negatives are possible.
- The model file and a reproducible training/evaluation pipeline are missing.
- The code sets an adult detection cooldown of 20 seconds, while the warning text says 40 seconds. There is no implemented automatic close timer for that warning window.
- GUI windows and the monitoring thread need further lifecycle testing, including repeated start/stop actions.
- There is no automated test suite in this repository. This documentation repair did not run the Windows application or verify model accuracy.

## Author and licensing

[Montajab Al-Hussein](https://github.com/Montajab98) · [LinkedIn](https://www.linkedin.com/in/moontajab/)

No license file is currently included. Earlier MIT-license text did not include a license grant file; licensing should be clarified by the owner before reuse.
