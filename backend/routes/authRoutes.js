const express = require('express');
const router = express.Router();
const authMiddleware = require("../middlewares/authMiddleware");
const { registerUser, loginUser, getUserProfile,updateUserProfile, updateUserPassword } = require('../controllers/authController');

// User Routes
router.post('/register', registerUser);
router.post('/login', loginUser);
router.get('/get-profile', authMiddleware, getUserProfile);
router.put("/update-profile", authMiddleware, updateUserProfile); 
router.put("/update-password", authMiddleware, updateUserPassword)

module.exports = router;