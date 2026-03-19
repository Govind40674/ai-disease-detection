import React, { useState, useRef, useEffect } from "react";
import { Link } from "react-router-dom";
import styles from "./header.module.css";

function Header() {
  const [open, setOpen] = useState(false);
  const menuRef = useRef();

  // Close when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      if (menuRef.current && !menuRef.current.contains(e.target)) {
        setOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <header className={styles.header}>
      <div className={styles.inner}>
        
        <h1 className={styles.title}>AI Disease Prediction</h1>

        <div className={styles.menu} ref={menuRef}>
          <button
            onClick={() => setOpen(!open)}
            className={styles.menuBtn}
          >
            ⋮
          </button>

          <div className={`${styles.dropdown} ${open ? styles.show : ""}`}>
            <Link to="/" onClick={() => setOpen(false)}>Home</Link>
            <Link to="/chest" onClick={() => setOpen(false)}>Chest X-ray</Link>
            <Link to="/eye" onClick={() => setOpen(false)}>Eye Disease</Link>
            <Link to="/skin" onClick={() => setOpen(false)}>Skin Disease</Link>
            <Link to="/kidney" onClick={() => setOpen(false)}>Kidney Disease</Link>
          </div>
        </div>

      </div>
    </header>
  );
}

export default Header;