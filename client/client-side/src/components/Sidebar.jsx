import {
    Menu,
    X,
    LogOut,
    Home as HomeIcon,
    User,
    MessageSquare,
    FileText,
    Search as SearchIcon,
} from "lucide-react";
import { NavLink, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { useState, useEffect } from "react";

// A simple hook to check the screen size
const useIsMobile = (breakpoint = 1024) => {
    const [isMobile, setIsMobile] = useState(window.innerWidth < breakpoint);
    useEffect(() => {
        const handleResize = () => setIsMobile(window.innerWidth < breakpoint);
        window.addEventListener("resize", handleResize);
        return () => window.removeEventListener("resize", handleResize);
    }, [breakpoint]);
    return isMobile;
};

const Sidebar = ({ isOpen, setIsOpen }) => {
    const navigate = useNavigate();
    const isMobile = useIsMobile();

    const handleLogout = () => {
        localStorage.removeItem("token");
        navigate("/login");
    };

    const navLinks = [
        { name: "Home", icon: <HomeIcon size={20} />, path: "/" },
        { name: "Profile", icon: <User size={20} />, path: "/profile" },
        { name: "Summary", icon: <FileText size={20} />, path: "/medical-chatbot/summary" },
        { name: "Medical Chatbot", icon: <MessageSquare size={20} />, path: "/medical-chatbot" },
        { name: "Search", icon: <SearchIcon size={20} />, path: "/search" },
    ];

    const sidebarVariants = {
        open: { x: 0 },
        closed: { x: "-100%" }
    };

    const SidebarContent = () => (
        <div className="flex flex-col h-full">
            {/* Header & Toggle Button */}
            <div className={`flex items-center p-4 ${isOpen ? "justify-between" : "lg:justify-center"}`}>
                {isOpen && <span className="text-xl font-bold whitespace-nowrap">Menu</span>}
                <button
                    onClick={() => setIsOpen(!isOpen)}
                    className="text-white p-2 rounded-full hover:bg-white/10 transition"
                >
                    {isOpen ? <X size={24} /> : <Menu size={24} />}
                </button>
            </div>

            {/* Navigation Links */}
            <nav className="flex-1 px-4 space-y-2">
                {navLinks.map((link) => (
                    <NavLink
                        key={link.name}
                        to={link.path}
                        end={link.path === "/"}
                        onClick={() => isMobile && setIsOpen(false)}
                        className={({ isActive }) =>
                            `flex items-center gap-4 p-3 rounded-lg hover:bg-white/10 transition-colors ${isActive ? "bg-blue-500/30 text-white" : "text-gray-300"} ${!isOpen && "lg:justify-center"}`
                        }
                    >
                        {link.icon}
                        <span className={`font-medium whitespace-nowrap ${isOpen ? "inline" : "lg:hidden"}`}>{link.name}</span>
                    </NavLink>
                ))}
            </nav>

            {/* Logout Button */}
            <div className="p-4 border-t border-white/10">
                <button
                    onClick={handleLogout}
                    className={`w-full flex items-center gap-4 p-3 rounded-lg text-red-400 hover:bg-red-500/20 hover:text-red-300 transition-colors ${!isOpen && "lg:justify-center"}`}
                >
                    <LogOut size={20} />
                    <span className={`font-medium whitespace-nowrap ${isOpen ? "inline" : "lg:hidden"}`}>Log Out</span>
                </button>
            </div>
        </div>
    );

    return (
        <>
            {/* --- MOBILE VIEW --- */}
            {isMobile && (
                <>
                    <button onClick={() => setIsOpen(true)} className="fixed top-4 left-4 z-50 p-2 bg-slate-800/50 backdrop-blur-sm rounded-full text-white">
                        <Menu size={24} />
                    </button>
                    <AnimatePresence>
                        {isOpen && (
                            <>
                                <motion.div
                                    initial={{ opacity: 0 }}
                                    animate={{ opacity: 1 }}
                                    exit={{ opacity: 0 }}
                                    onClick={() => setIsOpen(false)}
                                    className="fixed inset-0 bg-black/50 z-30"
                                />
                                <motion.div
                                    variants={sidebarVariants}
                                    initial="closed"
                                    animate="open"
                                    exit="closed"
                                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                                    className="fixed inset-y-0 left-0 bg-slate-900/80 backdrop-blur-md border-r border-white/20 h-screen text-white w-64 z-40"
                                >
                                    <SidebarContent />
                                </motion.div>
                            </>
                        )}
                    </AnimatePresence>
                </>
            )}

            {/* --- DESKTOP VIEW --- */}
            {!isMobile && (
                <div className={`bg-slate-900/50 backdrop-blur-md border-r border-white/20 h-screen text-white transition-width duration-300 ${isOpen ? "w-64" : "w-20"}`}>
                    <SidebarContent />
                </div>
            )}
        </>
    );
};

export default Sidebar;
