import React, { Suspense, lazy } from "react";
import { Routes, Route } from "react-router-dom";
import styles from "./route.module.css";

// Lazy loaded pages
const Home = lazy(() => import("../../pages/home/Home"));
const Eye = lazy(() => import("../../pages/eye/Eye"));
const Skin = lazy(() => import("../../pages/skin/Skin"));
const Tuber = lazy(() => import("../../pages/chest/chest_disease/Tuber"));
const Chest_home = lazy(() => import("../../pages/chest/chest_home/Chest_home"));

function AppRoutes() {
  return (
    <div className={styles.routeContainer}>
      <Suspense
        fallback={
          <div className={styles.loadingContainer}>
            <div className={styles.loader}></div>
            <p className={styles.loadingText}>Loading Page...</p>
          </div>
        }
      >
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chest" element={<Chest_home />} />
          <Route path="/chest/tuberculosis" element={<Tuber />} />
          <Route path="/eye" element={<Eye />} />
          <Route path="/skin" element={<Skin />} />
        </Routes>
      </Suspense>
    </div>
  );
}

export default AppRoutes;