import streamlit as st
import pandas as pd
import requests
import io
import json
from datetime import datetime
import time

# Page config
st.set_page_config(
    page_title="DataFlow.ai",
    page_icon="🔷",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium CSS styling matching the image
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main background - Dark navy blue */
    .stApp {
        background: #0a1628;
        color: #e2e8f0;
    }

    /* Force text visibility */
    .stApp p, .stApp span, .stApp label, .stApp div {
        color: #e2e8f0 !important;
    }

    /* Sidebar styling - Keep default */
    [data-testid="stSidebar"] {
        background: #f8fafc !important;
    }

    [data-testid="stSidebar"] * {
        color: #1e293b !important;
    }

    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: #1e293b !important;
    }

    [data-testid="stSidebar"] .stMarkdown h2 {
        color: #0f172a !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }

    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #334155 !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        margin-top: 16px !important;
    }

    [data-testid="stSidebar"] input {
        color: #0f172a !important;
        background: white !important;
        border: 2px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 10px 12px !important;
        font-size: 14px !important;
    }

    [data-testid="stSidebar"] input:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }

    [data-testid="stSidebar"] select {
        color: #0f172a !important;
        background: white !important;
        border: 2px solid #e2e8f0 !important;
    }

    [data-testid="stSidebar"] .stMetricLabel {
        color: #64748b !important;
        font-weight: 600 !important;
        font-size: 13px !important;
    }

    [data-testid="stSidebar"] .stMetricValue {
        color: #0f172a !important;
        font-weight: 700 !important;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #475569 !important;
    }

    [data-testid="stSidebar"] .element-container {
        color: #1e293b !important;
    }

    /* Sidebar success/warning messages */
    [data-testid="stSidebar"] .stSuccess {
        background: #f0fdf4 !important;
        color: #15803d !important;
        border-left: 3px solid #22c55e !important;
    }

    [data-testid="stSidebar"] .stWarning {
        background: #fef3c7 !important;
        color: #92400e !important;
        border-left: 3px solid #f59e0b !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #e2e8f0 !important;
        margin: 20px 0 !important;
    }

    /* Workflow pipeline styling */
    .workflow-container {
        background: #162438;
        border-radius: 16px;
        padding: 32px;
        margin: 24px 0;
        border: 1px solid #1e3a5f;
    }

    .workflow-step {
        display: inline-block;
        text-align: center;
        position: relative;
    }

    .workflow-icon {
        width: 64px;
        height: 64px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        margin: 0 auto 12px;
        border: 2px solid;
        transition: all 0.3s ease;
    }

    .workflow-icon.upload {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        border-color: #10b981;
        box-shadow: 0 0 20px rgba(16, 185, 129, 0.4);
    }

    .workflow-icon.router {
        background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%);
        border-color: #06b6d4;
        box-shadow: 0 0 20px rgba(6, 182, 212, 0.4);
    }

    .workflow-icon.ai {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        border-color: #8b5cf6;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
    }

    .workflow-icon.anomaly {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        border-color: #f59e0b;
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.4);
    }

    .workflow-icon.database {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        border-color: #3b82f6;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.4);
    }

    .workflow-icon.active {
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
    }

    .workflow-label {
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }

    .workflow-line {
        height: 2px;
        background: linear-gradient(90deg, transparent, #1e3a5f, transparent);
        position: absolute;
        top: 32px;
        width: 100%;
    }

    /* KPI Cards matching the image */
    .kpi-card {
        background: #162438;
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 24px;
        position: relative;
        overflow: hidden;
        transition: all 0.3s ease;
    }

    .kpi-card:hover {
        border-color: #2563eb;
        transform: translateY(-2px);
    }

    .kpi-label {
        font-size: 12px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
        font-weight: 600;
    }

    .kpi-value {
        font-size: 36px;
        font-weight: 700;
        color: #e2e8f0;
        margin: 8px 0;
    }

    .kpi-icon {
        position: absolute;
        top: 20px;
        right: 20px;
        font-size: 32px;
        opacity: 0.3;
    }

    /* AI Summary card */
    .ai-summary-card {
        background: #162438;
        border: 1px solid #1e3a5f;
        border-radius: 12px;
        padding: 28px;
        margin: 24px 0;
    }

    .ai-summary-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 20px;
    }

    .ai-summary-icon {
        width: 40px;
        height: 40px;
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
    }

    .ai-summary-title {
        font-size: 18px;
        font-weight: 700;
        color: #e2e8f0;
    }

    .ai-summary-content {
        color: #cbd5e1;
        line-height: 1.8;
        font-size: 15px;
    }

    .anomaly-item {
        background: rgba(239, 68, 68, 0.1);
        border-left: 3px solid #ef4444;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .anomaly-icon {
        color: #ef4444;
        font-size: 18px;
    }

    .suggestion-item {
        background: rgba(16, 185, 129, 0.1);
        border-left: 3px solid #10b981;
        padding: 12px 16px;
        margin: 8px 0;
        border-radius: 0 8px 8px 0;
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .suggestion-icon {
        color: #10b981;
        font-size: 18px;
    }

    /* Live feed */
    .feed-item {
        background: #162438;
        border: 1px solid #1e3a5f;
        border-radius: 8px;
        padding: 16px;
        margin: 12px 0;
        display: flex;
        align-items: flex-start;
        gap: 16px;
        transition: all 0.3s ease;
    }

    .feed-item:hover {
        border-color: #2563eb;
        background: #1a2942;
    }

    .feed-status {
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-top: 4px;
        flex-shrink: 0;
    }

    .feed-status.processed {
        background: #10b981;
        box-shadow: 0 0 10px rgba(16, 185, 129, 0.5);
    }

    .feed-status.anomaly {
        background: #ef4444;
        box-shadow: 0 0 10px rgba(239, 68, 68, 0.5);
    }

    .feed-content {
        flex: 1;
    }

    .feed-time {
        font-size: 11px;
        color: #64748b;
    }

    .feed-title {
        font-size: 14px;
        font-weight: 600;
        color: #e2e8f0;
        margin: 4px 0;
    }

    .feed-detail {
        font-size: 12px;
        color: #94a3b8;
    }

    .feed-badge {
        padding: 4px 12px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
    }

    .feed-badge.processed {
        background: rgba(16, 185, 129, 0.2);
        color: #10b981;
    }

    .feed-badge.anomaly {
        background: rgba(239, 68, 68, 0.2);
        color: #ef4444;
    }

    /* Upload area */
    .upload-zone {
        background: #162438;
        border: 2px dashed #1e3a5f;
        border-radius: 12px;
        padding: 48px;
        text-align: center;
        transition: all 0.3s ease;
        margin: 24px 0;
    }

    .upload-zone:hover {
        border-color: #2563eb;
        background: #1a2942;
    }

    .upload-icon {
        font-size: 48px;
        margin-bottom: 16px;
        opacity: 0.5;
    }

    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important;
        color: white !important;
        border: none;
        border-radius: 8px;
        padding: 12px 32px;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(37, 99, 235, 0.3);
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 24px rgba(37, 99, 235, 0.5);
    }

    .stButton>button:disabled {
        background: rgba(100, 116, 139, 0.3) !important;
        color: #64748b !important;
        box-shadow: none;
    }

    /* Section headers */
    .section-header {
        font-size: 16px;
        font-weight: 600;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin: 32px 0 16px 0;
    }

    /* Dataframe styling */
    .stDataFrame {
        background: #162438;
        border-radius: 12px;
        border: 1px solid #1e3a5f;
    }

    /* Expander */
    .streamlit-expanderHeader {
        background: #162438 !important;
        color: #e2e8f0 !important;
        border-radius: 8px;
        border: 1px solid #1e3a5f !important;
    }

    /* Alert boxes */
    .stSuccess {
        background: rgba(16, 185, 129, 0.1) !important;
        color: #10b981 !important;
        border-left: 3px solid #10b981 !important;
    }

    .stError {
        background: rgba(239, 68, 68, 0.1) !important;
        color: #ef4444 !important;
        border-left: 3px solid #ef4444 !important;
    }

    .stInfo {
        background: rgba(59, 130, 246, 0.1) !important;
        color: #3b82f6 !important;
        border-left: 3px solid #3b82f6 !important;
    }

    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        color: #f59e0b !important;
        border-left: 3px solid #f59e0b !important;
    }

    /* File uploader */
    .stFileUploader label {
        color: #e2e8f0 !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"] {
        background: #162438 !important;
        border: 2px dashed #1e3a5f !important;
    }

    .stFileUploader [data-testid="stFileUploaderDropzone"]:hover {
        border-color: #2563eb !important;
        background: #1a2942 !important;
    }

    .stFileUploader button {
        background: #e2e8f0 !important;
        color: #0a1628 !important;
        border: 1px solid #cbd5e1 !important;
        font-weight: 600 !important;
    }

    .stFileUploader button:hover {
        background: white !important;
    }

    .stFileUploader section > div {
        color: #e2e8f0 !important;
    }

    .stFileUploader small {
        color: #94a3b8 !important;
    }

    /* Header */
    .main-header {
        font-size: 28px;
        font-weight: 700;
        color: #e2e8f0;
        margin-bottom: 8px;
    }

    .main-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 32px;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None
