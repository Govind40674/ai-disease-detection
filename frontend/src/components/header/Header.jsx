import React from "react";
import { Link } from "react-router-dom";
import styles from "./header.module.css";

function Header() {
  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        <h1 className={styles.title}>AI Disease Predictor</h1>


        
      </div>
      <div className={styles.link}>
        <nav className={styles.nav}>
          <Link className={styles.link} to="/chest">Chest X-ray</Link>
          <Link className={styles.link} to="/eye">Eye Disease</Link>
          <Link className={styles.link} to="/skin">Skin Disease</Link>
        </nav>
      </div>
    </header>
  );
}

export default Header;
