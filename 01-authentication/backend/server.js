import express from "express";
import mongoose from "mongoose";
import cors from "cors";
import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import dotenv from "dotenv";
import User from "./models/User.js";

dotenv.config();
const app = express();
app.use(cors({ origin: "http://localhost:5173" }));
app.use(express.json());
app.get("/", (_req, res) => res.json({ message: "Authentication API is running" }));

app.post("/api/auth/register", async (req, res) => {
  try {
    const { name, email, password } = req.body;
    if (!name || !email || !password) return res.status(400).json({ message: "All fields are required." });
    if (password.length < 8) return res.status(400).json({ message: "Password must be at least 8 characters." });
    const normalized = email.toLowerCase().trim();
    if (await User.findOne({ email: normalized })) return res.status(409).json({ message: "Email already registered." });
    await User.create({ name: name.trim(), email: normalized, password: await bcrypt.hash(password, 12) });
    res.status(201).json({ message: "Registration successful. You can now log in." });
  } catch (error) {
    res.status(500).json({ message: "Registration failed.", error: error.message });
  }
});

app.post("/api/auth/login", async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email: (email || "").toLowerCase().trim() });
    if (!user || !(await bcrypt.compare(password || "", user.password))) {
      return res.status(401).json({ message: "Invalid email or password." });
    }
    const token = jwt.sign({ userId: user._id }, process.env.JWT_SECRET, { expiresIn: "1d" });
    res.json({ message: "Login successful.", token, user: { id: user._id, name: user.name, email: user.email } });
  } catch (error) {
    res.status(500).json({ message: "Login failed.", error: error.message });
  }
});

const PORT = process.env.PORT || 5000;
if (!process.env.MONGO_URI || !process.env.JWT_SECRET) {
  console.error("Configure MONGO_URI and JWT_SECRET in .env");
  process.exit(1);
}
mongoose.connect(process.env.MONGO_URI)
  .then(() => app.listen(PORT, () => console.log(`API running at http://localhost:${PORT}`)))
  .catch(error => { console.error(error.message); process.exit(1); });
