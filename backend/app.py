# from fastapi import FastAPI, UploadFile, File, Form
# from fastapi.middleware.cors import CORSMiddleware
# import numpy as np
# from PIL import Image
# import tensorflow as tf
# import joblib
# import io

# app = FastAPI()

# # ===================================================
# # ALLOW FRONTEND ACCESS
# # ===================================================

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # ===================================================
# # TB MODEL
# # ===================================================

# tb_interpreter = tf.lite.Interpreter(
#     model_path="model_Chest_Tuber.tflite"
# )

# tb_interpreter.allocate_tensors()

# tb_input_details = tb_interpreter.get_input_details()
# tb_output_details = tb_interpreter.get_output_details()

# print("TB model loaded successfully")

# # ===================================================
# # LOAD METADATA SCALER
# # ===================================================

# scaler = joblib.load("meta_scaler.pkl")
# print("Scaler loaded successfully")

# # ===================================================
# # KIDNEY MODEL
# # ===================================================

# kidney_interpreter = tf.lite.Interpreter(
#     model_path="kidney_model_quant.tflite"
# )

# kidney_interpreter.allocate_tensors()

# kidney_input_details = kidney_interpreter.get_input_details()
# kidney_output_details = kidney_interpreter.get_output_details()

# print("Kidney model loaded successfully")

# # ===================================================
# # RETINA FUNDUS MODEL
# # ===================================================

# retina_interpreter = tf.lite.Interpreter(
#     model_path="retinal_fundus_quant.tflite"
# )

# retina_interpreter.allocate_tensors()

# retina_input_details = retina_interpreter.get_input_details()
# retina_output_details = retina_interpreter.get_output_details()

# print("Retina model loaded successfully")

# # ===================================================
# # SKIN DISEASE MODEL (DERMNET)
# # ===================================================

# skin_interpreter = tf.lite.Interpreter(
#     model_path="dermnet_quant.tflite"
# )

# skin_interpreter.allocate_tensors()

# skin_input_details = skin_interpreter.get_input_details()
# skin_output_details = skin_interpreter.get_output_details()

# print("Skin disease model loaded successfully")

# # ===================================================
# # IMAGE PREPROCESSING
# # ===================================================

# def preprocess_tb_image(image_bytes):

#     img = Image.open(io.BytesIO(image_bytes)).convert("L")

#     img = img.resize((128, 128))

#     img_array = np.array(img) / 255.0

#     img_array = np.expand_dims(img_array, axis=-1)

#     img_array = np.expand_dims(img_array, axis=0)

#     return img_array.astype(np.float32)


# def preprocess_kidney_image(image_bytes):

#     img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

#     img = img.resize((224, 224))

#     img_array = np.array(img) / 255.0

#     img_array = np.expand_dims(img_array, axis=0)

#     return img_array.astype(np.float32)


# def preprocess_retina_image(image_bytes):

#     img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

#     img = img.resize((224, 224))

#     img_array = np.array(img) / 255.0

#     img_array = np.expand_dims(img_array, axis=0)

#     return img_array.astype(np.float32)


# def preprocess_skin_image(image_bytes):

#     img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

#     img = img.resize((224, 224))

#     img_array = np.array(img) / 255.0

#     img_array = np.expand_dims(img_array, axis=0)

#     return img_array.astype(np.float32)

# # ===================================================
# # METADATA PREPROCESSING
# # ===================================================

# def preprocess_metadata(age, gender):

#     age = float(age)

#     if gender.lower() == "m":
#         gender_val = 1
#     else:
#         gender_val = 0

#     meta = np.array([[age, gender_val]])

#     meta = scaler.transform(meta)

#     return meta.astype(np.float32)

# # ===================================================
# # TB PREDICTION API
# # ===================================================

# @app.post("/predict/tb")
# async def predict_tb(
#     file: UploadFile = File(...),
#     age: float = Form(...),
#     gender: str = Form(...)
# ):

#     contents = await file.read()

#     img_array = preprocess_tb_image(contents)

#     meta_array = preprocess_metadata(age, gender)

#     tb_interpreter.set_tensor(
#         tb_input_details[0]['index'],
#         img_array
#     )

#     tb_interpreter.set_tensor(
#         tb_input_details[1]['index'],
#         meta_array
#     )

#     tb_interpreter.invoke()

#     output = tb_interpreter.get_tensor(
#         tb_output_details[0]['index']
#     )

#     prob = float(output[0][0])

#     if prob > 0.5:
#         label = "Tuberculosis Detected"
#     else:
#         label = "Normal"

#     return {
#         "class": label,
#         "confidence": prob
#     }

# # ===================================================
# # KIDNEY PREDICTION API
# # ===================================================

# @app.post("/predict/kidney")
# async def predict_kidney(file: UploadFile = File(...)):

#     contents = await file.read()

#     img_array = preprocess_kidney_image(contents)

#     kidney_interpreter.set_tensor(
#         kidney_input_details[0]['index'],
#         img_array
#     )

#     kidney_interpreter.invoke()

#     output = kidney_interpreter.get_tensor(
#         kidney_output_details[0]['index']
#     )

#     classes = ["Cyst", "Normal", "Stone", "Tumor"]

#     pred_index = int(np.argmax(output))

#     confidence = float(np.max(output))

#     label = classes[pred_index]

#     return {
#         "class": label,
#         "confidence": confidence
#     }

# # ===================================================
# # RETINA FUNDUS PREDICTION API
# # ===================================================

# @app.post("/predict/retina")
# async def predict_retina(file: UploadFile = File(...)):

#     contents = await file.read()

#     img_array = preprocess_retina_image(contents)