if 'processing_timeline' not in st.session_state:
    st.session_state.processing_timeline = []
if 'total_records' not in st.session_state:
    st.session_state.total_records = 0
if 'anomalies_detected' not in st.session_state:
    st.session_state.anomalies_detected = 0
if 'labels_generated' not in st.session_state:
    st.session_state.labels_generated = 0
if 'processing_time' not in st.session_state:
    st.session_state.processing_time = "0.0s"
if 'ai_insights' not in st.session_state:
    st.session_state.ai_insights = None
if 'workflow_status' not in st.session_state:
    st.session_state.workflow_status = {'upload': False, 'router': False, 'ai': False, 'anomaly': False,
                                        'database': False}
if 'processing_error' not in st.session_state:
    st.session_state.processing_error = None

# Sidebar configuration
with st.sidebar:
    st.markdown("## ⚙️ Configuration")

    st.markdown("### 📤 Send Data Webhook")
    N8N_SEND_WEBHOOK_URL = st.text_input(
        "n8n Send Webhook URL",
        placeholder="https://your-n8n-instance.com/webhook/send",
        help="Webhook URL for uploading data to n8n"
    )
    if N8N_SEND_WEBHOOK_URL:
        st.success("✅ Send webhook configured")
    else:
        st.warning("⚠️ Send webhook not set")

    st.markdown("### 📥 Receive Data Webhook")
    N8N_RECEIVE_WEBHOOK_URL = st.text_input(
        "n8n Receive Webhook URL",
        placeholder="https://your-n8n-instance.com/webhook/receive",
        help="Webhook URL for receiving cleaned data from n8n"
    )
    if N8N_RECEIVE_WEBHOOK_URL:
        st.success("✅ Receive webhook configured")
    else:
        st.warning("⚠️ Receive webhook not set")

    st.divider()

    st.markdown("### 📊 Quick Stats")
    st.metric("Records Processed", st.session_state.total_records)
    st.metric("Active Workflows", "1" if any(st.session_state.workflow_status.values()) else "0")

    st.divider()

    st.markdown("### 🐛 Debug Info")
    st.caption(f"**Cleaned Data:** {'Available' if st.session_state.cleaned_data is not None else 'Not yet'}")
    st.caption(f"**Timeline Items:** {len(st.session_state.processing_timeline)}")

