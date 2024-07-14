import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import RegisterPage from "./screens/register";
import CongratPage from "./screens/congrats";
import RandomPage from "./screens/random";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RegisterPage />} />
        <Route path="/congrats" element={<CongratPage />} />
        <Route path="/random" element={<RandomPage />} />
      </Routes>
    </Router>
  );
}

export default App;