#     retina_interpreter.set_tensor(
#         retina_input_details[0]['index'],
#         img_array
#     )

#     retina_interpreter.invoke()

#     output = retina_interpreter.get_tensor(
#         retina_output_details[0]['index']
#     )

#     classes = [
#         "ACRIMA",
#         "Glaucoma",
#         "ODIR-5K",
#         "ORIGA",
#         "Cataract",
#         "Retina Disease"
#     ]

#     pred_index = int(np.argmax(output))

#     confidence = float(np.max(output))

#     label = classes[pred_index]

#     return {
#         "class": label,
#         "confidence": confidence
#     }

# # ===================================================
# # SKIN DISEASE PREDICTION API
# # ===================================================

# @app.post("/predict/skin/dermnet")
# async def predict_skin(file: UploadFile = File(...)):

#     contents = await file.read()

#     img_array = preprocess_skin_image(contents)

#     skin_interpreter.set_tensor(
#         skin_input_details[0]['index'],
#         img_array
#     )

#     skin_interpreter.invoke()

#     output = skin_interpreter.get_tensor(
#         skin_output_details[0]['index']
#     )

#     skin_classes = [
#         "Acne and Rosacea Photos",
#         "Actinic Keratosis Basal Cell Carcinoma and other Malignant Lesions",
#         "Atopic Dermatitis Photos",
#         "Bullous Disease Photos",
#         "Cellulitis Impetigo and other Bacterial Infections",
#         "Eczema Photos",
#         "Exanthems and Drug Eruptions",
#         "Hair Loss Photos Alopecia and other Hair Diseases",
#         "Herpes HPV and other STDs Photos",
#         "Light Diseases and Disorders of Pigmentation",
#         "Lupus and other Connective Tissue diseases",
#         "Melanoma Skin Cancer Nevi and Moles",
#         "Nail Fungus and other Nail Disease",
#         "Poison Ivy Photos and other Contact Dermatitis",
#         "Psoriasis pictures Lichen Planus and related diseases",
#         "Scabies Lyme Disease and other Infestations and Bites",
#         "Seborrheic Keratoses and other Benign Tumors",
#         "Systemic Disease",
#         "Tinea Ringworm Candidiasis and other Fungal Infections",
#         "Urticaria Hives",
#         "Vascular Tumors",
#         "Vasculitis Photos",
#         "Warts Molluscum and other Viral Infections"
#     ]

#     pred_index = int(np.argmax(output))

#     confidence = float(np.max(output))

#     label = skin_classes[pred_index]

#     return {
#         "class": label,
#         "confidence": confidence
#     }








from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from PIL import Image

try:
    from tflite_runtime.interpreter import Interpreter
    print("✅ Using tflite-runtime")
except ImportError:
    import tensorflow as tf
    Interpreter = tf.lite.Interpreter
    print("✅ Using TensorFlow Lite")
import joblib
import io

app = FastAPI()

# ===================================================
# CORS (CORRECT)
# ===================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================================================
# GLOBAL VARIABLES (LAZY LOADING)
# ===================================================

tb_interpreter = None
kidney_interpreter = None
retina_interpreter = None
skin_interpreter = None
scaler = None

# ===================================================
# MODEL LOADERS
# ===================================================

def load_tb_model():
    global tb_interpreter, tb_input_details, tb_output_details
    if tb_interpreter is None:
        try:
            print("Loading TB model...")
            tb_interpreter = Interpreter(model_path="model_Chest_Tuber.tflite")
            tb_interpreter.allocate_tensors()
            tb_input_details = tb_interpreter.get_input_details()
            tb_output_details = tb_interpreter.get_output_details()
            print("TB model loaded")
        except Exception as e:
            print("❌ TB ERROR:", e)


def load_kidney_model():
    global kidney_interpreter, kidney_input_details, kidney_output_details
    if kidney_interpreter is None:
        try:
            print("Loading Kidney model...")
            kidney_interpreter = Interpreter(model_path="kidney_model_quant.tflite")
            kidney_interpreter.allocate_tensors()
            kidney_input_details = kidney_interpreter.get_input_details()
            kidney_output_details = kidney_interpreter.get_output_details()
            print("Kidney model loaded")
        except Exception as e:
            print("❌ Kidney ERROR:", e)


def load_retina_model():
    global retina_interpreter, retina_input_details, retina_output_details
    if retina_interpreter is None:
        try:
            print("Loading Retina model...")
            retina_interpreter = Interpreter(model_path="retinal_fundus_quant.tflite")
            retina_interpreter.allocate_tensors()
            retina_input_details = retina_interpreter.get_input_details()
            retina_output_details = retina_interpreter.get_output_details()
            print("Retina model loaded")
        except Exception as e:
            print("❌ Retina ERROR:", e)


def load_skin_model():
    global skin_interpreter, skin_input_details, skin_output_details
    if skin_interpreter is None:
        try:
            print("Loading Skin model...")
            skin_interpreter = Interpreter(model_path="dermnet_quant.tflite")
            skin_interpreter.allocate_tensors()
            skin_input_details = skin_interpreter.get_input_details()
            skin_output_details = skin_interpreter.get_output_details()
            print("Skin model loaded")
        except Exception as e:
            print("❌ Skin ERROR:", e)


def load_scaler():
    global scaler
    if scaler is None:
        scaler = joblib.load("meta_scaler.pkl")
        print("Scaler loaded")

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

        contents = await file.read()
        img_array = preprocess_retina_image(contents)

        print("Input shape:", img_array.shape)

        retina_interpreter.set_tensor(retina_input_details[0]['index'], img_array)
        retina_interpreter.invoke()

        output = retina_interpreter.get_tensor(retina_output_details[0]['index'])

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