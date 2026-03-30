import { useState } from "react";
import { useTheme } from "./ThemeContext";
import { T } from "./translations";

export default function Scan() {
  const [lang, setLang] = useState("en");
  const [file, setFile] = useState(null);
  const [analysing, setAnalysing] = useState(false);
  const [result, setResult] = useState(null);
  const t = T[lang];
  const { theme } = useTheme();

  const handleFileUpload = (e) => {
    const uploaded = e.target.files[0];
    if (!uploaded) return;
    setFile(uploaded);
    setAnalysing(true);
    // Simulate AI processing
    setTimeout(() => {
      setResult({
        summary: "This document shows a bank statement with a total income of UGX 2,500,000 and expenses of UGX 1,800,000. Net savings of UGX 700,000. Great job!",
        keyPoints: ["Income: UGX 2.5M", "Expenses: UGX 1.8M", "Net Savings: UGX 700k"],
      });
      setAnalysing(false);
    }, 2000);
  };

  return (
    <div style={{ padding: "80px 20px 80px 20px", maxWidth: 600, margin: "0 auto" }}>
      <h2 style={{ marginBottom: 8 }}>{t.scanTitle}</h2>
      <p style={{ color: "var(--text-secondary)", marginBottom: 24 }}>{t.scanDesc}</p>

      <div style={{ background: "var(--bg-card)", borderRadius: 24, padding: 32, textAlign: "center", border: `2px dashed var(--border)` }}>
        <input type="file" accept="image/*,application/pdf" onChange={handleFileUpload} style={{ display: "none" }} id="doc-upload" />
        <label htmlFor="doc-upload" className="pbtn" style={{ display: "inline-block", cursor: "pointer" }}>
          {t.scanBtn}
        </label>
        {file && <p style={{ marginTop: 16, fontSize: 14, color: "var(--text-secondary)" }}>{file.name}</p>}
      </div>

      {analysing && (
        <div style={{ marginTop: 32, textAlign: "center" }}>
          <div className="spinner" style={{ width: 40, height: 40, border: "3px solid var(--border)", borderTopColor: "#2e7d52", borderRadius: "50%", animation: "spin 1s linear infinite", margin: "0 auto 16px" }} />
          <p>{t.analysing}</p>
        </div>
      )}

      {result && (
        <div style={{ marginTop: 32, background: "var(--bg-card)", borderRadius: 24, padding: 20 }}>
          <h3>{t.scanResult}</h3>
          <p style={{ margin: "16px 0" }}>{result.summary}</p>
          <ul style={{ paddingLeft: 20 }}>
            {result.keyPoints.map((point, i) => (
              <li key={i}>{point}</li>
            ))}
          </ul>
          <button className="pbtn" onClick={() => { setFile(null); setResult(null); }} style={{ marginTop: 16 }}>
            {t.scanAnother}
          </button>
        </div>
      )}
    </div>
  );
}
