import React from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { FiFileText, FiMessageSquare, FiShield } from "react-icons/fi";

const HomePage = () => {
  // Animation variants for the container to stagger children
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2,
      },
    },
  };

  // Animation variants for individual items
  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.6,
        ease: "easeInOut",
      },
    },
  };

  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center bg-slate-900 p-6 overflow-hidden">
      {/* Animated background shapes */}
      <div className="absolute top-0 -left-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-lighten filter blur-xl opacity-70 animate-blob"></div>
      <div className="absolute top-0 -right-4 w-72 h-72 bg-purple-500 rounded-full mix-blend-lighten filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
      <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-500 rounded-full mix-blend-lighten filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>

      <motion.div
        className="text-center max-w-4xl z-10"
        initial="hidden"
        animate="visible"
        variants={containerVariants}
      >
        {/* Introduction Section */}
        <motion.div variants={itemVariants}>
          <h1 className="text-5xl md:text-6xl font-extrabold text-white mb-4">
            Unlock Insights from Your{" "}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-purple-500">
              Medical Reports
            </span>
          </h1>
          <p className="text-lg text-gray-300 mb-8 max-w-2xl mx-auto">
            Securely upload your medical documents to get AI-powered summaries
            and chat support for a clearer understanding of your health.
          </p>
        </motion.div>

        {/* Action Buttons */}
        <motion.div
          className="flex flex-wrap justify-center gap-4 mb-20"
          variants={itemVariants}
        >
          <Link to="/medical-chatbot">
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: '0px 0px 20px rgba(59, 130, 246, 0.5)' }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-3 bg-blue-600 text-white font-semibold rounded-full shadow-lg hover:bg-blue-700 transition-all duration-300"
            >
              📄 Upload Report
            </motion.button>
          </Link>
          <Link to="/medical-chatbot">
            <motion.button
              whileHover={{ scale: 1.05, boxShadow: '0px 0px 20px rgba(34, 197, 94, 0.5)' }}
              whileTap={{ scale: 0.95 }}
              className="px-8 py-3 bg-green-600 text-white font-semibold rounded-full shadow-lg hover:bg-green-700 transition-all duration-300"
            >
              💬 Start Chat
            </motion.button>
          </Link>
        </motion.div>

        {/* Key Features Section */}
        <motion.div variants={itemVariants}>
          <h2 className="text-3xl font-bold text-white mb-8">
            A New Way to Understand Your Health
          </h2>
          <motion.div
            className="grid grid-cols-1 md:grid-cols-3 gap-8"
            variants={containerVariants}
          >
            {/* Feature 1: Glassmorphism Card */}
            <motion.div
              className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-2xl shadow-lg hover:border-blue-400 transition-all duration-300"
              variants={itemVariants}
            >
              <FiFileText className="text-4xl text-blue-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white">
                Instant Summaries
              </h3>
              <p className="text-gray-300 text-sm mt-2">
                Our AI instantly reads and summarizes your complex medical PDFs.
              </p>
            </motion.div>

            {/* Feature 2: Glassmorphism Card */}
            <motion.div
              className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-2xl shadow-lg hover:border-purple-400 transition-all duration-300"
              variants={itemVariants}
            >
              <FiMessageSquare className="text-4xl text-purple-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white">
                Intelligent Chat
              </h3>
              <p className="text-gray-300 text-sm mt-2">
                Ask questions about your reports in plain language and get clear answers.
              </p>
            </motion.div>

            {/* Feature 3: Glassmorphism Card */}
            <motion.div
              className="bg-white/10 backdrop-blur-md border border-white/20 p-6 rounded-2xl shadow-lg hover:border-pink-400 transition-all duration-300"
              variants={itemVariants}
            >
              <FiShield className="text-4xl text-pink-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-white">
                Secure & Private
              </h3>
              <p className="text-gray-300 text-sm mt-2">
                Your data is encrypted and confidential. Your privacy is our priority.
              </p>
            </motion.div>
          </motion.div>
        </motion.div>
      </motion.div>
    </div>
  );
};

export default HomePage;
