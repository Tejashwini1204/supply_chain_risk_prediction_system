import streamlit as st
import pandas as pd
import pickle
from datetime import datetime
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

st.set_page_config(layout="wide")
#st.image("login.jpeg")


# --------------------------
# AUTH SYSTEM (ADD HERE)
# --------------------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = None

# Start with signup first
if "page" not in st.session_state:
    st.session_state.page = "signup"

#---------------
# CSS
#---------------
st.markdown("""
<style>

/*.main {
    background-color:rgb(2, 16, 44);
}*/

/* ✅ FULL WIDTH FIX */
.block-container {
    max-width: 100%;
    padding-left: 3rem;
    padding-right: 3rem;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

html, body, [class*="css"] {
    height: 100%;
    margin: 0;
    padding: 0;
}

/* 🚫 Remove Streamlit header completely */
header {
    visibility: hidden;
}

/* 🚫 Remove top spacing */
.block-container {
    padding-top: 0rem !important;
}

/* Optional: remove footer */
footer {
    visibility: hidden;
}

/* FULL WIDTH FIX */
.stApp {
    margin: 0;
    padding: 0;
}

/* Main title centered */
h1 {
    text-align: center;
    font-size: 45px;
    font-weight: 700;
    margin-bottom: 10px;
}

/* Other headings left aligned */
h2 {
    text-align: left;
}

h3 {
    text-align: center;
    color: #C5C6C7;
    margin-top: -8px;
}

/* Paragraph visibility fix */
.header-box p {
    font-size: 20px;
    font-weight: 500;
    color:rgb(209, 207, 207);
    text-align: center;
    max-width: 900px;
    margin: 10px auto 0 auto;
    line-height: 1.9;
}

.header-box {
    text-align: center;
    margin-top: 30px;
    margin-bottom: 40px;
}

/* CARDS */
.card {
    background-color:rgb(69, 125, 255);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
}

/* METRIC */
.metric {
    text-align: center;
    font-size: 22px;
}

/* FORM */
.form-card {
    background: #1c1f26;
    padding: 25px;
    border-radius: 15px;
    margin-top: 20px;
}

/* RESULT */
.result-card {
    background: #1c1f26;
    padding: 20px;
    border-radius: 15px;
    margin-top: 20px;
    text-align: center;
}

/* BUTTON */
.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 45px;
    font-size: 16px;
}

/* AUTH BOX CENTER */
.auth-box {
    text-align: center !important;
    margin-bottom: 20px;
    width: 100%;
    max-width: 450px;
    margin: 120px auto;
    background: rgba(0, 0, 0, 0.7);
    padding: 40px;
    border-radius: 18px;
    backdrop-filter: blur(14px);
}

/* 🔥 Title */
.auth-box h2 {
    font-size: 34px !important;
    font-weight: 700 !important;
}

/* 🔥 Labels */
div[data-testid="stTextInput"] label {
    font-size: 18px !important;
}

/* 🔥 Input text */
div[data-testid="stTextInput"] input {
    height: 50px !important;
    font-size: 18px !important;
}

/* 🔥 Buttons */
div[data-testid="stButton"] button {
    height: 52px !important;
    font-size: 18px !important;
    font-weight: 600 !important;
}
/* 🔥 Reduce width */
div[data-testid="stTextInput"],
div[data-testid="stButton"] {
    max-width: 450px;   /* was ~450 */
    margin: auto;
}
/* 🔥 Labels (Username / Password) */
label {
    font-size: 18px !important;   /* slightly bigger */
}

/* 🔥 Input text */
.stTextInput input {
    height: 48px;
    font-size: 17px;
}

/* 🔥 Buttons */
.stButton > button {
    height: 52px;
    font-size: 17px;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# BACKGROUND FUNCTIONS
# --------------------------

# 🔹 AUTH (LOGIN + SIGNUP) → IMAGE BACKGROUND
def auth_background():
    import base64
    with open(os.path.join(BASE_DIR, "login.jpeg"), "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background: url("data:image/jpeg;base64,{encoded}") no-repeat center center fixed;
        background-size: cover;
    }}
    </style>
    """, unsafe_allow_html=True)


