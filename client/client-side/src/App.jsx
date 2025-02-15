import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import Profile from './components/Profile';
import Registration from './components/Registration';
import { ToastContainer } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Sidebar from './components/Sidebar';
import Summary from './components/Summary';
import { useState, useEffect, useRef } from 'react';
import Search from './components/Search';
import ProtectedRoute from './components/Auth/ProtectedRoute';

function AppContent() {
  const location = useLocation();
  const hideSidebar = location.pathname === '/login' || location.pathname === '/register';

  const [isSidebarOpen, setIsSidebarOpen] = useState(true);

  // Persist iframe by keeping it mounted
  const iframeRef = useRef(null);
  const [showChatbot, setShowChatbot] = useState(false);

  useEffect(() => {
    setShowChatbot(location.pathname === '/medical-chatbot');
  }, [location.pathname]);

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
          </Route>
        </Routes>

        {/* Persist the Medical Chatbot iframe */}
        <div className={`w-full h-full ${showChatbot ? 'block' : 'hidden'}`}>
          <iframe
            ref={iframeRef}
            src="http://localhost:8501/"
            className="w-full h-screen border-none"
            title="Medical Chatbot"
          />
        </div>
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
