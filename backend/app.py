from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import tensorflow as tf
import joblib
import io

app = FastAPI()

# -------------------------------
# Allow frontend access
# -------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =====================================================
# TB MODEL
# =====================================================

tb_interpreter = tf.lite.Interpreter(model_path="model_Chest_Tuber.tflite")
tb_interpreter.allocate_tensors()

tb_input_details = tb_interpreter.get_input_details()
tb_output_details = tb_interpreter.get_output_details()

print("TB model loaded successfully")

# -------------------------------
# Load metadata scaler
# -------------------------------

scaler = joblib.load("meta_scaler.pkl")

print("Scaler loaded successfully")


# =====================================================
# KIDNEY MODEL
# =====================================================

kidney_interpreter = tf.lite.Interpreter(
    model_path="kidney_model_quant.tflite"
)

kidney_interpreter.allocate_tensors()

kidney_input_details = kidney_interpreter.get_input_details()
kidney_output_details = kidney_interpreter.get_output_details()

print("Kidney model loaded successfully")


# =====================================================
# IMAGE PREPROCESSING
# =====================================================

def preprocess_tb_image(image_bytes):

    img = Image.open(io.BytesIO(image_bytes)).convert("L")

    img = img.resize((128, 128))

    img_array = np.array(img) / 255.0

    img_array = np.expand_dims(img_array, axis=-1)

    img_array = np.expand_dims(img_array, axis=0)

    return img_array.astype(np.float32)


def preprocess_kidney_image(image_bytes):

    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    img = img.resize((224, 224))

    img_array = np.array(img) / 255.0

    img_array = np.expand_dims(img_array, axis=0)

    return img_array.astype(np.float32)


# =====================================================
# METADATA PREPROCESSING
# =====================================================

def preprocess_metadata(age, gender):

    age = float(age)

    if gender.lower() == "m":
        gender_val = 1
    else:
        gender_val = 0

    meta = np.array([[age, gender_val]])

    meta = scaler.transform(meta)

    return meta.astype(np.float32)


# =====================================================
# TB PREDICTION API
# =====================================================

@app.post("/predict/tb")
async def predict_tb(
    file: UploadFile = File(...),
    age: float = Form(...),
    gender: str = Form(...)
):

    contents = await file.read()

    img_array = preprocess_tb_image(contents)

    meta_array = preprocess_metadata(age, gender)

    tb_interpreter.set_tensor(
        tb_input_details[0]['index'],
        img_array
    )

    tb_interpreter.set_tensor(
        tb_input_details[1]['index'],
        meta_array
    )

    tb_interpreter.invoke()

    output = tb_interpreter.get_tensor(
        tb_output_details[0]['index']
    )

    prob = float(output[0][0])

    if prob > 0.5:
        label = "Tuberculosis Detected"
    else:
        label = "Normal"

    return {
        "class": label,
        "confidence": prob
    }


# =====================================================
# KIDNEY PREDICTION API
# =====================================================

@app.post("/predict/kidney")
async def predict_kidney(file: UploadFile = File(...)):

    contents = await file.read()

    img_array = preprocess_kidney_image(contents)

    kidney_interpreter.set_tensor(
        kidney_input_details[0]['index'],
        img_array
    )

    kidney_interpreter.invoke()

    output = kidney_interpreter.get_tensor(
        kidney_output_details[0]['index']
    )

    classes = ["Cyst", "Normal", "Stone", "Tumor"]

    pred_index = int(np.argmax(output))

    confidence = float(np.max(output))

    label = classes[pred_index]

    return {
        "class": label,
        "confidence": confidence
    }