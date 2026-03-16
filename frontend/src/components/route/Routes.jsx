import React, { Suspense, lazy } from "react";
import { Routes, Route } from "react-router-dom";
import styles from "./route.module.css";

// Lazy loaded pages
const Home = lazy(() => import("../../pages/home/Home"));


const Tuber = lazy(() => import("../../pages/chest/chest_disease/tuber/Tuber"));
const Chest_home = lazy(() => import("../../pages/chest/chest_home/Chest_home"));
const Not_found=lazy(() => import("../../pages/not_found/Not_found"));
const Kidney_home=lazy(() => import("../../pages/kidney/kidney_home/Kidney_home"));
const NCTS=lazy(() => import("../../pages/kidney/kidney_disease/NCTS/NCTS"));
const Eye_home=lazy(() => import("../../pages/eye/eye_home/Eye_home"));
const Retinal_fundus=lazy(() => import("../../pages/eye/eye_disease/retinal_fundus/Retinal_fundus"));
const Skin_home=lazy(() => import("../../pages/skin/skin_home/Skin_home"));

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
          <Route path="/eye" element={<Eye_home />} />
          <Route path="/skin" element={<Skin_home />} />
          <Route path="/kidney" element={<Kidney_home />} />
          <Route path="/kidney/ncts" element={<NCTS />} />
          <Route path="/eye/retinal_fundus" element={<Retinal_fundus />} />
          
          <Route path="*" element={<Not_found />} />
        </Routes>
      </Suspense>
    </div>
  );
}

export default AppRoutes;