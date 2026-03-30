// App.js (or wherever your main component is)
import { useState, useEffect } from "react";
import { ThemeProvider, useTheme } from "./ThemeContext"; // adjust path
import Splash from "./Splash";
import AuthScreen from "./AuthScreen";
import Dashboard from "./Dashboard";
import Scan from "./Scan";
import Tips from "./Tips";
import Account from "./Account";

function AuthenticatedApp() {
  const [activeTab, setActiveTab] = useState(0);
  const { theme } = useTheme();
  const isDark = theme === "dark";

  const tabs = [
    { name: "Home", component: Dashboard },
    { name: "Scan", component: Scan },
    { name: "Tips", component: Tips },
    { name: "Account", component: Account },
  ];
  const CurrentComponent = tabs[activeTab].component;

  return (
    <div style={{ minHeight: "100vh", background: "var(--bg-page)", color: "var(--text-primary)" }}>
      <CurrentComponent />
      <div style={{
        position: "fixed",
        bottom: 0,
        left: 0,
        right: 0,
        display: "flex",
        background: "var(--bg-card)",
        borderTop: `1px solid var(--border)`,
        padding: "8px 16px",
        justifyContent: "space-around",
        zIndex: 10,
      }}>
        {tabs.map((tab, idx) => (
          <button
            key={idx}
            onClick={() => setActiveTab(idx)}
            style={{
              background: "transparent",
              border: "none",
              padding: "8px 16px",
              borderRadius: 20,
              fontSize: 14,
              fontWeight: activeTab === idx ? 600 : 400,
              color: activeTab === idx ? "#2e7d52" : "var(--text-secondary)",
              cursor: "pointer",
            }}
          >
            {tab.name}
          </button>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [auth, setAuth] = useState(null);
  const [showSplash, setShowSplash] = useState(true);

  useEffect(() => {
    const session = getSession(); // from storage.js
    if (session) {
      const data = getUserData(session.email) || mkData();
      setAuth({ ...session, data });
      setShowSplash(false);
    } else {
      setTimeout(() => setShowSplash(false), 2400);
    }
  }, []);

  const handleAuth = (user, userData) => {
    setAuth({ ...user, data: userData });
  };

  if (showSplash) return <Splash onDone={() => setShowSplash(false)} />;
  if (!auth) return <AuthScreen onAuth={handleAuth} />;

  return (
    <ThemeProvider>
      <AuthenticatedApp />
    </ThemeProvider>
  );
}