# 🔹 DASHBOARD → NAVY BLUE ONLY
def dashboard_background():
    st.markdown("""
    <style>
    .stApp {
        background-color: rgb(2, 16, 44);
    }
    </style>
    """, unsafe_allow_html=True)    # dashboard image
# --------------------------
# SIGNUP PAGE
# --------------------------
def signup_page():
    #col1, col2, col3 = st.columns([1, 2, 1])  # center layout

    #with col2:
    st.markdown("""
        <style>
        .center-box {
            max-width: 450px;
            margin: 120px auto;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='center-box'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center;'>📝 Create Account</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Signup"):
        if username == "" or password == "":
            st.warning("Please fill all fields")
        elif username in st.session_state.users:
            st.error("User already exists")
        else:
            st.session_state.users[username] = password
            st.success("Account created! Please login")
            st.session_state.page = "login"
            st.rerun()

    if st.button("Already have account? Login"):
        st.session_state.page = "login"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True) # ✅ FIXED

# --------------------------
# LOGIN PAGE
# --------------------------
def login_page():
    st.markdown("""
        <style>
        .center-box {
            max-width: 450px;
            margin: 120px auto;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='center-box'>", unsafe_allow_html=True)

    st.markdown("<h2 style='text-align:center;'>🔐 Login</h2>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "" or password == "":
            st.warning("Please enter username and password")
        elif username in st.session_state.users and st.session_state.users[username] == password:
            st.session_state.logged_in = True
            st.session_state.current_user = username   # ✅ ADD THIS
            st.rerun()
        else:
            st.error("Invalid credentials")

    if st.button("New user? Signup"):
        st.session_state.page = "signup"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)# ✅ FIXED
# --------------------------
# DATABASE SETUP (RUNS ONCE)
# --------------------------
conn = sqlite3.connect(os.path.join(BASE_DIR, "predictions.db"))
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    vendor TEXT,
    mode TEXT,
    quantity INT,
    freight REAL,
    price REAL,
    probability REAL,
    timestamp TEXT
)
""")

conn.commit()
conn.close()

def load_db_data():
    conn = sqlite3.connect(os.path.join(BASE_DIR, "predictions.db"))
    df = pd.read_sql_query("SELECT * FROM predictions", conn)
    conn.close()
    return df

# --------------------------
# LOAD DATA
# --------------------------
df = pd.read_csv(os.path.join(BASE_DIR, "SCMS_Delivery_History_Dataset.csv"))

# Load model & encoders
model = pickle.load(open(os.path.join(BASE_DIR, "model.pkl"), "rb"))
le_vendor = pickle.load(open(os.path.join(BASE_DIR, "le_vendor.pkl"), "rb"))
le_mode = pickle.load(open(os.path.join(BASE_DIR, "le_mode.pkl"), "rb"))
scaler = pickle.load(open(os.path.join(BASE_DIR, "scaler.pkl"), "rb"))
columns = pickle.load(open(os.path.join(BASE_DIR, "columns.pkl"), "rb"))

import joblib

metrics = joblib.load(os.path.join(BASE_DIR, "metrics.pkl"))

accuracy = metrics["accuracy"]
precision = metrics["precision"]
recall = metrics["recall"]
y_test = metrics["y_test"]
y_pred = metrics["y_pred"]
y_prob = metrics["y_prob"]

# --------------------------
# AUTH CONTROL
# --------------------------
if st.session_state.logged_in:
    dashboard_background()
else:
    auth_background()

    if st.session_state.page == "signup":
        signup_page()
    else:
        login_page()

    st.stop()
# --------------------------
# TITLE
# --------------------------
st.markdown("""
<div class="header-box">
    <h1>SupplyGuard: Intelligent Risk Insights for Logistics</h1>
    <p>
        Predict delivery disruptions, evaluate supplier reliability, and make smarter shipment decisions in real time.
    </p>
</div>
""", unsafe_allow_html=True)

# --------------------------
# SIDEBAR
# --------------------------
menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Predict Delay",
    "Supplier Risk",
    "Model Performance",
    "Live Analytics" 
])

# --------------------------
# LOGOUT BUTTON (ADD HERE)
# --------------------------
st.sidebar.markdown("---")
st.sidebar.markdown(f"👤 {st.session_state.current_user}")

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.page = "login"
    st.rerun()

# --------------------------
# DASHBOARD
# --------------------------
if menu == "Dashboard":

    df['Scheduled Delivery Date'] = pd.to_datetime(df['Scheduled Delivery Date'])
    df['Delivered to Client Date'] = pd.to_datetime(df['Delivered to Client Date'])

    df['delay'] = (df['Delivered to Client Date'] > df['Scheduled Delivery Date']).astype(int)

    total_orders = len(df)
    suppliers = df['Vendor'].nunique()
    delay_rate = round(df['delay'].mean()*100,2)

    # --------------------------
    # HERO SECTION
    # --------------------------
    st.markdown("""
    <div style='text-align:center; padding-top:10px; padding-bottom:20px;'>

    <h1 style='font-size:40px;'>📦 Supply Chain Dashboard</h1>

    <p style='color:#C5C6C7; font-size:18px; max-width:700px; margin:auto;'>
    Monitor delivery performance, supplier risk, and shipment efficiency
    </p>

    </div>
    """, unsafe_allow_html=True)

    # KPI CARDS
    col1, col2, col3 = st.columns(3)

    col1.markdown(f"<div class='card'><h4>📦 Orders</h4><h2>{total_orders}</h2></div>", unsafe_allow_html=True)
    col2.markdown(f"<div class='card'><h4>🏭 Suppliers</h4><h2>{suppliers}</h2></div>", unsafe_allow_html=True)
    col3.markdown(f"<div class='card'><h4>⚠️ Delay %</h4><h2>{delay_rate}%</h2></div>", unsafe_allow_html=True)

    st.markdown("<br><br><hr><br>", unsafe_allow_html=True)

    # --------------------------
    # ANALYTICS SECTION
    # --------------------------
    st.markdown("<h2 style='text-align:center;'>📊 Insights</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚚 Delay by Shipment Mode")
        mode_delay = df.groupby('Shipment Mode')['delay'].mean()
        st.bar_chart(mode_delay)

    with col2:
        st.markdown("### 🏭 Top Risk Suppliers")
        risk = df.groupby('Vendor')['delay'].mean().sort_values(ascending=False)
        st.bar_chart(risk.head(5))
    
    st.divider()

    st.subheader("📌 Business Insights")

    st.markdown("""
    <div style='background:#1c1f26; padding:20px; border-radius:10px'>
    <ul>
    <li>🚨 High-risk suppliers identified</li>
    <li>🚚 Ocean shipments show more delays</li>
    <li>📦 Large orders increase risk</li>
    <li>💰 Freight cost impacts delivery</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)

