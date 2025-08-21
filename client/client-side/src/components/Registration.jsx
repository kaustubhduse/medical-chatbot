import axios from "axios";
import React, { useState } from "react";
import { toast } from "react-toastify";
import { AiOutlineEye, AiOutlineEyeInvisible, AiOutlineUserAdd } from "react-icons/ai";
import { useNavigate } from "react-router-dom";
// Import motion from Framer Motion
import { motion } from "framer-motion";

const url = import.meta.env.VITE_SERVER_URI || "http://localhost:3000";

// A reusable spinner component for the loading button
const LoadingSpinner = () => (
  <svg
    className="animate-spin h-5 w-5 text-white"
    xmlns="http://www.w3.org/2000/svg"
    fill="none"
    viewBox="0 0 24 24"
  >
    <circle
      className="opacity-25"
      cx="12"
      cy="12"
      r="10"
      stroke="currentColor"
      strokeWidth="4"
    ></circle>
    <path
      className="opacity-75"
      fill="currentColor"
      d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
    ></path>
  </svg>
);


const Registration = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [userName, setUserName] = useState("");
  const [loading, setLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userName || !email || !password) {
      toast.error("Please fill in all fields.");
      return;
    }
    setLoading(true);

    try {
      const { data } = await axios.post(`${url}/user/register`, {
        name: userName,
        email,
        password,
      });

      if (data.status) {
        toast.success("Registration Successful! Redirecting to login...");
        setTimeout(() => navigate("/login"), 1500); // Wait a bit before redirecting
      } else {
        toast.error(
          "Registration Failed: " + (data.message || "Unknown error")
        );
      }
    } catch (err) {
      toast.error(err.response?.data?.error || "Registration Failed");
      console.error("Error while registration:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-gray-100 to-blue-100 px-4">
      {/* Framer Motion animation for the form container */}
      <motion.div
        initial={{ opacity: 0, y: 50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: "easeInOut" }}
        className="w-full max-w-md p-8 space-y-8 bg-white shadow-2xl rounded-3xl"
      >
        <div className="text-center">
          <div className="inline-block p-3 mb-4 bg-blue-100 rounded-full">
            <AiOutlineUserAdd className="w-8 h-8 text-blue-600" />
          </div>
          <h2 className="text-3xl font-extrabold text-gray-900">
            Create an Account
          </h2>
          <p className="mt-2 text-sm text-gray-600">
            Join us and start your journey!
          </p>
        </div>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Floating Label Input for Name */}
          <div className="relative">
            <input
              type="text"
              id="userName"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
              // The 'peer' class is key for the floating label effect
              className="block w-full px-4 py-3 text-gray-900 bg-transparent border-2 border-gray-300 rounded-md appearance-none peer focus:outline-none focus:ring-0 focus:border-blue-600"
              placeholder=" "
            />
            <label
              htmlFor="userName"
              className="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-3"
            >
              Full Name
            </label>
          </div>

          {/* Floating Label Input for Email */}
          <div className="relative">
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              className="block w-full px-4 py-3 text-gray-900 bg-transparent border-2 border-gray-300 rounded-md appearance-none peer focus:outline-none focus:ring-0 focus:border-blue-600"
              placeholder=" "
            />
            <label
              htmlFor="email"
              className="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-3"
            >
              Email Address
            </label>
          </div>

          {/* Floating Label Input for Password */}
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="block w-full px-4 py-3 text-gray-900 bg-transparent border-2 border-gray-300 rounded-md appearance-none peer focus:outline-none focus:ring-0 focus:border-blue-600"
              placeholder=" "
            />
            <label
              htmlFor="password"
              className="absolute text-sm text-gray-500 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-white px-2 peer-focus:px-2 peer-focus:text-blue-600 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-3"
            >
              Password
            </label>
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-3 flex items-center text-gray-500 hover:text-blue-600 transition-colors"
            >
              {showPassword ? (
                <AiOutlineEyeInvisible size={22} />
              ) : (
                <AiOutlineEye size={22} />
              )}
            </button>
          </div>
          
          {/* Submit Button with animation and loading state */}
          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            disabled={loading}
            type="submit"
            className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-base font-medium text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
          >
            {loading ? <LoadingSpinner /> : "Sign up"}
          </motion.button>
          
          <p className="text-center text-sm text-gray-600">
            Already have an account?{" "}
            <span
              onClick={() => navigate("/login")}
              className="font-medium text-blue-600 hover:text-blue-500 cursor-pointer transition-colors"
            >
              Sign in
            </span>
          </p>
        </form>
      </motion.div>
    </div>
  );
};

export default Registration;