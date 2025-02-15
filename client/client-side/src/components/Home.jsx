import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-blue-50 p-6">
      {/* Introduction Section */}
      <div className="text-center max-w-2xl animate-fadeIn">
        <h1 className="text-4xl font-bold text-blue-600 mb-4">
          Chat with Your Medical Reports ⚕️
        </h1>
        <p className="text-lg text-gray-700 mb-6">
          Upload your medical reports and get an AI-powered summary & chatbot support 
          for better understanding of your health.
        </p>

        {/* Action Buttons */}
        <div className="flex flex-wrap justify-center gap-4">
          <Link to="/medical-chatbot">
            <button className="px-6 py-3 bg-blue-600 text-white font-medium rounded-lg shadow-md hover:bg-blue-700 transition cursor-pointer">
              📄 Upload Report
            </button>
          </Link>
          <Link to="/medical-chatbot">
            <button className="px-6 py-3 bg-green-600 text-white font-medium rounded-lg shadow-md hover:bg-green-700 transition cursor-pointer">
              💬 Start Chat
            </button>
          </Link>
        </div>
      </div>

      {/* Key Features Section */}
      <div className="mt-12 max-w-3xl text-center">
        <h2 className="text-2xl font-semibold text-gray-800 mb-4">Why Use this Medical Chatbot?</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          {/* Feature 1 */}
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="text-xl font-medium text-blue-700">📑 PDF Summarization</h3>
            <p className="text-gray-600 text-sm mt-2">
              Get an AI-powered summary of your medical reports instantly.
            </p>
          </div>

          {/* Feature 2 */}
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="text-xl font-medium text-green-700">🤖 AI Chat Support</h3>
            <p className="text-gray-600 text-sm mt-2">
              Ask health-related questions and get AI-driven responses.
            </p>
          </div>

          {/* Feature 3 */}
          <div className="bg-white p-4 rounded-lg shadow-md">
            <h3 className="text-xl font-medium text-purple-700">🔒 Secure & Private</h3>
            <p className="text-gray-600 text-sm mt-2">
              Your medical data remains safe and confidential.
            </p>
          </div>
        </div>
      </div>

      
    </div>
  );
};

export default HomePage;
