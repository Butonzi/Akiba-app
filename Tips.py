import { useState, useEffect } from "react";
import { useTheme } from "./ThemeContext";
import { T } from "./translations";

export default function Tips() {
  const [lang, setLang] = useState("en");
  const t = T[lang];
  const { theme } = useTheme();
  const [tipIndex, setTipIndex] = useState(0);

  // Rotate daily wisdom every 24h (or just a random tip)
  useEffect(() => {
    const interval = setInterval(() => {
      setTipIndex((prev) => (prev + 1) % t.tips.length);
    }, 1000 * 60 * 60 * 24); // daily
    return () => clearInterval(interval);
  }, [t.tips.length]);

  return (
    <div style={{ padding: "80px 20px 80px 20px", maxWidth: 600, margin: "0 auto" }}>
      <h2 style={{ marginBottom: 8 }}>{t.tipsTitle}</h2>
      <p style={{ color: "var(--text-secondary)", marginBottom: 24 }}>{t.dailyWisdom}</p>

      {/* Daily Proverb */}
      <div style={{ background: "var(--bg-card)", borderRadius: 24, padding: 20, marginBottom: 32 }}>
        <p style={{ fontStyle: "italic", fontSize: 18 }}>{t.proverb}</p>
        <p style={{ marginTop: 8, color: "var(--text-secondary)" }}>{t.proverbSrc}</p>
      </div>

      {/* Tips List */}
      <div style={{ display: "flex", flexDirection: "column", gap: 20 }}>
        {t.tips.map((tip, idx) => (
          <div key={idx} style={{ background: "var(--bg-card)", borderRadius: 20, padding: 16, display: "flex", gap: 16, alignItems: "flex-start" }}>
            <div style={{ fontSize: 32 }}>{tip.icon}</div>
            <div>
              <h4 style={{ marginBottom: 6 }}>{tip.title}</h4>
              <p style={{ color: "var(--text-secondary)", fontSize: 14 }}>{tip.body}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
