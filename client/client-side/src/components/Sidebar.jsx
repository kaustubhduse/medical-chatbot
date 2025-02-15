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
import { Link, useNavigate } from "react-router-dom";

const Sidebar = ({ isOpen, setIsOpen }) => {
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  return (
    <div
      className={`bg-gray-900 h-screen text-white transition-all duration-300 fixed flex flex-col ${
        isOpen ? "lg:w-64 w-fit"  : "w-16"
      }`}
    >
      {/* Toggle Button */}
      <div className="flex justify-end p-4">
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="text-white p-2 rounded-full hover:bg-gray-700 transition cursor-pointer"
        >
          {isOpen ? <X size={24} /> : <Menu size={24} />}
        </button>
      </div>

      {/* Sidebar Links */}
      <ul className="space-y-4 px-4 flex-1">
        <li>
          <Link
            to="/"
            className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-700 transition cursor-pointer text-lg"
          >
            <HomeIcon size={20} />
            {isOpen && <span className="text-xl">Home</span>}
          </Link>
        </li>
        <li>
          <Link
            to="/profile"
            className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-700 transition cursor-pointer text-lg"
          >
            <User size={20} />
            {isOpen && <span className="text-xl">Profile</span>}
          </Link>
        </li>
        <li>
          <Link
            to="/medical-chatbot/summary"
            className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-700 transition cursor-pointer text-lg"
          >
            <FileText size={20} />
            {isOpen && <span className="text-xl">Summary</span>}
          </Link>
        </li>
        <li>
          <Link
            to="/medical-chatbot"
            className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-700 transition cursor-pointer text-lg"
          >
            <MessageSquare size={20} />
            {isOpen && <span className="text-xl">Medical Chatbot</span>}
          </Link>
        </li>
        <li>
          <Link
            to="/search"
            className="flex items-center gap-3 p-2 rounded-lg hover:bg-gray-700 transition cursor-pointer text-lg"
          >
            <SearchIcon size={20} />
            {isOpen && <span className="text-xl">Search</span>}
          </Link>
        </li>
      </ul>

      {/* Logout Button */}
      <div className="p-4">
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 p-2 rounded-lg bg-red-600 hover:bg-red-700 transition cursor-pointer text-lg"
        >
          <LogOut size={20} />
          {isOpen && <span className="text-xl">Log Out</span>}
        </button>
      </div>
    </div>
  );
};

export default Sidebar;
