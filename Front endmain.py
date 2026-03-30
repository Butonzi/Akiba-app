import { useState, useEffect, useRef, createContext, useContext } from "react";

// ── THEME CONTEXT ────────────────────────────────────────────────────────────
const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  const [theme, setTheme] = useState(() => {
    try {
      return localStorage.getItem("akiba_theme") || "light";
    } catch { return "light"; }
  });

  useEffect(() => {
    localStorage.setItem("akiba_theme", theme);
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  const toggleTheme = () => setTheme(prev => prev === "light" ? "dark" : "light");

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error("useTheme must be used within ThemeProvider");
  return context;
};

// ── THEME-BASED STYLE HELPERS ────────────────────────────────────────────────
const getThemeStyles = (theme) => ({
  // Base backgrounds & text
  pageBg: theme === "light" ? "#fafdf8" : "#0a0f1c",
  cardBg: theme === "light" ? "#ffffff" : "#141a2b",
  textPrimary: theme === "light" ? "#1a2e2a" : "#eef5f0",
  textSecondary: theme === "light" ? "#4a5b55" : "#9baeb8",
  border: theme === "light" ? "#e0ece4" : "#2a3548",
  inputBg: theme === "light" ? "#f9fdf9" : "#1e2538",
  inputBorder: theme === "light" ? "#dde8e0" : "#334155",
  // Gradients & buttons
  primaryGradient: theme === "light"
    ? "linear-gradient(135deg,#1a5c3a,#2e7d52)"
    : "linear-gradient(135deg,#2b4b3a,#1e6b4c)",
  shadow: theme === "light"
    ? "0 4px 20px rgba(46,125,82,0.2)"
    : "0 4px 20px rgba(0,0,0,0.4)",
  // Auth card specific
  authCardBg: theme === "light" ? "rgba(255,255,255,0.96)" : "rgba(20,26,43,0.96)",
  // Splash – keep natural, but can adjust
  splashGradient: theme === "light"
    ? "linear-gradient(160deg,#0a1628 0%,#0e3a28 100%)"
    : "linear-gradient(160deg,#030712 0%,#0a281c 100%)",
});

// ── GLOBAL STYLES (with theme-aware variables) ───────────────────────────────
const globalStyles = `
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700;900&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&display=swap');
  
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body { transition: background-color 0.25s ease, color 0.2s ease; background-color: var(--bg-page); color: var(--text-primary); }
  
  :root {
    --bg-page: #fafdf8;
    --bg-card: #ffffff;
    --text-primary: #1a2e2a;
    --text-secondary: #4a5b55;
    --border: #e0ece4;
    --input-bg: #f9fdf9;
    --input-border: #dde8e0;
    --primary-gradient: linear-gradient(135deg,#1a5c3a,#2e7d52);
    --shadow-sm: 0 4px 20px rgba(46,125,82,0.2);
  }
  
  [data-theme="dark"] {
    --bg-page: #0a0f1c;
    --bg-card: #141a2b;
    --text-primary: #eef5f0;
    --text-secondary: #9baeb8;
    --border: #2a3548;
    --input-bg: #1e2538;
    --input-border: #334155;
    --primary-gradient: linear-gradient(135deg,#2b4b3a,#1e6b4c);
    --shadow-sm: 0 4px 20px rgba(0,0,0,0.4);
  }

  @keyframes spin { to { transform: rotate(360deg); } }
  @keyframes fadeUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes slideIn { from { opacity: 0; transform: translateX(24px); } to { opacity: 1; transform: translateX(0); } }
  @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
  @keyframes float { 0%,100%{transform:translateY(0px)} 50%{transform:translateY(-10px)} }
  
  .ifield {
    width:100%; padding:13px 16px; border-radius:12px;
    border:1.5px solid var(--input-border); background:var(--input-bg);
    font-size:14px; font-family:'DM Sans',sans-serif;
    color:var(--text-primary); outline:none; transition:all 0.2s;
  }
  .ifield:focus { border-color:#2e7d52; background:var(--bg-card); box-shadow:0 0 0 3px rgba(46,125,82,0.1); }
  .ifield::placeholder { color:#9ca3af; }
  
  .pbtn {
    width:100%; padding:14px; border-radius:12px; border:none;
    background:var(--primary-gradient);
    color:#fff; font-weight:700; font-size:15px;
    font-family:'DM Sans',sans-serif; cursor:pointer;
    box-shadow:var(--shadow-sm);
    transition:all 0.2s; letter-spacing:0.3px;
  }
  .pbtn:hover { transform:translateY(-1px); filter:brightness(1.05); }
  .pbtn:active { transform:translateY(0); }
  .pbtn:disabled { background:#bbb; box-shadow:none; cursor:not-allowed; transform:none; }
`;

// ── THEME TOGGLE BUTTON ──────────────────────────────────────────────────────
function ThemeToggle({ lightMode }) {
  const { theme, toggleTheme } = useTheme();
  const isDark = theme === "dark";
  
  return (
    <button
      onClick={toggleTheme}
      style={{
        background: lightMode ? "rgba(0,0,0,0.05)" : "rgba(255,255,255,0.12)",
        border: `1px solid ${lightMode ? "rgba(0,0,0,0.1)" : "rgba(255,255,255,0.2)"}`,
        borderRadius: 20,
        padding: "5px 12px",
        color: lightMode ? "#333" : "#e8f5e0",
        fontSize: 12,
        cursor: "pointer",
        display: "flex",
        alignItems: "center",
        gap: 5,
        fontFamily: "'DM Sans',sans-serif"
      }}
    >
      {isDark ? "☀️ Light" : "🌙 Dark"}
    </button>
  );
}

// ── LANGUAGE DATA ─────────────────────────────────────────────────────────────
const LANGS = { en:{label:"English",flag:"🇺🇬"}, lg:{label:"Luganda",flag:"🇺🇬"}, sw:{label:"Kiswahili",flag:"🇰🇪"}, rny:{label:"Runyankore",flag:"🇺🇬"} };

const AT = {
  en: {
    welcome:"Welcome to", tagline:"Save smart. Live well.",
    login:"Sign In", signup:"Create Account",
    fullName:"Full Name", email:"Email Address", phone:"Phone Number",
    password:"Password", confirmPwd:"Confirm Password",
    loginBtn:"Sign In", signupBtn:"Create Account",
    noAccount:"Don't have an account?", hasAccount:"Already have an account?",
    signupLink:"Create one", loginLink:"Sign in",
    forgotPwd:"Forgot password?", orContinue:"or continue with",
    namePh:"e.g. Rogers Tumusiime", emailPh:"you@email.com",
    phonePh:"+256 7XX XXX XXX", pwdPh:"Min. 6 characters",
    err:{ nameReq:"Full name is required", emailBad:"Enter a valid email", phoneBad:"Enter a valid phone number", pwdShort:"Password must be at least 6 characters", pwdMismatch:"Passwords do not match", emailExists:"An account with this email already exists", badCreds:"Incorrect email or password" },
    success:"Account created! Welcome to Akiba 🎉",
  },
  lg: {
    welcome:"Tukwagaliza ku", tagline:"Tereka obulungi. Beera bulungi.",
    login:"Yingira", signup:"Tondawo Akaunti",
    fullName:"Erinnya Lyonna", email:"Aderesi y'Email", phone:"Enamba ya Simu",
    password:"Ekigambo ky'Okulinda", confirmPwd:"Kakasa Ekigambo",
    loginBtn:"Yingira", signupBtn:"Tondawo Akaunti",
    noAccount:"Tolina akaunti?", hasAccount:"Olina akaunti?",
    signupLink:"Gitonde", loginLink:"Yingira",
    forgotPwd:"Werabide ekigambo?", orContinue:"oba enjogereza n'",
    namePh:"e.g. Rogers Tumusiime", emailPh:"ggwe@email.com",
    phonePh:"+256 7XX XXX XXX", pwdPh:"Obutono 6 by'ebbaluwa",
    err:{ nameReq:"Erinnya lyonna liyinzika", emailBad:"Yingiza aderesi y'email entuufu", phoneBad:"Yingiza enamba ya simu entuufu", pwdShort:"Ekigambo kiba obutono 6", pwdMismatch:"Ebigambo ebitali kimwe", emailExists:"Akaunti ya email eno eriwo", badCreds:"Email oba ekigambo si bituufu" },
    success:"Akaunti etondeddwa! Tukwagaliza ku Akiba 🎉",
  },
  sw: {
    welcome:"Karibu kwenye", tagline:"Weka vizuri. Ishi vizuri.",
    login:"Ingia", signup:"Fungua Akaunti",
    fullName:"Jina Kamili", email:"Barua Pepe", phone:"Nambari ya Simu",
    password:"Nenosiri", confirmPwd:"Thibitisha Nenosiri",
    loginBtn:"Ingia", signupBtn:"Fungua Akaunti",
    noAccount:"Huna akaunti?", hasAccount:"Una akaunti tayari?",
    signupLink:"Fungua moja", loginLink:"Ingia",
    forgotPwd:"Umesahau nenosiri?", orContinue:"au endelea na",
    namePh:"mfano Rogers Tumusiime", emailPh:"wewe@email.com",
    phonePh:"+256 7XX XXX XXX", pwdPh:"Angalau herufi 6",
    err:{ nameReq:"Jina kamili linahitajika", emailBad:"Ingiza barua pepe sahihi", phoneBad:"Ingiza nambari sahihi ya simu", pwdShort:"Nenosiri liwe na herufi 6+", pwdMismatch:"Nenosiri hazilingani", emailExists:"Akaunti ipo tayari", badCreds:"Barua pepe au nenosiri si sahihi" },
    success:"Akaunti imefunguliwa! Karibu Akiba 🎉",
  },
  rny: {
    welcome:"Turakureebereza ku", tagline:"Bika obulungi. Isha neza.",
    login:"Injira", signup:"Tondawo Konti",
    fullName:"Eizina Ryona", email:"Aderesi ya Email", phone:"Namba ya Siimu",
    password:"Ekigambo ky'Okurinda", confirmPwd:"Kakasa Ekigambo",
    loginBtn:"Injira", signupBtn:"Tondawo Konti",
    noAccount:"Ntolina konti?", hasAccount:"Olina konti?",
    signupLink:"Gitonde", loginLink:"Injira",
    forgotPwd:"Werabire ekigambo?", orContinue:"oba enjogereza n'",
    namePh:"e.g. Rogers Tumusiime", emailPh:"iwe@email.com",
    phonePh:"+256 7XX XXX XXX", pwdPh:"Obutono 6 by'ebbaluwa",
    err:{ nameReq:"Eizina ryona ririndwa", emailBad:"Injiza aderesi ntuufu ya email", phoneBad:"Injiza namba ntuufu ya siimu", pwdShort:"Ekigambo kiba obutono 6", pwdMismatch:"Ebigambo ebitali kimwe", emailExists:"Konti ya email eno eriho", badCreds:"Email oba ekigambo si ntuufu" },
    success:"Konti etondeddwa! Turakureebereza ku Akiba 🎉",
  },
};

const T = {
  en: {
    appName:"Akiba", greeting:"Good day,",
    totalSavings:"Total Savings", monthlyGoal:"Monthly Goal", progress:"Progress",
    quickSave:"Quick Save", scanDoc:"Scan Doc", viewTips:"Tips",
    recentTx:"Recent Transactions", noTx:"No transactions yet.",
    nav:["Home","Scan","Tips","Account"],
    scanTitle:"Scan Financial Document",
    scanDesc:"Upload a bank statement, loan agreement, payslip or receipt — AI will explain it in plain language.",
    scanBtn:"Tap to upload document", analysing:"Analysing…",
    scanResult:"📄 Document Summary", scanAnother:"Scan Another",
    tipsTitle:"Financial Tips", dailyWisdom:"Today's Wisdom",
    proverb:'"A small amount saved daily becomes a large amount over time."',
    proverbSrc:"— Ugandan Proverb",
    goalLabel:"Set Monthly Goal (UGX)", setGoal:"Update", goalSaved:"Goal updated!",
    addTx:"Add Transaction", txDesc:"Description", txAmt:"Amount (UGX)",
    income:"Income", expense:"Expense", add:"Add", cancel:"Cancel",
    linkedBank:"Linked Bank", mobileMoney:"Mobile Money",
    notifs:"Notifications", security:"Security", currency:"UGX",
    logout:"Sign Out", logoutConfirm:"Sign out of Akiba?",
    tips:[
      {icon:"💡",title:"Save before you spend",body:"Transfer savings the same day you receive income — treat it like a bill you must pay yourself first."},
      {icon:"📊",title:"Track every expense",body:"Small daily expenses add up fast. Recording them reveals patterns you can fix and money you didn't know you were losing."},
      {icon:"🏦",title:"Use a SACCO",body:"Joining a SACCO gives you access to low-interest loans and the power of group savings. Many SACCOs offer 15–20% annual returns."},
      {icon:"📱",title:"Mobile money savings",body:"Use MTN MoMo Save or Airtel Money. Even UGX 1,000/day = UGX 365,000/year."},
      {icon:"🎯",title:"Set specific goals",body:"Saving for something specific (school fees, land, business) is more powerful than saving in general."},
      {icon:"⚠️",title:"Avoid impulse spending",body:"Before any unplanned purchase, wait 24 hours. Most impulse urges disappear — and your savings stay intact."},
    ],
  },
  lg: {
    appName:"Akiba", greeting:"Wasuze otya,",
    totalSavings:"Ssente Zonna Eziterekeddwa", monthlyGoal:"Ekigendererwa kya Mwezi", progress:"Enkulakulana",
    quickSave:"Tereka Mangu", scanDoc:"Keba Mpapula", viewTips:"Amakubo",
    recentTx:"Okuwaŋŋaŋŋanya", noTx:"Tewaliiwo kuwaŋŋaŋŋanya.",
    nav:["Ennyumba","Keba","Amakubo","Akaunti"],
    scanTitle:"Keba Mpapula y'Ensimbi",
    scanDesc:"Yongereza ebbaluwa y'okuterekera oba payslip. AI yaffe ejjulira mu lulimi olwangu.",
    scanBtn:"Nyiga okuyongereza mpapula", analysing:"Ekikolwa mpapula…",
    scanResult:"📄 Ensonga z'Empapula", scanAnother:"Keba Endala",
    tipsTitle:"Amakubo ag'Ensimbi", dailyWisdom:"Amagezi ga Leero",
    proverb:'"Ntono eziterekeddwa buli lunaku ziba nnyingi oluvannyuma."',
    proverbSrc:"— Olugero lw'Uganda",
    goalLabel:"Teeka Ekigendererwa (UGX)", setGoal:"Vvonya", goalSaved:"Ekigendererwa kivvunyiziddwa!",
    addTx:"Yongereza Okuwaŋŋaŋŋanya", txDesc:"Ebisooka", txAmt:"Omuwendo (UGX)",
    income:"Ensimbi Ezazze", expense:"Okugulawo", add:"Yongereza", cancel:"Sazaamu",
    linkedBank:"Banki Eyogereddwa", mobileMoney:"Ssente za Simu",
    notifs:"Obubaka", security:"Obukuumi", currency:"UGX",
    logout:"Fuluma", logoutConfirm:"Fuluma mu Akiba?",
    tips:[
      {icon:"💡",title:"Tereka nga tonnakozesa",body:"Yimba ssente z'okutereka buli lw'ofuna empeera — beera nga biso ebisaasira."},
      {icon:"📊",title:"Keba ensimbi zonna",body:"Ebintu ebitono buli lunaku bibundikira. Okubikyusa kujjulira empisa onayinza okuzikkiriza."},
      {icon:"🏦",title:"Kozesa SACCO",body:"Okuyingira SACCO kukuwa omutego omunyiga era empeereza ya group."},
      {icon:"📱",title:"Ssente za simu",body:"Kozesa MTN MoMo Save okugabula ensimbi ntono buli lunaku."},
      {icon:"🎯",title:"Teeka ebisuubizo ebimu",body:"Okutereka okw'ekintu ekirala kusinga okutereka mu bwangu."},
      {icon:"⚠️",title:"Weewale okugula mu mangu",body:"Linda awezi 24 nga tonnagula kintu ekyali tekisuubiziddwa."},
    ],
  },
  sw: {
    appName:"Akiba", greeting:"Habari,",
    totalSavings:"Jumla ya Akiba", monthlyGoal:"Lengo la Mwezi", progress:"Maendeleo",
    quickSave:"Weka Haraka", scanDoc:"Scan Hati", viewTips:"Vidokezo",
    recentTx:"Miamala ya Hivi Karibuni", noTx:"Hakuna miamala bado.",
    nav:["Nyumbani","Scan","Vidokezo","Akaunti"],
    scanTitle:"Scan Hati ya Fedha",
    scanDesc:"Pakia taarifa ya benki au payslip. AI yetu itaeleza kwa lugha rahisi.",
    scanBtn:"Gonga kupakia hati", analysing:"Inachambua…",
    scanResult:"📄 Muhtasari wa Hati", scanAnother:"Scan Nyingine",
    tipsTitle:"Vidokezo vya Fedha", dailyWisdom:"Hekima ya Leo",
    proverb:'"Kilichowekwa kidogo kila siku kinakuwa kikubwa baada ya muda."',
    proverbSrc:"— Msemo wa Uganda",
    goalLabel:"Weka Lengo la Mwezi (UGX)", setGoal:"Sasisha", goalSaved:"Lengo limesasishwa!",
    addTx:"Ongeza Muamala", txDesc:"Maelezo", txAmt:"Kiasi (UGX)",
    income:"Mapato", expense:"Matumizi", add:"Ongeza", cancel:"Ghairi",
    linkedBank:"Benki Iliyounganishwa", mobileMoney:"Pesa ya Simu",
    notifs:"Arifa", security:"Usalama", currency:"UGX",
    logout:"Toka", logoutConfirm:"Toka kwenye Akiba?",
    tips:[
      {icon:"💡",title:"Weka kabla ya kutumia",body:"Hamisha akiba siku hiyo hiyo unapopata mshahara."},
      {icon:"📊",title:"Fuatilia kila gharama",body:"Matumizi madogo kila siku yanajumlika. Kuyaandika kunafunua mifumo."},
      {icon:"🏦",title:"Tumia SACCO",body:"Kujiunga SACCO kunakupa ufikiaji wa mikopo ya riba ndogo."},
      {icon:"📱",title:"Akiba ya simu",body:"Tumia MTN MoMo Save kuweka fedha kidogo kila siku."},
      {icon:"🎯",title:"Weka malengo maalum",body:"Kuweka akiba kwa lengo maalum ni nguvu zaidi kuliko kwa ujumla."},
      {icon:"⚠️",title:"Epuka manunuzi ya haraka",body:"Subiri masaa 24 kabla ya ununuzi usiokusudiwa."},
    ],
  },
  rny: {
    appName:"Akiba", greeting:"Oraire ota,",
    totalSavings:"Ensimbi Zose Zibitswe", monthlyGoal:"Ekyesubirwa kya Mwezi", progress:"Ebikorwa",
    quickSave:"Bika Mangu", scanDoc:"Reba Mpapuro", viewTips:"Amakuru",
    recentTx:"Obuguzi Obwaheru", noTx:"Nta buguzi buraahari.",
    nav:["Nyumba","Reba","Amakuru","Konti"],
    scanTitle:"Reba Mpapuro y'Ensimbi",
    scanDesc:"Hindura ebbaluwa y'eby'obuhangwa oba payslip. AI yaitu ejúúra mu rurimi rwaawe.",
    scanBtn:"Nyiga okuhindura mpapuro", analysing:"Ereba mpapuro…",
    scanResult:"📄 Ensonga z'Empapuro", scanAnother:"Reba Endara",
    tipsTitle:"Amakuru g'Ensimbi", dailyWisdom:"Amagezi g'Eizooba",
    proverb:'"Ntono zibitswe buri eisho ziba nnyingi oluvannyuma."',
    proverbSrc:"— Akavuga k'Uganda",
    goalLabel:"Teeka Ekyesubirwa (UGX)", setGoal:"Hindura", goalSaved:"Ekyesubirwa kihindurwa!",
    addTx:"Yongereza Obuguzi", txDesc:"Ebisooka", txAmt:"Omuwendo (UGX)",
    income:"Ensimbi Ezazire", expense:"Okugura", add:"Yongereza", cancel:"Reka",
    linkedBank:"Banki Eyogereddwa", mobileMoney:"Ensimbi za Siimu",
    notifs:"Obubaka", security:"Obukuumi", currency:"UGX",
    logout:"Fuluma", logoutConfirm:"Fuluma mu Akiba?",
    tips:[
      {icon:"💡",title:"Bika oza okozesa",body:"Hindura ensimbi z'okubika ahari olinda empeera."},
      {icon:"📊",title:"Rinda ensimbi zose",body:"Ahantu hatono buri eisho hatungaana."},
      {icon:"🏦",title:"Kozesa SACCO",body:"Okwinjira SACCO kukuha omutego munima era obukuru bw'ekibiina."},
      {icon:"📱",title:"Ensimbi za siimu",body:"Kozesa MTN MoMo Save okubika ensimbi ntono buri eisho."},
      {icon:"🎯",title:"Teeka ebisubirwa ebimu",body:"Okubika okw'ekintu ekirala kusinga okubika mu bwangu."},
      {icon:"⚠️",title:"Weewale okugura mu mangu",body:"Linda awara 24 nga tonnagura kintu ekyali tekisubirwa."},
    ],
  },
};

// ── STORAGE ───────────────────────────────────────────────────────────────────
const USERS_KEY = "akiba_users_v2";
const SESSION_KEY = "akiba_session_v2";
const dataKey = (e) => `akiba_data_v2_${e}`;
const getUsers = () => { try { return JSON.parse(localStorage.getItem(USERS_KEY)||"{}"); } catch { return {}; } };
const saveUsers = (u) => localStorage.setItem(USERS_KEY, JSON.stringify(u));
const getSession = () => { try { return JSON.parse(localStorage.getItem(SESSION_KEY)||"null"); } catch { return null; } };
const saveSession = (s) => localStorage.setItem(SESSION_KEY, JSON.stringify(s));
const clearSession = () => localStorage.removeItem(SESSION_KEY);
const getUserData = (e) => { try { return JSON.parse(localStorage.getItem(dataKey(e))||"null"); } catch { return null; } };
const saveUserData = (e, d) => localStorage.setItem(dataKey(e), JSON.stringify(d));
const uid = () => Math.random().toString(36).slice(2,9);
const fmt = (n) => Number(n).toLocaleString("en-UG");
const mkData = () => ({ lang:"en", goal:2000000, transactions:[{ id:uid(), label:"Welcome bonus", amount:10000, type:"income", date:new Date().toISOString().slice(0,10) }] });

// ── LANG MENU (UPDATED TO USE THEME) ─────────────────────────────────────────
function LangMenu({ current, onChange, light }) {
  const [open, setOpen] = useState(false);
  const { theme } = useTheme();
  const isDark = theme === "dark";
  
  return (
    <div style={{ position:"relative" }}>
      <button onClick={() => setOpen(!open)} style={{ background: light?"rgba(0,0,0,0.05)":"rgba(255,255,255,0.12)", border:`1px solid ${light?"rgba(0,0,0,0.1)":"rgba(255,255,255,0.2)"}`, borderRadius:20, padding:"5px 12px", color:light?"#333":"#e8f5e0", fontSize:12, cursor:"pointer", display:"flex", alignItems:"center", gap:5, fontFamily:"'DM Sans',sans-serif" }}>
        {LANGS[current].flag} {LANGS[current].label} ▾
      </button>
      {open && (
        <div style={{ position:"absolute", right:0, top:36, background: isDark ? "#1f2937" : "#fff", borderRadius:12, boxShadow:"0 8px 32px rgba(0,0,0,0.2)", zIndex:200, overflow:"hidden", minWidth:150 }}>
          {Object.entries(LANGS).map(([k,v]) => (
            <button key={k} onClick={()=>{onChange(k);setOpen(false);}} style={{ display:"flex", alignItems:"center", gap:10, width:"100%", padding:"10px 16px", background:current===k?(isDark?"#2d3a4e":"#e8f5e0"):"transparent", border:"none", cursor:"pointer", fontSize:13, color: isDark ? "#eef5f0" : "#0d2240", fontFamily:"'DM Sans',sans-serif" }}>
              {v.flag} {v.label}
            </button>
          ))}
  
