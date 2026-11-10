import { useState } from "react";
const API = "http://localhost:5000/api/auth";

export default function App() {
  const [mode, setMode] = useState("login");
  const [form, setForm] = useState({ name: "", email: "", password: "" });
  const [msg, setMsg] = useState("");
  const [bad, setBad] = useState(false);
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem("authUser") || "null"));
  const update = event => setForm({ ...form, [event.target.name]: event.target.value });

  async function submit(event) {
    event.preventDefault(); setMsg(""); setBad(false);
    try {
      const response = await fetch(`${API}/${mode === "register" ? "register" : "login"}`, {
        method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(form)
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.message || "Request failed");
      if (mode === "register") {
        setMsg(data.message); setMode("login"); setForm({ ...form, password: "" });
      } else {
        localStorage.setItem("authToken", data.token);
        localStorage.setItem("authUser", JSON.stringify(data.user));
        setUser(data.user);
      }
    } catch (error) { setBad(true); setMsg(error.message); }
  }

  function logout() {
    localStorage.removeItem("authToken"); localStorage.removeItem("authUser");
    setUser(null); setMsg("Logged out successfully.");
  }

  if (user) return <main><section className="card">
    <h1>Welcome, {user.name}!</h1><p>You are logged in as {user.email}</p>
    <button onClick={logout}>Log out</button>
  </section></main>;

  return <main><section className="card">
    <div className="logo">A</div><small>ACCOUNT PORTAL</small>
    <h1>{mode === "login" ? "Welcome back" : "Create account"}</h1>
    <p className="muted">{mode === "login" ? "Sign in to continue." : "Register to get started."}</p>
    <nav>
      <button className={mode === "login" ? "selected" : ""} onClick={() => { setMode("login"); setMsg(""); }}>Login</button>
      <button className={mode === "register" ? "selected" : ""} onClick={() => { setMode("register"); setMsg(""); }}>Register</button>
    </nav>
    <form onSubmit={submit}>
      {mode === "register" && <label>Full name<input name="name" value={form.name} onChange={update} required /></label>}
      <label>Email<input name="email" type="email" value={form.email} onChange={update} required /></label>
      <label>Password<input name="password" type="password" minLength="8" value={form.password} onChange={update} required /></label>
      <button className="primary">{mode === "login" ? "Sign in" : "Create account"}</button>
    </form>
    {msg && <p className={bad ? "error" : "success"}>{msg}</p>}
    <footer>Passwords are securely hashed before storage.</footer>
  </section></main>;
}
