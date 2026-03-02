import React, { Suspense, lazy } from "react";
import { Routes, Route } from "react-router-dom";

// Lazy loaded pages
const Home = lazy(() => import("../../pages/home/Home"));
const Eye = lazy(() => import("../../pages/eye/Eye"));
const Skin = lazy(() => import("../../pages/skin/Skin"));
const Chest = lazy(() => import("../../pages/chest/Chest"));

function AppRoutes() {
  return (
    <Suspense fallback={<div style={{ padding: 20 }}>Loading page...</div>}>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/chest" element={<Chest />} />
        <Route path="/eye" element={<Eye />} />
        <Route path="/skin" element={<Skin />} />
      </Routes>
    </Suspense>
  );
}

export default AppRoutes;