import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import backgroundImage from "../assets/background.jpg";
import { BASE_URL } from "../api/urls";
import axios from "axios";

const RegisterPage = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      alert("Please enter a valid email address.");
      return;
    }

    console.log("Email submitted:", email);
    try {
      const response = await axios.post(BASE_URL + "/register", {
        email: email,
      });
      console.log("Response:", response.data);
      navigate("/congrats");
    } catch (error) {
      console.error("There was an error!", error);
    }
  };

  const handleRandom = async (e) => {
    e.preventDefault();

    // Basic email validation regex
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!emailRegex.test(email)) {
      alert("Please enter a valid email address.");
      return;
    }

    try {
      const response = await axios.post(BASE_URL + "/random", {
        email: email,
      });
      navigate(`/random`);
    } catch (error) {
      console.error("There was an error fetching random problem!", error);
    }
  };

  return (
    <div
      className="min-h-screen flex items-center justify-center bg-cover bg-center"
      style={{
        backgroundImage: `url(${backgroundImage})`,
        backgroundSize: "cover",
        backgroundPosition: "center",
        backgroundRepeat: "no-repeat",
      }}
    >
      <div className="max-w-md w-full bg-white p-6 sm:p-8 md:p-10 lg:p-12 rounded-lg shadow-lg bg-opacity-90">
        <h2 className="text-2xl sm:text-3xl md:text-4xl font-bold mb-4 sm:mb-6 md:mb-8 text-center text-black">
          Register
        </h2>
        <form onSubmit={handleSubmit}>
          <div className="mb-3 sm:mb-4 md:mb-5">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-gray-700"
            >
              Email address
            </label>
            <input
              type="email"
              id="email"
              name="email"
              className="mt-1 block w-full px-3 py-2 sm:px-4 sm:py-2 md:px-5 md:py-3 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm md:text-base"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="flex flex-row justify-center">
            <div className="flex items-center justify-center pr-5">
              <Link to="/congrats">
                <button
                  type="submit"
                  className="w-full py-2 sm:py-2.5 md:py-3 px-4 border border-transparent rounded-md shadow-sm text-sm sm:text-base font-medium text-white bg-green-500 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  onClick={handleSubmit}
                >
                  Subscribe
                </button>
              </Link>
            </div>
            <div className="flex items-center justify-center">
              <Link to="/random">
                <button
                  type="submit"
                  className="w-full py-2 sm:py-2.5 md:py-3 px-4 border border-transparent rounded-md shadow-sm text-sm sm:text-base font-medium text-white bg-green-500 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  onClick={handleRandom}
                >
                  Get Random
                </button>
              </Link>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
};

export default RegisterPage;
