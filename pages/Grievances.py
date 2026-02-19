import streamlit as st
import plotly.express as px
import pandas as pd

df_grievances=pd.read_csv("grievances.csv")
df_wards=pd.read_csv("wards.csv")

df_innergrv = pd.merge(df_grievances, df_wards, on="ward_id", how="inner")

#form for new grievance
@st.dialog("Register a New Grievance")
def add_grievance_dialog():

    with st.form("grievance_form"):
        grievance_id = st.text_input("Grievance ID")
        category = st.selectbox("Category", ["Electricity","Market","Hospital","Police","Road","Sanitation","School","Water"])
        description = st.text_area("Description")
        ward_id = st.text_input("Ward ID")
        assigned_dept = st.text_input("Assigned Department")
        status = st.selectbox("Status", ["Pending","Open","Closed"])
        created_date = st.date_input("Created Date")

        submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Form successfully submitted")

st.markdown("""
<style>
.metric-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 18px rgba(0,0,0,0.12);
}

.metric-title {
    font-size: 14px;
    color: #6c757d;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 38px;
    font-weight: 600;
}
.blue { color: #2196F3; }
.red { color: #D32F2F; }
.green { color: #2E7D32; }
.yellow{ color : #FFD700}
</style>
            
""", unsafe_allow_html=True)
st.set_page_config(page_icon="📝",layout = 'wide')

#form for registering new grievance
col1, col2 = st.columns([6,1])
with col1:
    st.title("📝Grievances")
    st.write("Real-time overview of registered grievances, their status, and resolution progress across wards.")
with col2:
    if st.button("➕ Add Grievance"):
        add_grievance_dialog()
        
#KPI Cards
total_grievances = df_innergrv.shape[0]

resolved_grievances = df_innergrv[
    df_innergrv["status"] == "Closed"
].shape[0]

pending_grievances = df_innergrv[
    df_innergrv["status"] == "Pending"
].shape[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total no. of grievances received</div>
        <div class="metric-value blue">{total_grievances}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Grievances resolved</div>
        <div class="metric-value green">{resolved_grievances}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Grievances pending</div>
        <div class="metric-value red">{pending_grievances}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Average resolution time (days)</div>
        <div class="metric-value yellow">15 days</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

#grievances by category
df_grvcount = df_innergrv.groupby(["category"]).size().reset_index(name="count")
fig = px.bar(df_grvcount, x="category", y="count",text="count", color="category", title="Grievances by various categories")
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

#grievances by status
df_grv = df_innergrv.groupby(["category","status"]).size().reset_index(name="count")
fig2 = px.bar(df_grv, x="category", y="count",text="count", color="status", title="Status of grievances by category")
fig2.update_traces(textposition="outside")
st.plotly_chart(fig2, use_container_width=True)

#detailed table
selected = st.selectbox(
    "Select category to see filtered stats:",
    df_grievances["category"].unique()
)
df_filtered = df_grievances[df_grievances["category"] == selected]
st.dataframe(df_filtered[["grievance_id","assigned_dept","description"]], use_container_width=True)

