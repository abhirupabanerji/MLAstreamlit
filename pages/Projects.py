import streamlit as st
import pandas as pd
import plotly.express as px

df=pd.read_csv("projects.csv")
@st.dialog("Add a New Community")
def add_project():

    with st.form("form"):
        name = st.text_input("Project Name")
        category = st.selectbox("Category", ["Education", "Police", "Healthcare", "Infrastructure", "Religious", "Sports", "Welfare"])
        ward = st.text_input("Ward Name")
        status = st.selectbox("Status",["Running","Pending","Completed"])
        contractor = st.text_input("Assigned Contractor")
        budget = st.number_input("Budget Sanctioned")
        released= st.number_input("Budget Released")
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
""", unsafe_allow_html=True)

st.set_page_config(layout='wide')
col1 , col2 = st.columns([6,1])
with col1:
    st.title("📁Projects")
    st.write("Project status, budget allocation, completion rate.")
with col2:
    if st.button("➕ Add Project"):
        add_project()

#KPI Cards
total = df.shape[0]

running = df[df["status"] == "Running"].shape[0]

pending = df[df["status"] == "Pending"].shape[0]

completed = df[df["status"] == "Completed"].shape[0]
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total no. of projects</div>
        <div class="metric-value blue">{total}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Projects Pending</div>
        <div class="metric-value red">{pending}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Projects Running</div>
        <div class="metric-value yellow">{running}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Projects Completed</div>
        <div class="metric-value green">{completed}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")

#Projects completed by category
df_proj = df.groupby("category").size().reset_index(name="projects")
fig=px.bar(df_proj,x="category",y="projects",text="projects",color="category",title="Projects Completed by Category")
fig.update_traces(textposition="outside")
st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    #funds sanctioned vs used vs released 
    df_project = df.groupby("category")[["budget_sanctioned", "budget_released", "budget_used"]].sum().reset_index()
    df_long = df_project.melt(id_vars="category", value_vars=["budget_sanctioned", "budget_released", "budget_used"], var_name="Budget Type", value_name="Amount")
    fig2 = px.bar(df_long, x="category", y="Amount",text="Amount", color="Budget Type", barmode="group", title="Budget Comparison by Category")
    fig2.update_traces(textposition="outside")
    st.plotly_chart(fig2, use_container_width=True)
with col2:
    #average time taken for project completion
    df_completed = df[df["status"] == "Completed"]
    df_completed["start_date"] = pd.to_datetime(df_completed["start_date"])
    df_completed["end_date"] = pd.to_datetime(df_completed["end_date"])
    df_completed["completion_days"] = (df_completed["end_date"] - df_completed["start_date"]).dt.days
    avg_time = (df_completed.groupby("category")["completion_days"].mean().reset_index())

    fig4 = px.bar(avg_time, x="category", y="completion_days",text="completion_days",color="category", title="Average Time Taken for Project Completion (Days)", labels={"completion_days": "Average Completion Time (Days)"})
    fig4.update_traces(textposition="outside")
    st.plotly_chart(fig4, use_container_width=True)

#detailed table
dept_selected = st.selectbox(
    "Select Department to see filtered stats:",
    df["department"].unique()
)
df_filtered = df[df["department"] == dept_selected]
st.dataframe(df_filtered[["project_name","contractor","status"]],use_container_width=True)