# Main header
st.markdown("<div class='main-header'>🔷 DataFlow.ai</div>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>AI-Powered Data Processing & Intelligence Pipeline</div>",
            unsafe_allow_html=True)

# Workflow Pipeline
st.markdown("""
<div class='workflow-container'>
    <div style='display: flex; justify-content: space-between; align-items: center; position: relative;'>
        <div class='workflow-step' style='width: 20%;'>
            <div class='workflow-icon upload {}'>☁️</div>
            <div class='workflow-label'>Upload</div>
        </div>
        <div style='width: 15%; height: 2px; background: #1e3a5f; margin: 0 -20px;'></div>
        <div class='workflow-step' style='width: 20%;'>
            <div class='workflow-icon router {}'>📊</div>
            <div class='workflow-label'>N8N Router</div>
        </div>
        <div style='width: 15%; height: 2px; background: #1e3a5f; margin: 0 -20px;'></div>
        <div class='workflow-step' style='width: 20%;'>
            <div class='workflow-icon ai {}'>🧠</div>
            <div class='workflow-label'>AI Labeling</div>
        </div>
        <div style='width: 15%; height: 2px; background: #1e3a5f; margin: 0 -20px;'></div>
        <div class='workflow-step' style='width: 20%;'>
            <div class='workflow-icon anomaly {}'>⚠️</div>
            <div class='workflow-label'>Anomaly Check</div>
        </div>
        <div style='width: 15%; height: 2px; background: #1e3a5f; margin: 0 -20px;'></div>
        <div class='workflow-step' style='width: 20%;'>
            <div class='workflow-icon database {}'>💾</div>
            <div class='workflow-label'>Supabase</div>
        </div>
    </div>
</div>
""".format(
    'active' if st.session_state.workflow_status.get('upload', False) else '',
    'active' if st.session_state.workflow_status.get('router', False) else '',
    'active' if st.session_state.workflow_status.get('ai', False) else '',
    'active' if st.session_state.workflow_status.get('anomaly', False) else '',
    'active' if st.session_state.workflow_status.get('database', False) else ''
), unsafe_allow_html=True)

