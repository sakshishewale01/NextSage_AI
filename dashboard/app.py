import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="NetSage AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    /* Main background */
    .stApp {
        background-color: #f5f7fb;
    }

    /* Main content width */
    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #101827;
    }

    section[data-testid="stSidebar"] * {
        color: #f8fafc !important;
    }

    /* Main headings */
    h1, h2, h3 {
        color: #102a56 !important;
    }

    /* Normal text */
    p, label, span {
        color: #334155;
    }

    /* Hero */
    .hero {
        background: linear-gradient(
            135deg,
            #102a56,
            #2563eb
        );
        padding: 2.2rem 2.5rem;
        border-radius: 22px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 12px 30px rgba(37, 99, 235, 0.18);
    }

    .hero h1 {
        color: white !important;
        font-size: 2.7rem;
        margin-bottom: 0.3rem;
    }

    .hero p {
        color: #dbeafe !important;
        font-size: 1.1rem;
        margin-bottom: 0;
    }

    /* Metric cards */
    .metric-card {
        background: white;
        padding: 1.4rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
        min-height: 135px;
    }

    .metric-title {
        color: #64748b;
        font-size: 0.95rem;
        font-weight: 600;
    }

    .metric-number {
        color: #0f172a;
        font-size: 2.3rem;
        font-weight: 750;
        margin-top: 0.3rem;
    }

    .metric-description {
        color: #64748b;
        font-size: 0.85rem;
        margin-top: 0.2rem;
    }

    /* Information cards */
    .info-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        border: 1px solid #e2e8f0;
        margin-bottom: 1rem;
        box-shadow: 0 4px 15px rgba(15, 23, 42, 0.05);
    }

    .info-card h3 {
        margin-top: 0;
        color: #102a56 !important;
    }

    .info-card p {
        color: #475569 !important;
        line-height: 1.6;
    }

    /* Status boxes */
    .status-fail {
        background: #fee2e2;
        border-left: 6px solid #ef4444;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        color: #991b1b;
        font-weight: 600;
        margin: 1rem 0;
    }

    .status-pass {
        background: #dcfce7;
        border-left: 6px solid #22c55e;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        color: #166534;
        font-weight: 600;
        margin: 1rem 0;
    }

    .status-review {
        background: #fef3c7;
        border-left: 6px solid #f59e0b;
        padding: 1rem 1.2rem;
        border-radius: 10px;
        color: #92400e;
        font-weight: 600;
        margin: 1rem 0;
    }

    /* Diagnosis highlight */
    .diagnosis-box {
        background: #eff6ff;
        border: 1px solid #bfdbfe;
        border-left: 6px solid #2563eb;
        padding: 1.3rem;
        border-radius: 12px;
        margin: 1rem 0;
    }

    .diagnosis-box strong {
        color: #1d4ed8;
        font-size: 1.05rem;
    }

    /* Solution */
    .solution-box {
        background: #ecfdf5;
        border: 1px solid #bbf7d0;
        border-left: 6px solid #22c55e;
        padding: 1.3rem;
        border-radius: 12px;
        margin: 1rem 0;
    }

    .solution-box strong {
        color: #166534;
    }

    /* Human review */
    .review-box {
        background: white;
        border: 2px solid #c7d2fe;
        border-radius: 16px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 5px 18px rgba(15, 23, 42, 0.06);
    }

    /* Section divider */
    .section-line {
        height: 1px;
        background: #dbe2ea;
        margin: 2rem 0;
    }

    /* Small badge */
    .badge {
        display: inline-block;
        padding: 0.35rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 700;
        background: #dbeafe;
        color: #1d4ed8 !important;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #64748b;
        padding: 2rem 0;
        font-size: 0.85rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
CSV_PATH = BASE_DIR / "results" / "final_diagnosis.csv"


@st.cache_data
def load_data():
    if not CSV_PATH.exists():
        return None

    df = pd.read_csv(CSV_PATH)

    df.columns = df.columns.astype(str).str.strip()

    return df


df = load_data()


# ============================================================
# CHECK DATA
# ============================================================

if df is None:

    st.error(
        "final_diagnosis.csv was not found."
    )

    st.info(
        "Expected location: results/final_diagnosis.csv"
    )

    st.stop()


# ============================================================
# NORMALIZE STATUS
# ============================================================

if "Status" in df.columns:
    df["Status"] = (
        df["Status"]
        .astype(str)
        .str.upper()
        .str.strip()
    )


# ============================================================
# SESSION STATE FOR HUMAN REVIEW
# ============================================================

if "human_reviews" not in st.session_state:
    st.session_state.human_reviews = {}


# ============================================================
# CALCULATE SUMMARY
# ============================================================

total_cases = len(df)

pass_count = (
    int((df["Status"] == "PASS").sum())
    if "Status" in df.columns
    else 0
)

fail_count = (
    int((df["Status"] == "FAIL").sum())
    if "Status" in df.columns
    else 0
)

review_count = (
    int((df["Status"] == "NOT_CHECKED").sum())
    if "Status" in df.columns
    else 0
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        "# 🌐 NetSage AI"
    )

    st.caption(
        "AI-Assisted Network Troubleshooting"
    )

    st.divider()

    st.markdown("### 📌 Navigation")

    page = st.radio(
        "Go to",
        [
            "🏠 Dashboard",
            "🔎 Diagnose Case",
            "📋 Case Explorer",
            "ℹ️ About NetSage AI"
        ],
        label_visibility="collapsed"
    )

    st.divider()

    st.markdown("### ⚙️ System Status")

    st.success("Evidence pipeline loaded")

    st.success("Rule checker loaded")

    st.success("AI diagnosis loaded")

    st.success("Explanation engine loaded")

    st.divider()

    st.caption(
        f"Total cases processed: {total_cases}"
    )

    st.caption(
        "NetSage AI • Cisco Packet Tracer"
    )


# ============================================================
# PAGE 1 — DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">
            <h1>🌐 NetSage AI</h1>
            <p>
                AI-Assisted Network Fault Diagnosis & Troubleshooting
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.title("📊 Network Overview")

    st.write(
        "A one-glance summary of the 30 Cisco Packet Tracer troubleshooting cases."
    )

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # METRICS
    # --------------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">📁 Total Cases</div>
                <div class="metric-number">{total_cases}</div>
                <div class="metric-description">
                    Network cases analyzed
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">🔴 Faults Detected</div>
                <div class="metric-number">{fail_count}</div>
                <div class="metric-description">
                    Cases with detected faults
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">🟢 Passed</div>
                <div class="metric-number">{pass_count}</div>
                <div class="metric-description">
                    Cases passing automated checks
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-title">🟠 Need Review</div>
                <div class="metric-number">{review_count}</div>
                <div class="metric-description">
                    Cases requiring more evidence
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # WHAT DOES THIS MEAN?
    # --------------------------------------------------------

    st.header("🧠 What does this mean?")

    a, b, c = st.columns(3)

    with a:
        st.error(
            f"🔴 {fail_count} cases contain a detected network fault."
        )

    with b:
        st.success(
            f"🟢 {pass_count} case(s) passed the automated checks."
        )

    with c:
        st.warning(
            f"🟠 {review_count} cases need additional evidence or review."
        )

    # --------------------------------------------------------
    # ISSUE TYPE DISTRIBUTION
    # --------------------------------------------------------

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    st.header("📊 Issue Type Distribution")

    st.write(
        "Shows which types of networking problems appear across the troubleshooting cases."
    )

    if "Category" in df.columns:

        category_counts = (
            df["Category"]
            .astype(str)
            .value_counts()
            .sort_values(ascending=True)
        )

        fig, ax = plt.subplots(figsize=(10, 5))

        ax.barh(
            category_counts.index,
            category_counts.values
        )

        ax.set_xlabel("Number of Cases")

        ax.set_ylabel("Issue Type")

        ax.set_title("Network Issue Types")

        ax.grid(
            axis="x",
            alpha=0.25
        )

        plt.tight_layout()

        st.pyplot(fig)

        plt.close(fig)

    # --------------------------------------------------------
    # STATUS DISTRIBUTION
    # --------------------------------------------------------

    st.header("📈 Case Status")

    status_counts = df["Status"].value_counts()

    fig, ax = plt.subplots(figsize=(8, 4))

    ax.bar(
        status_counts.index,
        status_counts.values
    )

    ax.set_ylabel("Number of Cases")

    ax.set_xlabel("Status")

    ax.set_title("Automated Diagnosis Status")

    ax.grid(
        axis="y",
        alpha=0.25
    )

    plt.tight_layout()

    st.pyplot(fig)

    plt.close(fig)

    # --------------------------------------------------------
    # AI VS HUMAN AGREEMENT
    # --------------------------------------------------------

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    st.header("🤝 AI vs Human Agreement")

    st.write(
        "Human review allows a network expert to confirm, modify, or reject the AI diagnosis."
    )

    reviewed = len(st.session_state.human_reviews)

    accepted = sum(
        1
        for value in st.session_state.human_reviews.values()
        if value["decision"] == "Accept"
    )

    rejected = sum(
        1
        for value in st.session_state.human_reviews.values()
        if value["decision"] == "Reject"
    )

    modified = sum(
        1
        for value in st.session_state.human_reviews.values()
        if value["decision"] == "Needs Modification"
    )

    if reviewed == 0:

        st.info(
            "👤 No human reviews recorded yet. Go to 'Diagnose Case' and review a case."
        )

    else:

        agreement_percentage = (
            accepted / reviewed * 100
        )

        h1, h2, h3, h4 = st.columns(4)

        with h1:
            st.metric(
                "Cases Reviewed",
                reviewed
            )

        with h2:
            st.metric(
                "AI Accepted",
                accepted
            )

        with h3:
            st.metric(
                "Rejected",
                rejected
            )

        with h4:
            st.metric(
                "Needs Modification",
                modified
            )

        st.progress(
            agreement_percentage / 100
        )

        st.write(
            f"**AI-Human Agreement: {agreement_percentage:.1f}%**"
        )

    # --------------------------------------------------------
    # PIPELINE
    # --------------------------------------------------------

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    st.header("⚙️ How NetSage AI Works")

    p1, p2, p3, p4 = st.columns(4)

    with p1:
        st.markdown(
            """
            ### 1️⃣ Evidence

            Collects network evidence from Cisco Packet Tracer troubleshooting cases.
            """
        )

    with p2:
        st.markdown(
            """
            ### 2️⃣ Rule Checking

            Deterministic rules identify configuration problems.
            """
        )

    with p3:
        st.markdown(
            """
            ### 3️⃣ AI Diagnosis

            Converts technical findings into understandable diagnoses and explanations.
            """
        )

    with p4:
        st.markdown(
            """
            ### 4️⃣ Human Review

            A network expert can accept, reject, or modify the diagnosis.
            """

        )


# ============================================================
# PAGE 2 — DIAGNOSE CASE
# ============================================================

elif page == "🔎 Diagnose Case":

    st.title("🔎 Diagnose a Network Case")

    st.write(
        "Select a case to view its evidence, diagnosis, explanation and recommended solution."
    )

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    case_ids = df["Case ID"].astype(str).tolist()

    selected_case = st.selectbox(
        "Select Case ID",
        case_ids
    )

    case = df[
        df["Case ID"].astype(str) == selected_case
    ].iloc[0]

    st.markdown(
        f"## 📌 {selected_case}"
    )

    # --------------------------------------------------------
    # CASE INFORMATION
    # --------------------------------------------------------

    i1, i2, i3 = st.columns(3)

    with i1:
        st.metric(
            "Category",
            str(case.get("Category", "N/A"))
        )

    with i2:
        st.metric(
            "Rule",
            str(case.get("Rule", "N/A"))
        )

    with i3:
        status = str(case.get("Status", "N/A"))

        if status == "FAIL":
            st.error(f"Status: {status}")

        elif status == "PASS":
            st.success(f"Status: {status}")

        else:
            st.warning(f"Status: {status}")

    # --------------------------------------------------------
    # EXPECTED FAULT
    # --------------------------------------------------------

    st.subheader("🎯 Expected Fault")

    st.info(
        str(case.get("Expected Fault", "Not available"))
    )

    # --------------------------------------------------------
    # STATUS
    # --------------------------------------------------------

    if status == "FAIL":

        st.markdown(
            '<div class="status-fail">🔴 Network fault detected</div>',
            unsafe_allow_html=True
        )

    elif status == "PASS":

        st.markdown(
            '<div class="status-pass">🟢 No network fault detected</div>',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="status-review">🟠 Additional evidence or review required</div>',
            unsafe_allow_html=True
        )

    # --------------------------------------------------------
    # EVIDENCE FINDING
    # --------------------------------------------------------

    st.subheader("🔍 Evidence Finding")

    finding = str(
        case.get(
            "Finding",
            case.get("Finding_diagnosis", "No finding available")
        )
    )

    st.write(finding)

    # --------------------------------------------------------
    # DIAGNOSIS
    # --------------------------------------------------------

    st.subheader("🧠 AI Diagnosis")

    diagnosis = str(
        case.get(
            "Diagnosis",
            "No diagnosis available"
        )
    )

    st.markdown(
        f"""
        <div class="diagnosis-box">
            <strong>{diagnosis}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # EXPLANATION
    # --------------------------------------------------------

    st.subheader("💡 Explanation")

    explanation = str(
        case.get(
            "Explanation",
            "No explanation available."
        )
    )

    st.write(explanation)

    # --------------------------------------------------------
    # RECOMMENDED SOLUTION
    # --------------------------------------------------------

    st.subheader("🛠️ Recommended Solution")

    solution = str(
        case.get(
            "Recommended Solution",
            "No recommended solution available."
        )
    )

    st.markdown(
        f"""
        <div class="solution-box">
            <strong>{solution}</strong>
        </div>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------------
    # HUMAN REVIEW
    # --------------------------------------------------------

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    st.header("👤 Human Review")

    st.write(
        "Review the AI diagnosis before considering it a final decision."
    )

    existing_review = st.session_state.human_reviews.get(
        selected_case,
        None
    )

    default_decision = (
        existing_review["decision"]
        if existing_review
        else "Not Reviewed"
    )

    decision_options = [
        "Not Reviewed",
        "Accept",
        "Needs Modification",
        "Reject"
    ]

    decision = st.radio(
        "Human decision",
        decision_options,
        index=decision_options.index(default_decision),
        horizontal=True
    )

    reviewer_comment = st.text_area(
        "Reviewer Comment",
        value=(
            existing_review["comment"]
            if existing_review
            else ""
        ),
        placeholder="Enter your reasoning or correction here..."
    )

    if st.button(
        "💾 Save Human Review",
        type="primary"
    ):

        if decision == "Not Reviewed":

            st.warning(
                "Please select Accept, Needs Modification, or Reject."
            )

        else:

            st.session_state.human_reviews[
                selected_case
            ] = {
                "decision": decision,
                "comment": reviewer_comment
            }

            st.success(
                f"Human review saved for {selected_case}: {decision}"
            )

    # Show current review

    if selected_case in st.session_state.human_reviews:

        review = st.session_state.human_reviews[selected_case]

        st.info(
            f"Current Human Decision: **{review['decision']}**"
        )

        if review["comment"]:

            st.write(
                f"Reviewer Comment: {review['comment']}"
            )


# ============================================================
# PAGE 3 — CASE EXPLORER
# ============================================================

elif page == "📋 Case Explorer":

    st.title("📋 Case Explorer")

    st.write(
        "Search and explore all network troubleshooting cases."
    )

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # FILTERS
    # --------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        search_text = st.text_input(
            "🔎 Search",
            placeholder="NET-001, VLAN, gateway..."
        )

    with col2:

        categories = ["All"]

        if "Category" in df.columns:

            categories += sorted(
                df["Category"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

        selected_category = st.selectbox(
            "Category",
            categories
        )

    with col3:

        statuses = [
            "All",
            "PASS",
            "FAIL",
            "NOT_CHECKED"
        ]

        selected_status = st.selectbox(
            "Status",
            statuses
        )

    filtered_df = df.copy()

    # Search

    if search_text:

        mask = filtered_df.astype(str).apply(
            lambda row: row.str.contains(
                search_text,
                case=False,
                na=False
            ).any(),
            axis=1
        )

        filtered_df = filtered_df[mask]

    # Category

    if selected_category != "All":

        filtered_df = filtered_df[
            filtered_df["Category"].astype(str)
            == selected_category
        ]

    # Status

    if selected_status != "All":

        filtered_df = filtered_df[
            filtered_df["Status"].astype(str)
            == selected_status
        ]

    st.write(
        f"Showing **{len(filtered_df)}** case(s)"
    )

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    columns_to_show = [
        "Case ID",
        "Category",
        "Expected Fault",
        "Status",
        "Diagnosis"
    ]

    available_columns = [
        column
        for column in columns_to_show
        if column in filtered_df.columns
    ]

    st.dataframe(
        filtered_df[available_columns],
        use_container_width=True,
        hide_index=True
    )

    # --------------------------------------------------------
    # DOWNLOAD
    # --------------------------------------------------------

    csv_data = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        "⬇️ Download Filtered Cases",
        csv_data,
        "netsage_filtered_cases.csv",
        "text/csv"
    )


# ============================================================
# PAGE 4 — ABOUT NETSAGE AI
# ============================================================

elif page == "ℹ️ About NetSage AI":

    st.title("ℹ️ About NetSage AI")

    st.write(
        "AI-assisted network fault diagnosis and troubleshooting system."
    )

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    # --------------------------------------------------------
    # PROJECT OVERVIEW
    # --------------------------------------------------------

    st.header("🌐 What is NetSage AI?")

    st.write(
        """
        NetSage AI is a network troubleshooting system designed
        to analyze Cisco Packet Tracer network cases and identify
        configuration problems.
        """
    )

    st.write(
        """
        The system combines evidence extraction, deterministic
        rule checking, AI-style diagnosis, human-readable
        explanations and human review.
        """
    )

    # --------------------------------------------------------
    # PROJECT FLOW
    # --------------------------------------------------------

    st.header("⚙️ System Pipeline")

    st.write(
        "The complete workflow of NetSage AI is:"
    )

    flow = [
        (
            "1️⃣",
            "Packet Tracer Cases",
            "Network troubleshooting cases are created in Cisco Packet Tracer."
        ),
        (
            "2️⃣",
            "Evidence Extraction",
            "Important network configuration evidence is collected."
        ),
        (
            "3️⃣",
            "Rule Checking",
            "Deterministic rules check VLAN, gateway, DHCP, DNS, routing, ACL, NAT and other configurations."
        ),
        (
            "4️⃣",
            "AI Diagnosis",
            "Technical findings are converted into understandable diagnoses."
        ),
        (
            "5️⃣",
            "Explanation",
            "The system explains the problem in simple human-readable language."
        ),
        (
            "6️⃣",
            "Human Review",
            "A human reviewer can accept, reject or modify the diagnosis."
        )
    ]

    for number, title, description in flow:

        st.markdown(
            f"### {number} {title}"
        )

        st.write(description)

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    st.header("✨ Key Features")

    features = [
        "Evidence-based network troubleshooting",
        "Rule-based fault detection",
        "AI-assisted diagnosis",
        "Human-readable explanations",
        "Recommended troubleshooting solutions",
        "Human review and validation",
        "Case filtering and exploration",
        "Dashboard-based visualization"
    ]

    for feature in features:

        st.write(
            f"✅ {feature}"
        )

    # --------------------------------------------------------
    # TECHNOLOGY
    # --------------------------------------------------------

    st.header("🛠️ Technologies Used")

    t1, t2, t3, t4 = st.columns(4)

    with t1:
        st.info("🐍 Python")

    with t2:
        st.info("📊 Pandas")

    with t3:
        st.info("🎨 Streamlit")

    with t4:
        st.info("🌐 Cisco Packet Tracer")

    # --------------------------------------------------------
    # PROJECT VALUE
    # --------------------------------------------------------

    st.header("🎯 Project Objective")

    st.write(
        """
        The main objective of NetSage AI is to reduce the difficulty
        of network troubleshooting by transforming technical network
        evidence into understandable fault diagnoses and actionable
        troubleshooting guidance.
        """
    )

    st.markdown('<div class="section-line"></div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="footer">
            NetSage AI • AI-Assisted Network Fault Diagnosis & Troubleshooting<br>
            Cisco Packet Tracer • Evidence-Based Analysis • Rule Checking • AI Diagnosis • Human Review
        </div>
        """,
        unsafe_allow_html=True
    )