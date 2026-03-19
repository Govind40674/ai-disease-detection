import React, { useState } from "react";
import { Link } from "react-router-dom";
import styles from "./header.module.css";

function Header() {
  const [open, setOpen] = useState(false);

  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        
        {/* Center Title */}
        <h1 className={styles.title}>AI Disease Prediction</h1>

        {/* Three Dots */}
        <div className={styles.menu}>
          <button onClick={() => setOpen(!open)} className={styles.menuBtn}>
            ⋮
          </button>

          {/* Dropdown */}
          {open && (
            <div className={styles.dropdown}>
              <Link to="/" onClick={() => setOpen(false)}>Home</Link>
              <Link to="/chest" onClick={() => setOpen(false)}>Chest X-ray</Link>
              <Link to="/eye" onClick={() => setOpen(false)}>Eye Disease</Link>
              <Link to="/skin" onClick={() => setOpen(false)}>Skin Disease</Link>
              <Link to="/kidney" onClick={() => setOpen(false)}>Kidney Disease</Link>
            </div>
          )}
        </div>

      </div>
    </header>
  );
}

export default Header;
