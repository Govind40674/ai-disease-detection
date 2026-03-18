







from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image
import joblib
import io

# ===================================================
# INTERPRETER (WORKS BOTH LOCAL + RENDER)
# ===================================================




import tensorflow as tf
Interpreter = tf.lite.Interpreter

app = FastAPI()

# ===================================================
# CORS
# ===================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================================================
# GLOBAL VARIABLES
# ===================================================

tb_interpreter = None
kidney_interpreter = None
retina_interpreter = None
skin_interpreter = None
scaler = None

# ===================================================
# MODEL LOADERS (FIXED)
# ===================================================

def load_tb_model():
    global tb_interpreter, tb_input_details, tb_output_details

    if tb_interpreter is None:
        try:
            print("Loading TB model...")
            tb_interpreter = Interpreter(model_path="./model_Chest_Tuber.tflite")
            tb_interpreter.allocate_tensors()

            tb_input_details = tb_interpreter.get_input_details()
            tb_output_details = tb_interpreter.get_output_details()

            print("✅ TB model loaded")

        except Exception as e:
            print("❌ TB ERROR:", e)
            tb_interpreter = None
            raise e


def load_kidney_model():
    global kidney_interpreter, kidney_input_details, kidney_output_details

    if kidney_interpreter is None:
        try:
            print("Loading Kidney model...")
            kidney_interpreter = Interpreter(model_path="./kidney_model_quant.tflite")
            kidney_interpreter.allocate_tensors()

            kidney_input_details = kidney_interpreter.get_input_details()
            kidney_output_details = kidney_interpreter.get_output_details()

            print("✅ Kidney model loaded")

        except Exception as e:
            print("❌ Kidney ERROR:", e)
            kidney_interpreter = None
            raise e


def load_retina_model():
    global retina_interpreter, retina_input_details, retina_output_details

    if retina_interpreter is None:
        try:
            print("Loading Retina model...")

            retina_interpreter = Interpreter(
                model_path="./retinal_fundus_quant.tflite"
            )

            retina_interpreter.allocate_tensors()

            retina_input_details = retina_interpreter.get_input_details()
            retina_output_details = retina_interpreter.get_output_details()

            print("✅ Retina model loaded")

        except Exception as e:
            print("❌ Retina model failed:", e)
            retina_interpreter = None
            raise e  # 🔥 VERY IMPORTANT


def load_skin_model():
    global skin_interpreter, skin_input_details, skin_output_details

    if skin_interpreter is None:
        try:
            print("Loading Skin model...")
            skin_interpreter = Interpreter(model_path="./dermnet_quant.tflite")
            skin_interpreter.allocate_tensors()

            skin_input_details = skin_interpreter.get_input_details()
            skin_output_details = skin_interpreter.get_output_details()

            print("✅ Skin model loaded")

        except Exception as e:
            print("❌ Skin ERROR:", e)
            skin_interpreter = None
            raise e


def load_scaler():
    global scaler
    if scaler is None:
        scaler = joblib.load("meta_scaler.pkl")
        print("✅ Scaler loaded")

# ===================================================
# PREPROCESSING
# ===================================================

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


def preprocess_retina_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array.astype(np.float32)


def preprocess_skin_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    img = img.resize((224, 224))
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array.astype(np.float32)


def preprocess_metadata(age, gender):
    load_scaler()
    age = float(age)
    gender_val = 1 if gender.lower() == "m" else 0
    meta = np.array([[age, gender_val]])
    meta = scaler.transform(meta)
    return meta.astype(np.float32)

# ===================================================
# TB API
# ===================================================

@app.post("/predict/tb")
async def predict_tb(file: UploadFile = File(...), age: float = Form(...), gender: str = Form(...)):

    try:
        load_tb_model()

        if tb_interpreter is None:
            return {"error": "TB model failed to load"}

        contents = await file.read()
        img_array = preprocess_tb_image(contents)
        meta_array = preprocess_metadata(age, gender)

        tb_interpreter.set_tensor(tb_input_details[0]['index'], img_array)
        tb_interpreter.set_tensor(tb_input_details[1]['index'], meta_array)

        tb_interpreter.invoke()

        output = tb_interpreter.get_tensor(tb_output_details[0]['index'])

        prob = float(output[0][0])
        label = "Tuberculosis Detected" if prob > 0.5 else "Normal"

        return {"class": label, "confidence": prob}

    except Exception as e:
        print("❌ TB ERROR:", e)
        return {"error": str(e)}

# ===================================================
# KIDNEY API
# ===================================================

@app.post("/predict/kidney")
async def predict_kidney(file: UploadFile = File(...)):

    try:
        load_kidney_model()

        if kidney_interpreter is None:
            return {"error": "Kidney model failed to load"}

        contents = await file.read()
        img_array = preprocess_kidney_image(contents)

        kidney_interpreter.set_tensor(kidney_input_details[0]['index'], img_array)
        kidney_interpreter.invoke()

        output = kidney_interpreter.get_tensor(kidney_output_details[0]['index'])

        classes = ["Cyst", "Normal", "Stone", "Tumor"]

        pred_index = int(np.argmax(output))
        confidence = float(np.max(output))

        return {"class": classes[pred_index], "confidence": confidence}

    except Exception as e:
        print("❌ Kidney ERROR:", e)
        return {"error": str(e)}

# ===================================================
# RETINA API (FIXED)
# ===================================================

@app.post("/predict/retina")
async def predict_retina(file: UploadFile = File(...)):

    try:
        load_retina_model()

        if retina_interpreter is None:
            return {"error": "Retina model failed to load"}

        contents = await file.read()
        img_array = preprocess_retina_image(contents)

        print("Input shape:", img_array.shape)

        retina_interpreter.set_tensor(
            retina_input_details[0]['index'],
            img_array
        )

        retina_interpreter.invoke()

        output = retina_interpreter.get_tensor(
            retina_output_details[0]['index']
        )

        print("Output:", output)

        classes = ["ACRIMA", "Glaucoma", "ODIR-5K", "ORIGA", "Cataract", "Retina Disease"]

        pred_index = int(np.argmax(output))
        confidence = float(np.max(output))

        return {"class": classes[pred_index], "confidence": confidence}

    except Exception as e:
        print("❌ RETINA ERROR:", e)
        return {"error": str(e)}

# ===================================================
# SKIN API
# ===================================================

@app.post("/predict/skin/dermnet")
async def predict_skin(file: UploadFile = File(...)):

    try:
        load_skin_model()

        if skin_interpreter is None:
            return {"error": "Skin model failed to load"}

        contents = await file.read()
        img_array = preprocess_skin_image(contents)

        skin_interpreter.set_tensor(skin_input_details[0]['index'], img_array)
        skin_interpreter.invoke()

        output = skin_interpreter.get_tensor(skin_output_details[0]['index'])

        classes = [
            "Acne", "Actinic Keratosis", "Atopic Dermatitis", "Bullous Disease",
            "Cellulitis", "Eczema", "Drug Eruptions", "Hair Loss",
            "Herpes HPV", "Pigmentation Disorders", "Lupus",
            "Melanoma", "Nail Disease", "Contact Dermatitis",
            "Psoriasis", "Scabies", "Benign Tumors",
            "Systemic Disease", "Fungal Infection", "Urticaria",
            "Vascular Tumors", "Vasculitis", "Warts"
        ]

        pred_index = int(np.argmax(output))
        confidence = float(np.max(output))

        return {"class": classes[pred_index], "confidence": confidence}

    except Exception as e:
        print("❌ Skin ERROR:", e)
        return {"error": str(e)}