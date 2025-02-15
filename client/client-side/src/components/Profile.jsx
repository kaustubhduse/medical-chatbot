import React, { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import {
  FaUser,
  FaEnvelope,
  FaLock,
  FaSignOutAlt,
  FaSave,
  FaKey,
  FaEye,
  FaEyeSlash,
} from "react-icons/fa";
import Modal from "./Modal"; // Import the Modal component
const url = import.meta.env.VITE_SERVER_URI;
function Profile() {
  const [user, setUser] = useState({ name: "", email: "" });
  const [loading, setLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [passwords, setPasswords] = useState({
    prevPassword: "",
    newPassword: "",
    confirmNewPassword: "",
  });
  const navigate = useNavigate();

  useEffect(() => {
    const fetchProfile = async () => {
      setLoading(true);
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          toast.error("Unauthorized access. Please log in.");
          navigate("/login");
          return;
        }

        const response = await axios.get(`${url}/user/get-profile`, {
          headers: { Authorization: `Bearer ${token}` },
        });
        setUser(response.data);
      } catch (error) {
        toast.error("Failed to load profile. Please try again.");
        if (error.response?.status === 401) {
          navigate("/login");
        }
      } finally {
        setLoading(false);
      }
    };
    fetchProfile();
  }, [navigate]);

  const handleUpdateProfile = async () => {
    try {
      const token = localStorage.getItem("token");
      if (!token) {
        toast.error("Unauthorized access. Please log in.");
        return;
      }

      const updatedData = { name: user.name, email: user.email };

      const response = await axios.put(
        `${url}user/update-profile`,
        updatedData,
        {
          headers: { Authorization: `Bearer ${token}` },
        }
      );

      toast.success(response.data.message || "Profile updated successfully!");
    } catch (error) {
      toast.error("Failed to update profile. Please try again.");
    }
  };

  const handleUpdatePassword = async () => {
    if (passwords.newPassword !== passwords.confirmNewPassword) {
      toast.error("New passwords do not match!");
      return;
    }

    try {
      const token = localStorage.getItem("token");
      if (!token) {
        toast.error("Unauthorized access. Please log in.");
        return;
      }

      const response = await axios.put(
        `${url}/user/update-password`,
        {
          prevPassword: passwords.prevPassword,
          newPassword: passwords.newPassword,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      toast.success(response.data.message || "Password updated successfully!");
      setPasswords({
        prevPassword: "",
        newPassword: "",
        confirmNewPassword: "",
      });
      setIsModalOpen(false); // Close modal after update
    } catch (error) {
      toast.error(
        error.response?.data?.message ||
          "Failed to update password. Please try again."
      );
    }
  };

  const [showPassword, setShowPassword] = useState({
    prevPassword: false,
    newPassword: false,
    confirmNewPassword: false,
  });

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-blue-100 to-indigo-300">
      <div className="bg-white p-8 rounded-2xl shadow-xl w-full max-w-md">
        {loading ? (
          <div className="flex justify-center items-center h-40">
            <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
          </div>
        ) : (
          <>
            <div className="flex justify-center mb-6">
              <img
                src={`https://ui-avatars.com/api/?name=${user.name}`}
                alt="Profile Avatar"
                className="w-24 h-24 rounded-full shadow-md border-4 border-gray-200"
              />
            </div>
            <div className="space-y-4">
              <div className="relative">
                <FaUser className="absolute left-3 top-3 text-gray-500" />
                <input
                  type="text"
                  value={user.name}
                  onChange={(e) => setUser({ ...user, name: e.target.value })}
                  className="w-full p-3 pl-10 border border-gray-300 rounded-md"
                  placeholder="Enter your name"
                />
              </div>
              <div className="relative">
                <FaEnvelope className="absolute left-3 top-3 text-gray-500" />
                <input
                  type="email"
                  value={user.email}
                  onChange={(e) => setUser({ ...user, email: e.target.value })}
                  className="w-full p-3 pl-10 border border-gray-300 rounded-md"
                  placeholder="Enter your email"
                />
              </div>
            </div>
            <div className="flex flex-col gap-4 mt-6">
              <button
                onClick={handleUpdateProfile}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-md hover:bg-blue-600 cursor-pointer"
              >
                <FaSave /> Update Profile
              </button>
              <button
                onClick={() => setIsModalOpen(true)}
                className="flex items-center justify-center gap-2 px-6 py-3 bg-yellow-500 text-white rounded-md hover:bg-yellow-600 cursor-pointer"
              >
                <FaKey /> Update Password
              </button>
            </div>
          </>
        )}
      </div>
      {/* Modal for updating password */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title="Update Password"
      >
        <div className="space-y-4">
          {["prevPassword", "newPassword", "confirmNewPassword"].map(
            (field, index) => (
              <div key={index} className="relative">
                <input
                  type={showPassword[field] ? "text" : "password"}
                  value={passwords[field]}
                  onChange={(e) =>
                    setPasswords({ ...passwords, [field]: e.target.value })
                  }
                  className="w-full p-3 pl-4 pr-10 border border-gray-300 rounded-md"
                  placeholder={
                    field === "prevPassword"
                      ? "Previous Password"
                      : field === "newPassword"
                      ? "New Password"
                      : "Confirm New Password"
                  }
                />
                <button
                  type="button"
                  className="absolute right-3 top-3 text-gray-500 cursor-pointer"
                  onClick={() =>
                    setShowPassword({
                      ...showPassword,
                      [field]: !showPassword[field],
                    })
                  }
                >
                  {showPassword[field] ? <FaEyeSlash /> : <FaEye />}
                </button>
              </div>
            )
          )}
        </div>
        <div className="flex justify-end gap-3 mt-6">
          <button
            onClick={() => setIsModalOpen(false)}
            className="px-4 py-2 bg-gray-300 rounded-md cursor-pointer"
          >
            Cancel
          </button>
          <button
            onClick={handleUpdatePassword}
            className="px-6 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 cursor-pointer"
          >
            Save Password
          </button>
        </div>
      </Modal>
    </div>
  );
}

export default Profile;
