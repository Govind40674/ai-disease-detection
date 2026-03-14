import React from "react";
import styles from "./first_page.module.css";
import { Link } from "react-router-dom";

function First_page() {
  return (
    <>
      <div className={styles.container}>

        <div className={styles.content}>
          <img src="/chest_X_ray.png" alt="chest-xray" />
          <h1>AI Disease Detection</h1>
          <Link className={styles.link} to="/chest">Chest X-ray</Link>
        </div>

        <div className={styles.content}>
          <img src="/eye.png" alt="eye" />
          <h1>AI Disease Detection</h1>
          <Link className={styles.link} to="/eye">Eye Disease</Link>
        </div>

        <div className={styles.content}>
          <img src="/skin.png" alt="skin" />
          <h1>AI Disease Detection</h1>
          <Link className={styles.link} to="/skin">Skin Disease</Link>
        </div>

        <div className={styles.content}>
          <img src="/ct_scan_kidney.png" alt="kidney" />
          <h1>AI Disease Detection</h1>
          <Link className={styles.link} to="/kidney">Kidney Disease</Link>
        </div>

      </div>
    </>
  );
}

export default First_page;