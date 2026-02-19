import streamlit as st
import pandas as pd
import plotly.express as px
df_grievances=pd.read_csv("grievances.csv")
df_projects=pd.read_csv("projects.csv")
df_wards=pd.read_csv("wards.csv")
df_institutions=pd.read_csv("institutions.csv")

df_innerprj = pd.merge(df_projects, df_wards, on="ward_id", how="inner")
df_innergrv = pd.merge(df_grievances, df_wards, on="ward_id", how="inner")
df_innerins=pd.merge(df_institutions, df_wards, on="ward_id", how="inner")
#Sidebar Filter
ward_list = sorted(df_innerprj["ward_name"].unique())

selected_ward = st.sidebar.selectbox(
    "Select Ward",
    ["All"] + ward_list
)

if selected_ward == "All":
    df_projects_filtered = df_innerprj
else:
    df_projects_filtered = df_innerprj[df_innerprj["ward_name"] == selected_ward]

#filters
if selected_ward == "All":
    df_projects_filtered = df_innerprj
    df_grievances_filtered = df_innergrv
    df_institutions_filtered = df_innerins
else:
    df_projects_filtered = df_innerprj[df_innerprj["ward_name"] == selected_ward
    ]

    df_grievances_filtered = df_innergrv[
        df_innergrv["ward_name"] == selected_ward
    ]

    df_institutions_filtered = df_innerins[
        df_innerins["ward_name"] == selected_ward
    ]
#metrics for dynamic cards
total_projects = df_projects_filtered.shape[0]

pending_requests = df_grievances_filtered[
    df_grievances_filtered["status"] == "Pending"
].shape[0]

active_institutions = df_institutions_filtered[
    df_institutions_filtered["Status"] == "Active"
].shape[0]

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
.blue {color: #2196F3}
.red {color: #D32F2F}
.green {color: #2E7D32}
.yellow{color:#FFD700}
</style>
            
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="MLA CMS system",
    page_icon="🏛️", layout = 'wide')
st.title("📊 Constituency Dashboard")
st.write("Monitor and manage your constituency efficiently")

#KPI Cards
tab1, = st.tabs(["Overview Dashboard"])
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">📁 Total Projects Completed</div>
        <div class="metric-value blue">{total_projects}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">⏳ Pending Requests</div>
        <div class="metric-value red">{pending_requests}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">🏢 Active Institutional Units</div>
        <div class="metric-value green">{active_institutions}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-title">💰 Funds Utilized</div>
        <div class="metric-value yellow">78%</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
#projects by category
df_projectcount = df_projects_filtered.groupby(["category", "status"]).size().reset_index(name="count")
fig4 = px.bar(df_projectcount, x="category", y="count",text="count", color="status", barmode="group",title="Total projects (Completed / Pending / Running) by their category")
fig4.update_traces(textposition="outside")
st.plotly_chart(fig4, use_container_width=True)

#requests by ward
df_reqcount = df_grievances_filtered.groupby("ward_name").size().reset_index(name="request_count")
fig5 = px.pie(df_reqcount, values="request_count", names="ward_name", title="Grievances by Ward Name")


#grievances by dept
df_dept = df_grievances_filtered.groupby("assigned_dept").size().reset_index(name="grievances")
fig6 = px.bar(df_dept, x="assigned_dept", y="grievances",text="grievances", color="assigned_dept", title="Total Grievances by Department")
fig6.update_traces(textposition="outside")
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig5, use_container_width=True)

with col2:
    st.plotly_chart(fig6, use_container_width=True)

#institution subcategories
df_inst = df_institutions_filtered.groupby("infra_category").size().reset_index(name="total_institutions")
fig7=px.bar(df_inst,x="infra_category",y="total_institutions",text="total_institutions",color="infra_category",title="Total Institutions by Category")
fig7.update_traces(textposition="outside")
st.plotly_chart(fig7, use_container_width=True)






