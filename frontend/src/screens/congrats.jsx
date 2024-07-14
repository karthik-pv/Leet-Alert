import React from "react";
import congratsImage from "../assets/congrats.jpg"; // Adjust the path according to your folder structure

const CongratPage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-black">
      <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-center text-white mb-6">
        You have subscribed to Leetcode Daily
      </h1>
      <div className="w-full max-w-3xl px-4">
        <img
          src={congratsImage}
          alt="Congrats"
          className="w-full h-auto object-contain"
        />
      </div>
    </div>
  );
};

export default CongratPage;
