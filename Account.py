import { useState, useEffect } from "react";
import { useTheme } from "./ThemeContext";
import { getSession, clearSession, getUserData, saveUserData, T } from "./storage"; // adjust imports
import LangMenu from "./LangMenu"; // your existing component
import ThemeToggle from "./ThemeToggle"; // your existing component

export default function Account({ onLogout }) {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === "dark";
  const session = getSession();
  const email = session?.email;
  const [data, setData] = useState(null);
  const [lang, setLang] = useState("en");
  const [newGoal, setNewGoal] = useState("");
  const [message, setMessage] = useState("");
  const t = T[lang];

  useEffect(() => {
    if (email) {
      const userData = getUserData(email);
      if (userData) {
        setData(userData);
        setNewGoal(userData.goal.toString());
      }
    }
  }, [email]);

  const updateGoal = () => {
    const goalNum = parseInt(newGoal, 10);
    if (isNaN(goalNum) || goalNum <= 0) return;
    const updated = { ...data, goal: goalNum };
    setData(updated);
    saveUserData(email, updated);
    setMessage(t.goalSaved);
    setTimeout(() => setMessage(""), 2000);
  };

  const handleLogout = () => {
    if (window.confirm(t.logoutConfirm)) {
      clearSession();
      window.location.reload(); // or call onLogout from parent
    }
  };

  if (!data) return <div style={{ padding: 24 }}>Loading...</div>;

  return (
    <div style={{ padding: "80px 20px 80px 20px", maxWidth: 600, margin: "0 auto" }}>
      <h2 style={{ marginBottom: 24 }}>{t.nav[3]}</h2>

      {/* User Info */}
      <div style={{ background: "var(--bg-card)", borderRadius: 24, padding: 20, marginBottom: 20 }}>
        <p><strong>{t.fullName}</strong> {session?.name}</p>
        <p><strong>{t.email}</strong> {email}</p>
      </div>

      {/* Monthly Goal */}
      <div style={{ background: "var(--bg-card)", borderRadius: 24, padding: 20, marginBottom: 20 }}>
        <label style={{ display: "block", marginBottom: 8 }}>{t.goalLabel}</label>
        <div style={{ display: "flex", gap: 12 }}>
          <input className="ifield" type="number" value={newGoal} onChange={(e) => setNewGoal(e.target.value)} />
          <button className="pbtn" onClick={updateGoal} style={{ width: "auto", padding: "0 20px" }}>{t.setGoal}</button>
        </div>
        {message && <p style={{ marginTop: 8, fontSize: 12, color: "#2e7d52" }}>{message}</p>}
      </div>

      {/* Preferences */}
      <div style={{ background: "var(--bg-card)", borderRadius: 24, padding: 20, marginBottom: 20 }}>
        <h3 style={{ marginBottom: 12 }}>Preferences</h3>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 12 }}>
          <span>{t.linkedBank || "Theme"}</span>
          <ThemeToggle />
        </div>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <span>{t.mobileMoney || "Language"}</span>
          <LangMenu current={lang} onChange={setLang} light={!isDark} />
        </div>
      </div>

      {/* Logout */}
      <button className="pbtn" onClick={handleLogout} style={{ background: "#e53e3e", marginTop: 20 }}>
        {t.logout}
      </button>
    </div>
  );
}
