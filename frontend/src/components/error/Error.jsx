import React from "react";
import { Link } from "react-router-dom";
import styles from "./Error.module.css";

function Error() {
  return (
    <div className={styles.wrapper}>
      <div className={styles.container}>
        <h1 className={styles.code}>404</h1>
        <p className={styles.text}>Oops! Page Not Found</p>
        <Link className={styles.btn} to="/">Go Back Home</Link>
      </div>
    </div>
  );
}

export default Error;