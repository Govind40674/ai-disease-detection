from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import io
from PIL import Image


try:
    import tflite_runtime.interpreter as tflite
except ImportError:
    import tensorflow.lite as tflite

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# LOAD TFLITE MODEL
# -----------------------------

interpreter = tflite.Interpreter(model_path="model.tflite")
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

eye_class_names = ["cataract", "normal"]

print("Model loaded successfully")

# -----------------------------
# IMAGE PREPROCESSING
# -----------------------------

def preprocess_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))

    img_array = np.array(img).astype(np.float32) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    return img_array


# -----------------------------
# PREDICT ROUTE
# -----------------------------

@app.post("/predict/eye")
async def predict_eye(file: UploadFile = File(...)):
    
    image_bytes = await file.read()
    img_array = preprocess_image(image_bytes)

    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()

    pred_probs = interpreter.get_tensor(output_details[0]['index'])[0]

    pred_idx = int(np.argmax(pred_probs))
    predicted_class = eye_class_names[pred_idx]
    confidence = float(pred_probs[pred_idx])

    return {
        "class": predicted_class,
        "confidence": round(confidence, 4)
    }