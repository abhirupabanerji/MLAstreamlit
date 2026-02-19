import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df=pd.read_csv("institutions.csv")
@st.dialog("Add a New Institution")
def add_institution():

    with st.form("form"):
        grievance_id = st.text_input("Institution ID")
        category = st.selectbox("Category", ["Temple", "Hospital", "School", "College", "Police Station", "NGO", "Gym", "Govt. Office"])
        head_name = st.text_input("Head Name")
        designation = st.text_input("Designation")
        ward_id = st.text_input("Ward ID")
        Address = st.text_area("Full address")
        phone = st.text_input("Phone number")
        dob = st.date_input("DOB")
        submitted = st.form_submit_button("Submit")
    if submitted:
        st.success("Form successfully submitted")

st.set_page_config(page_icon="🏫",layout='wide')

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
.Temples{ color: #1F77B4}

.Schools{ color:#AEC7E8}

.Hospitals{ color:#D62728}

.Colleges{ color:#FF9896}

.Police{ color: #17BECF}

.NGO{ color: #98DF8A}

.Gym { color: #FF7F0E}

.Govoffice { color: #FFBB78}
</style>
            
""", unsafe_allow_html=True)

col1 , col2=st.columns([6,1])
with col1:
    st.title("🏫Institutions")
    st.write("Track and analyze the presence of institutional groups across the constituency.")
with col2:
    if st.button("➕ Add Institution"):
        add_institution()

#KPI cards
Temples = df[df["infra_category"] == "Temples"].shape[0]

Schools = df[df["infra_category"] == "Schools"].shape[0]

Hospitals = df[df["infra_category"] == "Hospitals"].shape[0]

Colleges = df[df["infra_category"] == "Colleges"].shape[0]

Police = df[df["infra_category"] == "Police Stations"].shape[0]

Govt_Offices = df[df["infra_category"] == "Govt Offices"].shape[0]

NGOs = df[df["infra_category"] == "NGOs"].shape[0]

Gyms = df[df["infra_category"] == "Gyms"].shape[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Temples</div>
        <div class="metric-value Temples">{Temples}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Schools</div>
        <div class="metric-value Schools">{Schools}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Hospitals</div>
        <div class="metric-value Hospitals">{Hospitals}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Colleges</div>
        <div class="metric-value Colleges">{Colleges}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Police Stations</div>
        <div class="metric-value Police">{Police}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Govt Offices</div>
        <div class="metric-value Govoffice">{Govt_Offices}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Gyms</div>
        <div class="metric-value Gym">{Gyms}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">NGOs</div>
        <div class="metric-value NGO">{NGOs}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

#institutions by category 
df_inst = df.groupby("infra_category").size().reset_index(name="total_institutions")
fig=px.bar(df_inst,x="infra_category",y="total_institutions",text="total_institutions",color="infra_category",title="Total Institutions by Category")
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

#institutions by status
category_selected = st.selectbox(
    "Select Institution Category",
    df["infra_category"].unique()
)

df_filtered = df[df["infra_category"] == category_selected]

df_status = df_filtered.groupby("Status").size().reset_index(name="count")

fig2 = px.pie(df_status, names="Status", values="count", title=f"{category_selected} Status Distribution", color="Status")
st.plotly_chart(fig2, use_container_width=True)

#detailed table
des_selected = st.selectbox(
    "Select Designation to see filtered stats:",
    df["designation"].unique()
)
df_filtered = df[df["designation"] == des_selected]
st.dataframe(df_filtered[['head_name','contact_number','dob','email_id']], use_container_width=True)