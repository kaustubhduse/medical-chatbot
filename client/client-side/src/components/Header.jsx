import React from 'react'
import { Link, useNavigate } from 'react-router-dom'

function Header() {
    const navigate = useNavigate()
    const handleLogout = () => {
        localStorage.removeItem('token')
        navigate('/login')
    }

    return (
        <div className='border border-b border-gray-400 bg-gray-100 h-12 flex items-center space-x-5'>
            <Link to="/" >Home</Link>
            <Link to="/login" >Login</Link>
            <Link to="/profile" >Profile</Link>
            <Link to="/register" >Register</Link>
            <button onClick={handleLogout} >Log Out</button>

        </div>
    )
}

export default Header