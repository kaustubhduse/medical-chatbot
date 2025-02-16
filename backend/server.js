const express = require('express')
const mongoose = require('mongoose')
const cors = require('cors')
const cookieParser = require("cookie-parser");
require('dotenv').config();

const userRoute = require('./routes/authRoutes')

const app = express();

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());
app.use(cors({
    origin: process.env.FRONTEND_URL || "http://localhost:5173", // Allow only your frontend URL
    credentials: true,                // Allow cookies if needed
    methods: ["GET", "POST", "PUT", "DELETE"],  // Allowed methods
}));



app.get('/', (req, res) => {
    res.send("Server is running..")
})

app.use('/user', userRoute)

mongoose.connect(process.env.MONGO_URI)
    .then(() => console.log("DB connected successfully"))
    .catch((err) => console.log("Failed to connect database ", err))

app.listen(3000, () => {
    console.log("server is running.. 3000")
})