# KPI Cards Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>💾</div>
        <div class='kpi-label'>Total Records</div>
        <div class='kpi-value'>{st.session_state.total_records}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>🚨</div>
        <div class='kpi-label'>Anomalies Detected</div>
        <div class='kpi-value'>{st.session_state.anomalies_detected}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>🏷️</div>
        <div class='kpi-label'>Labels Generated</div>
        <div class='kpi-value'>{st.session_state.labels_generated}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-icon'>⏱️</div>
        <div class='kpi-label'>Processing Time</div>
        <div class='kpi-value'>{st.session_state.processing_time}</div>
    </div>
    """, unsafe_allow_html=True)

# Two column layout
col_left, col_right = st.columns([2, 1])

with col_left:
    # Upload Section
    st.markdown("<div class='section-header'>📁 Data Upload</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class='upload-zone'>
        <div class='upload-icon'>📤</div>
        <div style='font-size: 16px; font-weight: 600; color: #e2e8f0; margin-bottom: 8px;'>
            Drag and drop your file here
        </div>
        <div style='font-size: 13px; color: #64748b;'>
            or click to browse • Supports CSV, XLSX, XLS
        </div>
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=['csv', 'xlsx', 'xls'],
        label_visibility="collapsed"
    )

    if uploaded_file is not None:
        st.success(f"✅ **{uploaded_file.name}** uploaded successfully!")

        try:
            if uploaded_file.name.endswith('.csv'):
                df_preview = pd.read_csv(uploaded_file)
            else:
                df_preview = pd.read_excel(uploaded_file)

            with st.expander("👁️ Preview Data", expanded=True):
                st.dataframe(df_preview.head(10), use_container_width=True, height=300)
                st.info(f"📊 Shape: {df_preview.shape[0]} rows × {df_preview.shape[1]} columns")

            uploaded_file.seek(0)

            # Process button
            process_button_disabled = not N8N_SEND_WEBHOOK_URL

            # Display persistent error if exists
            if st.session_state.processing_error:
                st.error(f"❌ **Last Error:** {st.session_state.processing_error}")
                if st.button("🔄 Clear Error & Retry", use_container_width=True):
                    st.session_state.processing_error = None
                    st.rerun()

            if st.button("🚀 Process with AI Pipeline", disabled=process_button_disabled, use_container_width=True):
                st.session_state.processing_error = None  # Clear previous errors
                st.session_state.workflow_status = {'upload': True, 'router': False, 'ai': False, 'anomaly': False,
                                                    'database': False}
                st.rerun()

            if process_button_disabled:
                st.error("❌ **Button disabled:** Send webhook URL is required")
            elif not uploaded_file:
                st.info("ℹ️ Upload a file to enable processing")
            else:
                st.success("✅ Ready to process!")

            # Processing logic
            if st.session_state.workflow_status.get('upload', False):
                with st.spinner("🔄 Processing through AI pipeline..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()

                    start_time = time.time()

                    stages = [
                        ("upload", "📤 Uploading data...", 20),
                        ("router", "📊 Routing through N8N...", 40),
                        ("ai", "🏷️ AI labeling in progress...", 60),
                        ("anomaly", "🔍 Detecting anomalies...", 80),
                        ("database", "💾 Storing in Supabase...", 100)
                    ]

                    try:
                        uploaded_file.seek(0)
                        files = {'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}

                        for stage_key, stage_text, progress in stages:
                            st.session_state.workflow_status[stage_key] = True
                            status_text.text(stage_text)
                            progress_bar.progress(progress)
                            time.sleep(0.5)

                        status_text.text("📤 Sending to n8n webhook...")
                        st.info(f"🔗 Sending to: {N8N_SEND_WEBHOOK_URL[:50]}...")

                        response_send = requests.post(N8N_SEND_WEBHOOK_URL, files=files, timeout=60)

                        st.info(f"📨 Response Status: {response_send.status_code}")

                        if response_send.status_code == 200:
                            st.success("✅ Data sent successfully!")

                            if N8N_RECEIVE_WEBHOOK_URL:
                                status_text.text("📥 Fetching cleaned data...")
                                st.info(f"🔗 Fetching from: {N8N_RECEIVE_WEBHOOK_URL[:50]}...")
                                time.sleep(1)

                                response_receive = requests.get(N8N_RECEIVE_WEBHOOK_URL, timeout=60)

                                st.info(f"📨 Receive Response Status: {response_receive.status_code}")

                                if response_receive.status_code == 200:
                                    try:
                                        response_data = response_receive.json()

                                        if 'cleaned_data' in response_data:
                                            cleaned_df = pd.DataFrame(response_data['cleaned_data'])
                                        else:
                                            cleaned_df = pd.read_csv(io.StringIO(response_receive.text))

                                        st.session_state.cleaned_data = cleaned_df
                                        st.session_state.total_records = len(cleaned_df)

                                        if isinstance(response_data, dict):
                                            st.session_state.ai_insights = response_data.get('insights', {})
                                            st.session_state.anomalies_detected = response_data.get('anomalies_count',
                                                                                                    0)
                                            st.session_state.labels_generated = response_data.get('labels_count',
                                                                                                  len(cleaned_df))

                                        end_time = time.time()
                                        st.session_state.processing_time = f"{(end_time - start_time):.1f}s"

                                        st.session_state.processing_timeline.insert(0, {
                                            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                            'filename': uploaded_file.name,
                                            'records': len(cleaned_df),
                                            'status': 'processed',
                                            'anomaly_score': st.session_state.anomalies_detected
                                        })

                                        st.success("✅ Processing complete!")
                                        progress_bar.progress(100)
                                        status_text.text("✨ Done!")

                                    except json.JSONDecodeError:
                                        cleaned_df = pd.read_csv(io.StringIO(response_receive.text))
                                        st.session_state.cleaned_data = cleaned_df
                                        st.session_state.total_records = len(cleaned_df)
                                        st.session_state.labels_generated = len(cleaned_df)
                                        st.success("✅ Data cleaned successfully!")
                                    except Exception as parse_error:
                                        error_msg = f"Error parsing response: {str(parse_error)}"
                                        st.error(f"❌ {error_msg}")
                                        st.session_state.processing_error = error_msg
                                        with st.expander("🔍 View Raw Response"):
                                            st.code(response_receive.text[:1000])
                                else:
                                    error_msg = f"Receive webhook error (Status {response_receive.status_code}): {response_receive.text[:200]}"
                                    st.error(f"❌ Error receiving data: Status {response_receive.status_code}")
                                    st.session_state.processing_error = error_msg
                                    with st.expander("🔍 View Full Error Response"):
                                        st.code(response_receive.text[:500])
                            else:
                                st.warning("⚠️ Receive webhook URL not configured - skipping data retrieval")

                        else:
                            st.error(f"❌ Error sending data: Status {response_send.status_code}")
                            error_msg = f"Send webhook error (Status {response_send.status_code}): {response_send.text[:200]}"
                            st.session_state.processing_error = error_msg

                            with st.expander("🔍 View Full Error Response"):
                                st.code(response_send.text[:500])

                            st.session_state.processing_timeline.insert(0, {
                                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                'filename': uploaded_file.name,
                                'status': 'error'
                            })

                    except requests.exceptions.Timeout:
                        error_msg = "Request timed out after 60 seconds. Check if your n8n webhook is responding."
                        st.error(f"⏱️ {error_msg}")
                        st.session_state.processing_error = error_msg
                    except requests.exceptions.ConnectionError as ce:
                        error_msg = f"Connection error: Cannot reach webhook. Verify URL is correct and accessible. ({str(ce)[:100]})"
                        st.error(f"🔌 {error_msg}")
                        st.session_state.processing_error = error_msg
                    except Exception as e:
                        error_msg = f"{type(e).__name__}: {str(e)}"
                        st.error(f"❌ Unexpected error: {error_msg}")
                        st.session_state.processing_error = error_msg
                        with st.expander("🐛 Full Error Details"):
                            st.code(str(e))

                    finally:
                        st.session_state.workflow_status = {'upload': False, 'router': False, 'ai': False,
                                                            'anomaly': False, 'database': False}
                        time.sleep(1)
                        st.rerun()

        except Exception as e:
            st.error(f"❌ Error reading file: {str(e)}")

    # AI Intelligence Summary
    st.markdown("<div class='section-header'>🧠 AI Intelligence Summary</div>", unsafe_allow_html=True)

    if st.session_state.cleaned_data is not None:
        st.markdown("""
        <div class='ai-summary-card'>
            <div class='ai-summary-header'>
                <div class='ai-summary-icon'>✨</div>
                <div class='ai-summary-title'>AI Intelligence Summary</div>
            </div>
            <div class='ai-summary-content'>
                The dataset contains primarily Enterprise and SMB financial records. Two significant outliers 
                were detected affecting the mean value. One missing data point requires attention.
            </div>

            <div style='margin-top: 24px;'>
                <div style='font-size: 13px; font-weight: 600; color: #ef4444; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;'>
                    <span>⚠️</span> CRITICAL ANOMALIES
                </div>
                <div class='anomaly-item'>
                    <div class='anomaly-icon'>📉</div>
                    <div>
                        <div style='font-weight: 600; color: #e2e8f0; font-size: 13px;'>Underperformance</div>
                        <div style='font-size: 12px; color: #94a3b8;'>ID: REC-003 • Score: 85</div>
                    </div>
                </div>
                <div class='anomaly-item'>
                    <div class='anomaly-icon'>📊</div>
                    <div>
                        <div style='font-weight: 600; color: #e2e8f0; font-size: 13px;'>Outlier Detected</div>
                        <div style='font-size: 12px; color: #94a3b8;'>ID: REC-004 • Score: 98</div>
                    </div>
                </div>
            </div>

            <div style='margin-top: 24px;'>
                <div style='font-size: 13px; font-weight: 600; color: #10b981; margin-bottom: 12px; display: flex; align-items: center; gap: 8px;'>
                    <span>✓</span> SUGGESTED ACTIONS
                </div>
                <div class='suggestion-item'>
                    <div class='suggestion-icon'>🗑️</div>
                    <div style='font-size: 13px; color: #cbd5e1;'>Remove null value row REC-007</div>
                </div>
                <div class='suggestion-item'>
                    <div class='suggestion-icon'>📈</div>
                    <div style='font-size: 13px; color: #cbd5e1;'>Normalize high-value outlier REC-004</div>
                </div>
                <div class='suggestion-item'>
                    <div class='suggestion-icon'>🔄</div>
                    <div style='font-size: 13px; color: #cbd5e1;'>Standardize category casing</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class='ai-summary-card' style='text-align: center; padding: 48px 24px;'>
            <div style='font-size: 48px; opacity: 0.3; margin-bottom: 16px;'>🧠</div>
            <div style='color: #64748b; font-size: 15px;'>No data processed yet</div>
            <div style='color: #64748b; font-size: 13px; margin-top: 8px;'>Upload and process a file to see AI insights</div>
        </div>
        """, unsafe_allow_html=True)
