import axios from "axios";
import React, { useState } from "react";
import { toast } from "react-toastify";
import { AiOutlineEye, AiOutlineEyeInvisible } from "react-icons/ai";
import { useNavigate } from "react-router-dom";

const url = import.meta.env.VITE_SERVER_URI || "http://localhost:3000";
const Registration = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userName, setUserName] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const { data } = await axios.post(`${url}/user/register`, {
        name: userName,
        email,
        password,
      });

      if (data.status) {
        toast.success("Registration Successful");
        console.log("User registered:", data);
        navigate("/login"); // Redirect user to login page after successful registration
      } else {
        toast.error(
          "Registration Failed: " + (data.message || "Unknown error")
        );
      }
    } catch (err) {
      toast.error("Registration Failed");
      console.error("Error while registration:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-50 px-4">
      <div className="w-full max-w-md p-8 bg-white shadow-lg rounded-2xl">
        <div className="text-center mb-6">
          <h2 className="text-2xl font-bold text-gray-800 mt-4">Sign up</h2>
        </div>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="userName"
              className="text-sm font-medium text-gray-700"
            >
              Name
            </label>
            <input
              type="text"
              id="userName"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-800"
              placeholder="Enter your name"
            />
          </div>
          <div>
            <label
              htmlFor="email"
              className="text-sm font-medium text-gray-700"
            >
              Email
            </label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-800"
              placeholder="Enter your email"
            />
          </div>
          <div className="relative">
            <label
              htmlFor="password"
              className="text-sm font-medium text-gray-700"
            >
              Password
            </label>
            <div className="relative w-full">
              <input
                type={showPassword ? "text" : "password"}
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="w-full px-4 py-3 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 text-sm text-gray-800 pr-10"
                placeholder="Enter your password"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute inset-y-0 right-3 flex items-center text-gray-600 cursor-pointer"
              >
                {showPassword ? (
                  <AiOutlineEyeInvisible size={20} />
                ) : (
                  <AiOutlineEye size={20} />
                )}
              </button>
            </div>
          </div>
          <button
            disabled={loading}
            type="submit"
            className="w-full py-3 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-70 cursor-pointer"
          >
            {loading ? "Signing up..." : "Sign up"}
          </button>
          <p className="text-center text-sm text-gray-700">
            Already have an account?
            <button
              onClick={() => navigate("/login")}
              className="text-blue-600 hover:underline font-semibold ml-1 cursor-pointer"
            >
              Sign in
            </button>
          </p>
        </form>
      </div>
    </div>
  );
};

export default Registration;
