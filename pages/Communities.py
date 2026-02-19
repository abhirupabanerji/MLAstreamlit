import streamlit as st
import pandas as pd
import plotly.express as px
df_citizen=pd.read_csv("citizen_demographics.csv")
df_wards=pd.read_csv("wards.csv")
df_religion = pd.read_csv("religions.csv")
df_innerreligion = pd.merge(df_religion, df_wards, how="inner", on="ward_id")
@st.dialog("Add a New Community")
def add_community():

    with st.form("form"):
        category = st.selectbox("Category", ["Buddhjiwi", "Market", "Club", "Sports Team", "Women group", "Slum", "RWA", "Senior"])
        president_name = st.text_input("President Name")
        ward_id = st.text_input("Ward ID")
        members = st.number_input("No. of members")
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
.Slums { color: #1F77B4}

.Markets{ color:#AEC7E8}

.RWA{ color:#D62728}

.Women { color:#FF9896}

.Sports { color: #17BECF}

.Senior{ color: #98DF8A}

.Clubs { color: #FF7F0E}

.Bud{ color: #FFBB78}
</style>
            
""", unsafe_allow_html=True)
st.set_page_config(page_icon="👥",layout = 'wide')
col1, col2 = st.columns([6,1])
with col1:
    st.title("👥Communities")
    st.write("Monitor and analyze demographic distribution across major community groups to support informed governance decisions.")
with col2:
    if st.button("➕Add community"):
        add_community()
    



#KPI Cards
Buddhjiwis = df_citizen[df_citizen["community_group"] == "Buddhjiwis"].shape[0]

Markets = df_citizen[df_citizen["community_group"] == "Markets"].shape[0]

Clubs = df_citizen[df_citizen["community_group"] == "Clubs"].shape[0]

Sports = df_citizen[df_citizen["community_group"] == "Sports Teams"].shape[0]

Women = df_citizen[df_citizen["community_group"] == "Women Groups"].shape[0]

Slums = df_citizen[df_citizen["community_group"] == "Slums"].shape[0]

RWA = df_citizen[df_citizen["community_group"] == "RWA"].shape[0]

Senior = df_citizen[df_citizen["community_group"] == "Senior Citizens"].shape[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Slums</div>
        <div class="metric-value Slums">{Slums}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">RWA's</div>
        <div class="metric-value RWA">{RWA}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Women Groups</div>
        <div class="metric-value Women">{Women}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Senior citizens</div>
        <div class="metric-value Senior">{Senior}</div>
    </div>
    """, unsafe_allow_html=True)
st.write("")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Markets</div>
        <div class="metric-value Markets">{Markets}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Clubs</div>
        <div class="metric-value Clubs">{Clubs}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Sport Teams</div>
        <div class="metric-value Sports">{Sports}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Buddhjiwis</div>
        <div class="metric-value Bud">{Buddhjiwis}</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
#total population
fig3=px.pie(df_citizen, values='total_population', names='community_group', title='Communities in my constituency')
st.plotly_chart(fig3, use_container_width=True)

#male count
df_total = df_citizen.groupby("community_group", as_index=False)["male_count"].sum()
fig=px.bar(df_total,x="community_group",y="male_count",color="community_group",text="male_count", labels={"x":"communitites","y":"male count"},title="Male count in various communitites")
fig.update_traces(textposition="outside")

#female count
df_ftotal = df_citizen.groupby("community_group", as_index=False)["female_count"].sum()
fig2=px.bar(df_ftotal,x="community_group",y="female_count",text="female_count",color="community_group",labels={"x":"communitites","y":"male count"},title="Female count in various communitites")
fig2.update_traces(textposition="outside")

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.plotly_chart(fig2, use_container_width=True)

#religions by ward name
df_religion_sum = (df_innerreligion.groupby("religion")["population_x"].sum().reset_index())

fig3 = px.bar(df_religion_sum, x="religion", y="population_x", color="religion", title="Population by Religion", text="population_x")
fig3.update_traces(textposition="outside")
st.plotly_chart(fig3, use_container_width=True)
