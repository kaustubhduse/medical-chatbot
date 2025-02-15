import { BrowserRouter as Router, Routes, Route, useLocation, useNavigate } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Profile from './components/Profile';
import Registration from './components/Registration';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Sidebar from './components/Sidebar';
import Summary from './components/Summary';
import { useState, useEffect } from 'react';
import Search from './components/Search';
import ProtectedRoute from './components/Auth/ProtectedRoute';

function RedirectToChatbot() {
  const navigate = useNavigate();

  useEffect(() => {
    // Open the chatbot in a new tab
    window.open('https://chatbot-zcfm8sfepngeqjvufqeq2w.streamlit.app/', '_blank');

    // Redirect back to home after opening chatbot
    navigate('/');
  }, [navigate]);

  return null; // Prevent rendering anything on this route
}

function AppContent() {
  const location = useLocation();
  const hideSidebar = location.pathname === '/login' || location.pathname === '/register';

  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  return (
    <div className="flex h-screen">
      {!hideSidebar && (
        <Sidebar isOpen={isSidebarOpen} setIsOpen={setIsSidebarOpen} />
      )}

      <div
        className={`flex-1 transition-all ${
          hideSidebar ? 'w-full' : isSidebarOpen ? 'ml-64' : 'ml-16'
        }`}
      >
        <Routes>
          {/* Public Routes */}
          <Route path="/register" element={<Registration />} />
          <Route path="/login" element={<Login />} />

          {/* Protected Routes */}
          <Route element={<ProtectedRoute />}>
            <Route path="/" element={<Home />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/search" element={<Search />} />
            <Route path="/medical-chatbot/summary" element={<Summary />} />

            {/* Redirects to Chatbot */}
            <Route path="/medical-chatbot" element={<RedirectToChatbot />} />
          </Route>
        </Routes>
      </div>
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <ToastContainer />
      <AppContent />
    </Router>
  );
}
