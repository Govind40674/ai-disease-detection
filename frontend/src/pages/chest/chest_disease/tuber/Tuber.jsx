import React, { useState } from "react";
import axios from "axios";
import styles from './chest_tuber.module.css';
import Footer from "../../../../components/footer/Footer";
import Header from "../../../../components/header/Header";
function Tuber() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [age, setAge] = useState("");
  const [gender, setGender] = useState("male");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFile = (e) => {
    const selected = e.target.files[0];
    if (selected) {
      setFile(selected);
      setPreview(URL.createObjectURL(selected));
    }
  };

  const handlePredict = async () => {
    if (!file || !age || !gender) {
      alert("Please upload X-ray, enter age, and select gender");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);
    formData.append("age", age);
    formData.append("gender", gender);

    try {
      setLoading(true);
      
      const res=await axios.post(`${import.meta.env.VITE_API_URL}/predict/tb`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Prediction failed. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
    <Header/>
    <div className={styles.container}>
      <h1>TB Detection (Chest X-ray)</h1>

      <input type="file" accept="image/*" onChange={handleFile} />

      {preview && (
        <img src={preview} alt="preview" className={styles.preview} />
      )}

      <div className={styles.form}>
        <input
          type="number"
          placeholder="Enter age"
          value={age}
          onChange={(e) => setAge(e.target.value)}
        />

        <select value={gender} onChange={(e) => setGender(e.target.value)}>
          <option value="male">Male</option>
          <option value="female">Female</option>
        </select>
      </div>

      <button  className={styles.open}onClick={handlePredict} disabled={loading}>
        {loading ? "Predicting..." : "Check TB"}
      </button>

      {result && (
        <div className={styles.result}>

          <h2>Result: {result.class}</h2>
          <p>Confidence: {result.confidence}</p>
        </div>
      )}
    </div>

    <Footer/>
    </>
  );
}

export default Tuber;