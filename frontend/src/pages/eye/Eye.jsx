
import React, { useState } from "react";
import axios from "axios";
import styles from "./eye.module.css";

function Eye() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [confidence, setConfidence] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
      setResult(null);
      setConfidence(null);
      setError("");
    }
  };

  const handlePredict = async () => {
    if (!file) {
      setError("Please upload an image first.");
      return;
    }

    try {
      setLoading(true);
      setError("");

      const formData = new FormData();
      formData.append("file", file);

    
      const res = await axios.post(
  `${import.meta.env.VITE_API_URL}/predict/eye`,
  formData,
  {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  }
);
console.log( "res",res.data);
      setResult(res.data.class);
      setConfidence(res.data.confidence);
    } catch (err) {
      console.error(err);
      setError("Prediction failed. Is backend running?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Eye Disease Detection (Cataract)</h1>

      <div className={styles.card}>
        
   <div className={styles.uploadBox}>
  <input type="file" accept="image/*" onChange={handleFileChange} />
  <p>Upload an eye image</p>

</div>

        {preview && (
          <div className={styles.previewBox}>
            <img src={preview} alt="preview" />
          </div>
        )}

        <button className={styles.btn} onClick={handlePredict} disabled={loading}>
          {loading ? "Predicting..." : "Predict"}
        </button>

        {/* Result */}
        <div className={styles.result}>
          {error && <p style={{ color: "#f87171" }}>{error}</p>}

          {!error && (
            <>
              <p>
                Result: <span>{result || "---"}</span>
              </p>
              <p>
                Confidence: <span>{confidence ? `${confidence * 100}%` : "---"}</span>
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default Eye;