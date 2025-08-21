import React, { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
// Switched to a more modern icon set for consistency
import { FiUser, FiMail, FiSave, FiKey, FiEye, FiEyeOff, FiLogOut } from "react-icons/fi"; // Corrected FiEyeSlash to FiEyeOff
import Modal from "./Modal"; // Using the enhanced Modal component
import { motion } from "framer-motion";

const url = import.meta.env.VITE_SERVER_URI || "http://localhost:3000";

// A more fitting loader for the dark theme
const Loader = () => (
    <div className="flex justify-center items-center h-full">
        <div className="w-12 h-12 border-4 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
    </div>
);

function Profile() {
    // --- ALL YOUR ORIGINAL LOGIC IS PRESERVED BELOW ---
    const [user, setUser] = useState({ name: "", email: "" });
    const [loading, setLoading] = useState(true); // Set initial loading to true
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
                `${url}/user/update-profile`, // Corrected the URL
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

    const handleLogout = () => {
        localStorage.removeItem("token");
        toast.info("You have been logged out.");
        navigate("/login");
    };

    const [showPassword, setShowPassword] = useState({
        prevPassword: false,
        newPassword: false,
        confirmNewPassword: false,
    });
    // --- END OF YOUR ORIGINAL LOGIC ---

    return (
        <div className="relative min-h-screen flex items-center justify-center bg-slate-900 p-4 overflow-hidden">
            {/* Animated background shapes */}
            <div className="absolute top-0 -left-4 w-72 h-72 bg-blue-500 rounded-full mix-blend-lighten filter blur-xl opacity-70 animate-blob"></div>
            <div className="absolute top-0 -right-4 w-72 h-72 bg-purple-500 rounded-full mix-blend-lighten filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
            <div className="absolute -bottom-8 left-20 w-72 h-72 bg-pink-500 rounded-full mix-blend-lighten filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>

            <motion.div
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, ease: "easeInOut" }}
                className="relative w-full max-w-md p-8 bg-white/10 backdrop-blur-md border border-white/20 shadow-2xl rounded-3xl z-10"
            >
                {loading ? (
                    <div className="h-96"><Loader /></div>
                ) : (
                    <>
                        <div className="flex flex-col items-center mb-6">
                            <img
                                src={`https://ui-avatars.com/api/?name=${user.name}&background=2563eb&color=fff&size=96`}
                                alt="Profile Avatar"
                                className="w-24 h-24 rounded-full shadow-lg border-4 border-white/20"
                            />
                            <h2 className="text-2xl font-bold text-white mt-4">{user.name}</h2>
                            <p className="text-sm text-gray-400">{user.email}</p>
                        </div>

                        <div className="space-y-6">
                            {/* Floating Label Input for Name */}
                            <div className="relative">
                                <input
                                    type="text"
                                    id="name"
                                    value={user.name}
                                    onChange={(e) => setUser({ ...user, name: e.target.value })}
                                    className="block w-full px-4 py-3 text-white bg-white/5 border-2 border-white/20 rounded-md appearance-none peer focus:outline-none focus:ring-0 focus:border-blue-400 transition"
                                    placeholder=" "
                                />
                                <label htmlFor="name" className="absolute text-sm text-gray-300 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-slate-900/50 px-2 peer-focus:px-2 peer-focus:text-blue-400 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-3">
                                    <FiUser className="inline-block mr-2" /> Full Name
                                </label>
                            </div>

                            {/* Floating Label Input for Email */}
                            <div className="relative">
                                <input
                                    type="email"
                                    id="email"
                                    value={user.email}
                                    onChange={(e) => setUser({ ...user, email: e.target.value })}
                                    className="block w-full px-4 py-3 text-white bg-white/5 border-2 border-white/20 rounded-md appearance-none peer focus:outline-none focus:ring-0 focus:border-blue-400 transition"
                                    placeholder=" "
                                />
                                <label htmlFor="email" className="absolute text-sm text-gray-300 duration-300 transform -translate-y-4 scale-75 top-2 z-10 origin-[0] bg-slate-900/50 px-2 peer-focus:px-2 peer-focus:text-blue-400 peer-placeholder-shown:scale-100 peer-placeholder-shown:-translate-y-1/2 peer-placeholder-shown:top-1/2 peer-focus:top-2 peer-focus:scale-75 peer-focus:-translate-y-4 left-3">
                                    <FiMail className="inline-block mr-2" /> Email Address
                                </label>
                            </div>
                        </div>

                        <div className="flex flex-col gap-4 mt-8">
                            <motion.button 
                                whileHover={{ scale: 1.02, boxShadow: '0px 0px 20px rgba(59, 130, 246, 0.5)' }} 
                                whileTap={{ scale: 0.98 }} 
                                onClick={handleUpdateProfile} 
                                className="flex items-center justify-center gap-2 w-full py-3 px-4 bg-blue-600 text-white font-semibold rounded-lg shadow-md hover:bg-blue-700 transition-all">
                                <FiSave /> Update Profile
                            </motion.button>
                            <motion.button 
                                whileHover={{ scale: 1.02, boxShadow: '0px 0px 15px rgba(200, 200, 200, 0.2)' }} 
                                whileTap={{ scale: 0.98 }} 
                                onClick={() => setIsModalOpen(true)} 
                                className="flex items-center justify-center gap-2 w-full py-3 px-4 bg-gray-600 text-white font-semibold rounded-lg shadow-md hover:bg-gray-700 transition-all">
                                <FiKey /> Change Password
                            </motion.button>
                        </div>
                        <div className="text-center mt-6">
                            <button onClick={handleLogout} className="text-red-400 hover:text-red-300 text-sm font-medium flex items-center justify-center gap-2 mx-auto">
                                <FiLogOut /> Log Out
                            </button>
                        </div>
                    </>
                )}
            </motion.div>

            {/* Modal for updating password */}
            <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Change Password">
                <div className="space-y-4">
                    {["prevPassword", "newPassword", "confirmNewPassword"].map((field) => (
                        <div key={field} className="relative">
                            <input
                                type={showPassword[field] ? "text" : "password"}
                                value={passwords[field]}
                                onChange={(e) => setPasswords({ ...passwords, [field]: e.target.value })}
                                className="w-full p-3 pl-4 pr-10 bg-slate-700 border border-slate-600 text-white rounded-md focus:ring-blue-500 focus:border-blue-500"
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
                                className="absolute right-3 top-3 text-gray-400 hover:text-white cursor-pointer"
                                onClick={() => setShowPassword({ ...showPassword, [field]: !showPassword[field] })}
                            >
                                {showPassword[field] ? <FiEyeOff /> : <FiEye />} 
                            </button>
                        </div>
                    ))}
                </div>
                <div className="flex justify-end gap-3 mt-6">
                    <motion.button 
                        whileHover={{ scale: 1.05 }} 
                        whileTap={{ scale: 0.95 }} 
                        onClick={() => setIsModalOpen(false)} 
                        className="px-4 py-2 bg-slate-600 text-white rounded-md hover:bg-slate-500 transition-colors">
                        Cancel
                    </motion.button>
                    <motion.button 
                        whileHover={{ scale: 1.05 }} 
                        whileTap={{ scale: 0.95 }} 
                        onClick={handleUpdatePassword} 
                        className="px-6 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 transition-colors">
                        Save Changes
                    </motion.button>
                </div>
            </Modal>
        </div>
    );
}

export default Profile;
