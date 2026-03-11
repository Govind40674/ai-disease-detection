from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import tensorflow as tf
import joblib
import io

app = FastAPI()

# Allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Load TFLite Model
# -------------------------------

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


# -------------------------------
# Image preprocessing
# -------------------------------

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("L")  # grayscale
    img = img.resize((128, 128))

    img_array = np.array(img) / 255.0

    img_array = np.expand_dims(img_array, axis=-1)  # channel
    img_array = np.expand_dims(img_array, axis=0)   # batch

    return img_array.astype(np.float32)


# -------------------------------
# Metadata preprocessing
# -------------------------------

def preprocess_metadata(age, gender):

    age = float(age)

    if gender.lower() == "m":
        gender_val = 1
    else:
        gender_val = 0

    meta = np.array([[age, gender_val]])

    meta = scaler.transform(meta)

    return meta.astype(np.float32)


# -------------------------------
# TB Prediction API
# -------------------------------

@app.post("/predict/tb")
async def predict_tb(
    file: UploadFile = File(...),
    age: float = Form(...),
    gender: str = Form(...)
):

    contents = await file.read()

    # preprocess image
    img_array = preprocess_image(contents)

    # preprocess metadata
    meta_array = preprocess_metadata(age, gender)

    # set tensors
    tb_interpreter.set_tensor(tb_input_details[0]['index'], img_array)
    tb_interpreter.set_tensor(tb_input_details[1]['index'], meta_array)

    # run model
    tb_interpreter.invoke()

    output = tb_interpreter.get_tensor(tb_output_details[0]['index'])

    prob = float(output[0][0])

    if prob > 0.5:
        label = "Tuberculosis Detected"
    else:
        label = "Normal"

    return {
        "class": label,
        "confidence": prob
    }