# --------------------------
# PREDICTION
# --------------------------
elif menu == "Predict Delay":

    # --------------------------
    # CENTER PAGE + STYLE
    # --------------------------
    st.markdown("""
    <style>
    .container {
        max-width: 750px;
        margin: auto;
    }
    .card {
        background: #1c1f26;
        padding: 25px;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0,0,0,0.3);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='container'>", unsafe_allow_html=True)

    # --------------------------
    # TITLE
    # --------------------------
    st.markdown("""
        <h2 style='text-align:center;'>🔍 Predict Delivery Delay</h2>
        <p style='text-align:center; color:#C5C6C7;'>
        Enter shipment details to estimate delay risk
        </p>
    """, unsafe_allow_html=True)

    # --------------------------
    # FORM CARD
    # --------------------------
    st.markdown("<div class='card'>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        vendor = st.selectbox("Vendor", le_vendor.classes_)
        quantity = st.number_input("Quantity", 1, 10000)

    with col2:
        mode = st.selectbox("Shipment Mode", le_mode.classes_)
        freight = st.number_input("Freight Cost", 0.0, 10000.0)

    price = st.number_input("Unit Price", 0.0, 10000.0)

    st.markdown("<br>", unsafe_allow_html=True)

    predict_btn = st.button("🚀 Predict")

    st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------
    # ENCODING
    # --------------------------
    vendor_enc = le_vendor.transform([vendor])[0]
    mode_enc = le_mode.transform([mode])[0]

    # --------------------------
    # PREDICTION
    # --------------------------
    if predict_btn:

        today = datetime.today()
        day_of_week = today.weekday()
        month = today.month

        input_df = pd.DataFrame(columns=columns)
        input_df.loc[0] = 0

        input_df['Line Item Quantity'] = quantity
        input_df['Freight Cost (USD)'] = freight
        input_df['Unit Price'] = price
        input_df['day_of_week'] = day_of_week
        input_df['month'] = month

        vendor_col = f"Vendor_{vendor}"
        if vendor_col in input_df.columns:
            input_df[vendor_col] = 1

        mode_col = f"Shipment Mode_{mode}"
        if mode_col in input_df.columns:
            input_df[mode_col] = 1

        num_cols = ['Line Item Quantity', 'Freight Cost (USD)', 'Unit Price']
        input_df[num_cols] = scaler.transform(input_df[num_cols])

        # ✅ SAVE INPUT FOR COMPARISON
        st.session_state["input_df"] = input_df

        result = model.predict(input_df)
        prob = model.predict_proba(input_df)[0][1]

        # --------------------------
        # SAVE TO DATABASE
        # --------------------------
        conn = sqlite3.connect(os.path.join(BASE_DIR, "predictions.db"))
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO predictions VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            vendor,
            mode,
            quantity,
            freight,
            price,
            float(prob),
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))
        st.success("✅ Saved to DB")

        conn.commit()
        conn.close()

        # --------------------------
        # RESULT CARD
        # --------------------------
        st.markdown("<div class='card' style='margin-top:20px; text-align:center;'>", unsafe_allow_html=True)

        st.markdown(f"### 📊 Delay Probability: {round(prob*100,2)}%")
        st.write("### 📌 Risk Level:",
        "High 🔴" if prob > 0.6 else "Medium 🟡" if prob > 0.3 else "Low 🟢")

        st.progress(float(prob))

        if prob > 0.6:
            st.error("⚠️ High Risk of Delay")
            st.markdown("📌 Use faster shipping or change supplier")
        elif prob > 0.3:
            st.warning("⚠️ Medium Risk of Delay")
            st.markdown("📌 Monitor shipment closely")
        else:
            st.success("✅ Shipment likely to arrive on time")
            st.markdown("📌 No action needed")

        # --------------------------
        # SMART ACTIONS
        # --------------------------
        if prob > 0.6:
            st.markdown("""
            ### 🚨 Recommended Actions
            - Switch to faster shipping (Air)
            - Choose a low-risk supplier
            - Reduce shipment size
            - Increase logistics budget
            """)
        elif prob > 0.3:
            st.markdown("""
            ### ⚠️ Suggested Actions
            - Monitor shipment closely
            - Keep backup supplier ready
            - Track shipment updates
            """)
        else:
            st.markdown("""
            ### ✅ Safe Plan
            - No action needed
            - Proceed with shipment
            """)

        st.markdown("---")
        st.markdown("### 🤖 Why this prediction?")
        st.write("""
        - Shipment mode affects delivery speed  
        - High quantity increases delay chances  
        - Supplier history impacts reliability  
        """)

        st.markdown("</div>", unsafe_allow_html=True)

    # --------------------------
    # SMART COMPARE (FIXED UX)
    # --------------------------
    if "input_df" in st.session_state:

        st.divider()
        st.subheader("⚖️ Compare Shipment Options")

        # ✅ Option 1 = SAME as user selected
        st.markdown(f"**Option 1 (Your Choice): 🚚 {mode}**")

        # ✅ Option 2 = User selects alternative
        mode2 = st.selectbox(
            "Option 2 (Try Alternative)",
            [m for m in le_mode.classes_ if m != mode],  # remove same option
            key="mode2"
        )

        # --------------------------
        # CREATE DATA
        # --------------------------
        df1 = st.session_state["input_df"].copy()
        df2 = st.session_state["input_df"].copy()

        # Reset shipment columns
        for col in df1.columns:
            if "Shipment Mode_" in col:
                df1[col] = 0
                df2[col] = 0

        # Apply Option 1 (original)
        if f"Shipment Mode_{mode}" in df1.columns:
            df1[f"Shipment Mode_{mode}"] = 1

        # Apply Option 2 (selected)
        if f"Shipment Mode_{mode2}" in df2.columns:
            df2[f"Shipment Mode_{mode2}"] = 1

        # --------------------------
        # PREDICT
        # --------------------------
        p1 = model.predict_proba(df1)[0][1]
        p2 = model.predict_proba(df2)[0][1]

        # --------------------------
        # DISPLAY
        # --------------------------
        col1, col2 = st.columns(2)

        col1.metric(
            f"🚚 {mode}",
            f"{round(p1*100,2)}%"
        )

        col2.metric(
            f"🚚 {mode2}",
            f"{round(p2*100,2)}%"
        )

        # --------------------------
        # DECISION
        # --------------------------
        diff = abs(p1 - p2) * 100

        if p1 < p2:
            st.success(f"✅ Your choice ({mode}) is better (↓ {round(diff,2)}% lower risk)")
        elif p2 < p1:
            st.success(f"✅ {mode2} is better (↓ {round(diff,2)}% lower risk)")
        else:
            st.info("⚖️ Both options have similar risk")

        # --------------------------
        # SMART INSIGHT
        # --------------------------
        st.markdown("### 🤖 Recommendation")

        if p2 < p1:
            st.markdown(f"👉 Consider switching to **{mode2}** to reduce delay risk")
        else:
            st.markdown("👉 Current shipment mode is optimal")

    else:
        st.info("👉 Click 'Predict' first to enable comparison")

    # --------------------------
    # 🔥 AUTO BEST MODE (SMART AI)
    # --------------------------
    st.divider()
    st.subheader("🧠 Best Shipment Mode Recommendation")

    if "input_df" in st.session_state:

        base_df = st.session_state["input_df"]

        results = []

        # Test ALL shipment modes
        for m in le_mode.classes_:

            temp_df = base_df.copy()

            # Reset all shipment columns
            for col in temp_df.columns:
                if "Shipment Mode_" in col:
                    temp_df[col] = 0

            # Apply current mode
            col_name = f"Shipment Mode_{m}"
            if col_name in temp_df.columns:
                temp_df[col_name] = 1

            prob = model.predict_proba(temp_df)[0][1]

            results.append({
                "Mode": m,
                "Delay Risk (%)": round(prob * 100, 2)
            })

        # Convert to DataFrame
        result_df = pd.DataFrame(results)

        # Sort (LOWEST risk first)
        result_df = result_df.sort_values(by="Delay Risk (%)")

        # --------------------------
        # 🎯 SHOW BEST OPTION
        # --------------------------
        best_mode = result_df.iloc[0]["Mode"]
        best_risk = result_df.iloc[0]["Delay Risk (%)"]

        st.success(f"🏆 Best Shipment Mode: **{best_mode}** ({best_risk}%)")

        # --------------------------
        # 📊 SHOW TOP 3 OPTIONS
        # --------------------------
        st.markdown("### 📊 Top 3 Best Options")

        st.dataframe(result_df.head(3), use_container_width=True)

        # --------------------------
        # 📉 VISUAL BAR CHART
        # --------------------------
        st.markdown("### 📈 All Modes Comparison")

        st.bar_chart(result_df.set_index("Mode"))

    else:
        st.info("👉 Click Predict first")
    
    # --------------------------
    # 💰 COST vs RISK INSIGHT
    # --------------------------
    st.divider()
    st.subheader("💰 Cost vs Risk Insight")

    if "input_df" in st.session_state:

        st.markdown("""
        - 🚀 Faster shipping (Air) → Lower delay but higher cost  
        - 🚢 Ocean → Cheaper but higher delay risk  
        - ⚖️ Choose based on urgency vs budget  
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------
# SUPPLIER RISK
# --------------------------
elif menu == "Supplier Risk":

    # --------------------------
    # HEADER
    # --------------------------
    st.markdown("""
    <div style='text-align:center; margin-bottom:30px;'>
        <h2>🏭 Supplier Risk Dashboard</h2>
        <p style='color:#C5C6C7;'>Understand which suppliers are risky and improve decisions</p>
    </div>
    """, unsafe_allow_html=True)

    # --------------------------
    # PREP DATA
    # --------------------------
    df['Scheduled Delivery Date'] = pd.to_datetime(df['Scheduled Delivery Date'])
    df['Delivered to Client Date'] = pd.to_datetime(df['Delivered to Client Date'])

    df['delay'] = (df['Delivered to Client Date'] > df['Scheduled Delivery Date']).astype(int)

    risk = df.groupby('Vendor')['delay'].mean().sort_values(ascending=False)

    # --------------------------
    # KPI CARDS (CLEAN)
    # --------------------------
    high = (risk > 0.15).sum()
    medium = ((risk > 0.08) & (risk <= 0.15)).sum()
    low = (risk <= 0.08).sum()

    c1, c2, c3 = st.columns(3)

    c1.metric("🔴 High Risk", high)
    c2.metric("🟡 Medium Risk", medium)
    c3.metric("🟢 Low Risk", low)

    st.markdown("---")

    # --------------------------
    # MAIN CHART (BIG + CLEAR)
    # --------------------------
    st.subheader("🚨 Most Risky Suppliers")

    top_risk = risk.head(10)

    st.bar_chart(top_risk, use_container_width=True)

    st.info("Higher bar = more delays (more risky supplier)")

    st.markdown("---")

    # --------------------------
    # SIMPLE INSIGHT (NO CLUTTER)
    # --------------------------
    st.subheader("💡 Key Insights")

    st.markdown(f"""
    - 🔴 **{top_risk.index[0]}** is the most risky supplier  
    - 🟢 Majority suppliers are low-risk ({low} suppliers)  
    - ⚠️ Focus on top 3 risky suppliers to reduce delays  
    """)

elif menu == "Model Performance":

    st.markdown("## 📈 Model Performance Dashboard")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Accuracy", f"{round(accuracy*100,2)}%")
        st.metric("Precision", f"{round(precision,2)}")

    with col2:
        st.metric("Recall", f"{round(recall,2)}")

    st.divider()

    # --------------------------
    # CONFUSION MATRIX
    # --------------------------
    st.subheader("📊 Confusion Matrix")

    from sklearn.metrics import confusion_matrix
    import seaborn as sns
    import matplotlib.pyplot as plt

    cm = confusion_matrix(y_test, y_pred)

    # 👇 FIX: control size
    fig, ax = plt.subplots(figsize=(6, 4))

    sns.heatmap(cm, annot=True, fmt='d', cmap="Blues", ax=ax)

    ax.set_xlabel("Predicted Label")
    ax.set_ylabel("Actual Label")
    ax.set_title("Confusion Matrix")

    # 👇 center alignment (optional but better UI)
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.pyplot(fig)


    # --------------------------
    # ROC CURVE
    # --------------------------
    st.subheader("📉 ROC Curve")

    from sklearn.metrics import roc_curve, auc

    fpr, tpr, _ = roc_curve(y_test, y_prob)
    roc_auc = auc(fpr, tpr)

    # 👇 FIX: control size
    fig2, ax2 = plt.subplots(figsize=(6, 4))

    ax2.plot(fpr, tpr, label=f"AUC = {roc_auc:.2f}", linewidth=2)
    ax2.plot([0,1], [0,1], linestyle='--')

    ax2.set_xlabel("False Positive Rate")
    ax2.set_ylabel("True Positive Rate")
    ax2.set_title("ROC Curve")
    ax2.legend()

    # 👇 center alignment
    col4, col5, col6 = st.columns([1,2,1])
    with col5:
        st.pyplot(fig2)

    # ----------------------------
    # FEATURE IMPORTANCE (ADD HERE)
    # ----------------------------
    st.divider()
    st.subheader("🔍 Feature Importance")

    import pandas as pd
    import plotly.express as px
    import pickle

    # Load columns (VERY IMPORTANT)
    columns = pickle.load(open(os.path.join(BASE_DIR, "columns.pkl"), "rb"))

    # Get importance
    importance = model.feature_importances_

    # Create dataframe
    feat_df = pd.DataFrame({
        "Feature": columns,
        "Importance": importance
    })

    # Sort
    feat_df = feat_df.sort_values(by="Importance", ascending=False)

    # Plot
    fig3 = px.bar(
        feat_df.head(15),
        x="Importance",
        y="Feature",
        orientation='h',
        title="Top Important Features"
    )

    st.plotly_chart(fig3, use_container_width=True)

# --------------------------
# LIVE ANALYTICS (NEW)
# --------------------------
elif menu == "Live Analytics":

    import time

    st.title("📡 Live Prediction Dashboard")

    df_db = load_db_data()

    if df_db.empty:
        st.warning("No data yet. Make predictions first.")
    else:
        # Convert timestamp
        df_db['timestamp'] = pd.to_datetime(df_db['timestamp'])

        # --------------------------
        # KPI
        # --------------------------
        col1, col2, col3 = st.columns(3)

        col1.metric("📊 Total Predictions", len(df_db))
        col2.metric("⚠️ Avg Risk", f"{round(df_db['probability'].mean()*100,2)}%")
        col3.metric("🔥 Max Risk", f"{round(df_db['probability'].max()*100,2)}%")

        st.divider()

        # --------------------------
        # TREND
        # --------------------------
        st.subheader("📈 Risk Over Time")
        import plotly.express as px

        fig = px.line(
            df_db,
            x="timestamp",
            y="probability",
            title="📈 Risk Over Time"
        )

        fig.update_layout(
            xaxis_title="Time",
            yaxis_title="Delay Probability"
        )

        st.plotly_chart(fig, use_container_width=True)

        # --------------------------
        # MODE
        # --------------------------
        st.subheader("🚚 Risk by Shipment Mode")
        mode_df = df_db.groupby("mode")["probability"].mean().reset_index()

        fig2 = px.bar(
            mode_df,
            x="mode",
            y="probability",
            title="🚚 Risk by Shipment Mode"
        )

        fig2.update_layout(
            xaxis_title="Shipment Mode",
            yaxis_title="Average Delay Probability"
        )

        st.plotly_chart(fig2, use_container_width=True)

        # --------------------------
        # VENDOR
        # --------------------------
        st.subheader("🏭 Top Risk Vendors")
        vendor_df = (
            df_db.groupby("vendor")["probability"]
            .mean()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig3 = px.bar(
            vendor_df,
            x="vendor",
            y="probability",
            title="🏭 Top Risk Vendors"
        )

        fig3.update_layout(
            xaxis_title="Vendor",
            yaxis_title="Average Delay Probability"
        )

        st.plotly_chart(fig3, use_container_width=True)

        # --------------------------
        # TABLE
        # --------------------------
        st.subheader("📋 Latest Predictions")
        st.dataframe(df_db.tail(10), use_container_width=True)

        # --------------------------
        # AUTO REFRESH
        # --------------------------
        st.caption("🔄 Auto-refreshing every 5 seconds...")
        time.sleep(5)
        st.rerun()