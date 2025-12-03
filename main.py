import streamlit as st
import pandas as pd
import requests
import io

# App title
st.title("📊 Data Cleaning App")
st.write("Upload your CSV or Excel file to clean and validate your data")

# Initialize session state for cleaned data
if 'cleaned_data' not in st.session_state:
    st.session_state.cleaned_data = None
if 'original_filename' not in st.session_state:
    st.session_state.original_filename = None

# n8n webhook URL (replace with your actual webhook URL)
N8N_WEBHOOK_URL = st.text_input(
    "n8n Webhook URL", 
    placeholder="https://your-n8n-instance.com/webhook/your-webhook-id",
    help="Enter your n8n webhook URL"
)

st.divider()

# File upload section
st.subheader("1️⃣ Upload Your Data")
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file",
    type=['csv', 'xlsx', 'xls'],
    help="Only CSV and Excel files are supported"
)

# Upload and process button
if uploaded_file is not None:
    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully!")
    
    # Show file preview
    try:
        if uploaded_file.name.endswith('.csv'):
            df_preview = pd.read_csv(uploaded_file)
        else:
            df_preview = pd.read_excel(uploaded_file)
        
        st.write("**Preview (first 5 rows):**")
        st.dataframe(df_preview.head(), use_container_width=True)
        
        # Reset file pointer for sending to n8n
        uploaded_file.seek(0)
        
    except Exception as e:
        st.error(f"Error reading file: {str(e)}")
        uploaded_file = None

# Process button
if st.button("🚀 Send to n8n for Cleaning", disabled=(uploaded_file is None or not N8N_WEBHOOK_URL)):
    if uploaded_file is not None and N8N_WEBHOOK_URL:
        with st.spinner("🔄 Sending data to n8n for cleaning and validation..."):
            try:
                # Reset file pointer
                uploaded_file.seek(0)
                
                # Prepare file for sending
                files = {
                    'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                }
                
                # Send to n8n webhook
                response = requests.post(N8N_WEBHOOK_URL, files=files, timeout=60)
                
                if response.status_code == 200:
                    # Try to parse the response as CSV
                    try:
                        # Assume n8n returns cleaned CSV data
                        cleaned_df = pd.read_csv(io.StringIO(response.text))
                        st.session_state.cleaned_data = cleaned_df
                        st.session_state.original_filename = uploaded_file.name
                        st.success("✅ Data cleaned successfully!")
                        
                        # Show cleaned data preview
                        st.write("**Cleaned Data Preview:**")
                        st.dataframe(cleaned_df.head(10), use_container_width=True)
                        st.info(f"📊 Total rows: {len(cleaned_df)} | Columns: {len(cleaned_df.columns)}")
                        
                    except Exception as e:
                        st.error(f"Error parsing cleaned data: {str(e)}")
                        st.write("**Raw Response:**")
                        st.code(response.text[:500])
                else:
                    st.error(f"❌ Error from n8n: Status code {response.status_code}")
                    st.write(response.text[:500])
                    
            except requests.exceptions.Timeout:
                st.error("⏱️ Request timed out. Please try again.")
            except requests.exceptions.RequestException as e:
                st.error(f"❌ Connection error: {str(e)}")
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")

st.divider()

# Download section
st.subheader("2️⃣ Download Cleaned Data")

# Download button - disabled if no cleaned data
if st.session_state.cleaned_data is not None:
    # Convert to CSV
    csv_buffer = io.StringIO()
    st.session_state.cleaned_data.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()
    
    # Generate download filename
    original_name = st.session_state.original_filename
    if original_name:
        name_without_ext = original_name.rsplit('.', 1)[0]
        download_name = f"{name_without_ext}_cleaned.csv"
    else:
        download_name = "cleaned_data.csv"
    
    st.download_button(
        label="⬇️ Download Cleaned Data",
        data=csv_data,
        file_name=download_name,
        mime="text/csv",
        use_container_width=True
    )
    
    st.success("✅ Ready to download!")
else:
    st.button(
        "⬇️ Download Cleaned Data",
        disabled=True,
        use_container_width=True,
        help="Upload and process a file first"
    )
    st.info("ℹ️ Upload and process a file to enable download")

# Footer
st.divider()
st.caption("💡 Tip: Make sure your n8n webhook is configured to accept file uploads and return cleaned CSV data")
