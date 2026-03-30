import { useState, useEffect } from "react";
import { useTheme } from "./ThemeContext";
import { getUserData, saveUserData, fmt, uid, getSession } from "./storage"; // adjust path
import { T } from "./translations"; // adjust path

export default function Dashboard() {
  const { theme } = useTheme();
  const isDark = theme === "dark";
  const session = getSession();
  const email = session?.email;
  const [data, setData] = useState(null);
  const [showAddTx, setShowAddTx] = useState(false);
  const [newTx, setNewTx] = useState({ label: "", amount: "", type: "expense" });
  const [lang, setLang] = useState("en"); // you can get this from user data
  const t = T[lang];

  useEffect(() => {
    if (email) {
      const userData = getUserData(email);
      if (userData) setData(userData);
    }
  }, [email]);

  const updateData = (newData) => {
    setData(newData);
    saveUserData(email, newData);
  };

  const totalSavings = data?.transactions.reduce((sum, tx) => {
    return tx.type === "income" ? sum + tx.amount : sum - tx.amount;
  }, 0) || 0;

  const progress = data ? (totalSavings / data.goal) * 100 : 0;
  const progressPercent = Math.min(100, Math.max(0, progress));

  const addTransaction = () => {
    if (!newTx.label || !newTx.amount) return;
    const amountNum = parseFloat(newTx.amount);
    if (isNaN(amountNum)) return;
    const transaction = {
      id: uid(),
      label: newTx.label,
      amount: amountNum,
      type: newTx.type,
      date: new Date().toISOString().slice(0, 10),
    };
    const updated = { ...data, transactions: [transaction, ...data.transactions] };
    updateData(updated);
    setNewTx({ label: "", amount: "", type: "expense" });
    setShowAddTx(false);
  };

  if (!data) return <div style={{ padding: 24 }}>Loading...</div>;

  return (
    <div style={{ padding: "80px 20px 80px 20px", maxWidth: 600, margin: "0 auto" }}>
      {/* Greeting */}
      <h2 style={{ fontSize: 24, marginBottom: 8 }}>{t.greeting} {session?.name.split(" ")[0]} 👋</h2>
      <p style={{ color: "var(--text-secondary)", marginBottom: 24 }}>{t.appName}</p>

      {/* Total Savings Card */}
      <div style={{ background: "var(--bg-card)", borderRadius: 24, padding: 20, marginBottom: 20, boxShadow: "var(--shadow-sm)" }}>
        <p style={{ fontSize: 14, color: "var(--text-secondary)" }}>{t.totalSavings}</p>
        <p style={{ fontSize: 36, fontWeight: 700 }}>UGX {fmt(totalSavings)}</p>
        <div style={{ marginTop: 16 }}>
          <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 6 }}>
            <span>{t.monthlyGoal}</span>
            <span>UGX {fmt(data.goal)}</span>
          </div>
          <div style={{ height: 8, background: "var(--border)", borderRadius: 4, overflow: "hidden" }}>
            <div style={{ width: `${progressPercent}%`, height: "100%", background: "#2e7d52", borderRadius: 4 }} />
          </div>
          <p style={{ fontSize: 12, marginTop: 6, color: "var(--text-secondary)" }}>{t.progress}: {progressPercent.toFixed(0)}%</p>
        </div>
      </div>

      {/* Quick Actions */}
      <div style={{ display: "flex", gap: 12, marginBottom: 32 }}>
        <button className="pbtn" onClick={() => setShowAddTx(true)} style={{ flex: 1 }}>{t.quickSave}</button>
        {/* Other action buttons can be added here */}
      </div>

      {/* Recent Transactions */}
      <div>
        <h3 style={{ marginBottom: 16 }}>{t.recentTx}</h3>
        {data.transactions.length === 0 ? (
          <p style={{ color: "var(--text-secondary)" }}>{t.noTx}</p>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 12 }}>
            {data.transactions.slice(0, 5).map((tx) => (
              <div key={tx.id} style={{ display: "flex", justifyContent: "space-between", background: "var(--bg-card)", padding: 12, borderRadius: 16 }}>
                <div>
                  <p style={{ fontWeight: 500 }}>{tx.label}</p>
                  <p style={{ fontSize: 12, color: "var(--text-secondary)" }}>{tx.date}</p>
                </div>
                <p style={{ color: tx.type === "income" ? "#2e7d52" : "#e53e3e" }}>
                  {tx.type === "income" ? "+" : "-"} UGX {fmt(tx.amount)}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Add Transaction Modal */}
      {showAddTx && (
        <div style={{ position: "fixed", top: 0, left: 0, right: 0, bottom: 0, background: "rgba(0,0,0,0.5)", display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000 }}>
          <div style={{ background: "var(--bg-card)", borderRadius: 24, padding: 24, width: "90%", maxWidth: 400 }}>
            <h3 style={{ marginBottom: 16 }}>{t.addTx}</h3>
            <input className="ifield" placeholder={t.txDesc} value={newTx.label} onChange={(e) => setNewTx({ ...newTx, label: e.target.value })} style={{ marginBottom: 12 }} />
            <input className="ifield" placeholder={t.txAmt} type="number" value={newTx.amount} onChange={(e) => setNewTx({ ...newTx, amount: e.target.value })} style={{ marginBottom: 12 }} />
            <div style={{ display: "flex", gap: 12, marginBottom: 20 }}>
              <button onClick={() => setNewTx({ ...newTx, type: "income" })} style={{ flex: 1, padding: 10, borderRadius: 12, background: newTx.type === "income" ? "#2e7d52" : "var(--border)", color: newTx.type === "income" ? "#fff" : "var(--text-secondary)", border: "none" }}>{t.income}</button>
              <button onClick={() => setNewTx({ ...newTx, type: "expense" })} style={{ flex: 1, padding: 10, borderRadius: 12, background: newTx.type === "expense" ? "#e53e3e" : "var(--border)", color: newTx.type === "expense" ? "#fff" : "var(--text-secondary)", border: "none" }}>{t.expense}</button>
            </div>
            <div style={{ display: "flex", gap: 12 }}>
              <button className="pbtn" onClick={addTransaction}>{t.add}</button>
              <button className="pbtn" onClick={() => setShowAddTx(false)} style={{ background: "var(--border)", color: "var(--text-primary)" }}>{t.cancel}</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
