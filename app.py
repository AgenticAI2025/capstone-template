
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title='AML Detection Dashboard', 
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    .main-header h1 {
        color: white;
        margin: 0;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 2rem;
        font-weight: bold;
    }
    .metric-card p {
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    .typology-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: bold;
        margin: 0.2rem;
    }
    .structuring { background-color: #ff6b6b; color: white; }
    .layering { background-color: #4ecdc4; color: white; }
    .integration { background-color: #45b7d1; color: white; }
    .placement { background-color: #ffa726; color: white; }
    .unclassified { background-color: #6c757d; color: white; }
    .insight-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-left: 4px solid #007bff;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    .rationale-text {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #28a745;
        font-style: italic;
        margin: 0.5rem 0;
    }
    .typology-stage {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 15px;
        font-size: 0.7rem;
        font-weight: bold;
        margin-left: 0.5rem;
    }
    .placement { background-color: #dc3545; color: white; }
    .layering-stage { background-color: #17a2b8; color: white; }
    .integration-stage { background-color: #28a745; color: white; }
    .unknown { background-color: #6c757d; color: white; }
    .sar-highlight {
        background-color: #ffebee;
        border-left: 4px solid #f44336;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    .filter-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🛡️ AML Detection Dashboard</h1>
    <p style="color: white; font-size: 1.2rem; margin: 0;">Advanced Anti-Money Laundering Risk Assessment & Monitoring</p>
</div>
""", unsafe_allow_html=True)

df = pd.read_csv('aml_report.csv')

# Create typology mapping based on scenario patterns
def classify_typology(scenario):
    scenario_lower = scenario.lower()
    if 'structuring' in scenario_lower or 'sub-threshold' in scenario_lower:
        return 'STRUCTURING'
    elif 'payment chain' in scenario_lower or 'tax havens' in scenario_lower:
        return 'LAYERING'
    elif 'wildlife' in scenario_lower or 'trafficking' in scenario_lower:
        return 'INTEGRATION'
    elif 'sanctioned' in scenario_lower or 'bypass' in scenario_lower:
        return 'INTEGRATION'
    elif 'cryptocurrency' in scenario_lower or 'mixer' in scenario_lower:
        return 'LAYERING'
    elif 'pep' in scenario_lower or 'high-value' in scenario_lower:
        return 'PLACEMENT'
    elif 'trade' in scenario_lower or 'invoice' in scenario_lower:
        return 'LAYERING'
    elif 'high-risk' in scenario_lower or 'country' in scenario_lower:
        return 'PLACEMENT'
    else:
        return 'UNCLASSIFIED'

def generate_typology_rationale(scenario, typology):
    rationale_map = {
        'STRUCTURING': 'Breaking down large transactions into smaller amounts to avoid reporting thresholds',
        'LAYERING': 'Complex transactions to obscure the origin of illicit funds',
        'INTEGRATION': 'Reintroducing laundered funds into the legitimate economy',
        'PLACEMENT': 'Initial placement of illicit funds into the financial system',
        'UNCLASSIFIED': 'Requires further analysis for typology classification'
    }
    return f"Based on scenario '{scenario}': {rationale_map.get(typology, rationale_map['UNCLASSIFIED'])}"

# Create typology columns based on scenario analysis
df['Typology'] = df['Scenario'].apply(classify_typology)
df['Typology Rationale'] = df.apply(lambda row: generate_typology_rationale(row['Scenario'], row['Typology']), axis=1)

# Create a mapping for typology colors and descriptions
typology_info = {
    'STRUCTURING': {
        'color': '#ff6b6b',
        'description': 'Breaking down large transactions into smaller amounts to avoid reporting thresholds',
        'stage': 'Placement'
    },
    'LAYERING': {
        'color': '#4ecdc4', 
        'description': 'Complex transactions to obscure the origin of illicit funds',
        'stage': 'Layering'
    },
    'INTEGRATION': {
        'color': '#45b7d1',
        'description': 'Reintroducing laundered funds into the legitimate economy',
        'stage': 'Integration'
    },
    'PLACEMENT': {
        'color': '#ffa726',
        'description': 'Initial placement of illicit funds into the financial system',
        'stage': 'Placement'
    },
    'UNCLASSIFIED': {
        'color': '#6c757d',
        'description': 'Cases requiring further analysis for typology classification',
        'stage': 'Unknown'
    }
}

# Filters section
st.markdown('<div class="filter-section">', unsafe_allow_html=True)
st.subheader("🔍 Filters & Controls")
col1, col2, col3 = st.columns(3)
with col1:
    risk_filter = st.selectbox("🎯 Risk Level", ["ALL"] + sorted(df["Level"].unique().tolist()))
with col2:
    typ_filter = st.selectbox("📊 Typology", ["ALL"] + sorted(df["Typology"].unique().tolist()))
with col3:
    sar_filter = st.selectbox("🚨 SAR Status", ["ALL", "SAR Required", "No SAR Required"])
st.markdown('</div>', unsafe_allow_html=True)

# Apply filters
filtered = df.copy()
if risk_filter != "ALL":
    filtered = filtered[filtered["Level"] == risk_filter]
if typ_filter != "ALL":
    filtered = filtered[filtered["Typology"] == typ_filter]
if sar_filter == "SAR Required":
    filtered = filtered[filtered["SAR"] == True]
elif sar_filter == "No SAR Required":
    filtered = filtered[filtered["SAR"] == False]

# Key Metrics
st.subheader("📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <h3>{len(filtered)}</h3>
        <p>Total Cases</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    sar_count = len(filtered[filtered["SAR"] == True])
    st.markdown(f"""
    <div class="metric-card">
        <h3>{sar_count}</h3>
        <p>SAR Required</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    sar_rate = (sar_count / len(filtered) * 100) if len(filtered) > 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <h3>{sar_rate:.1f}%</h3>
        <p>SAR Rate</p>
    </div>
    """, unsafe_allow_html=True)

with col4:
    unique_typologies = len(filtered["Typology"].unique())
    st.markdown(f"""
    <div class="metric-card">
        <h3>{unique_typologies}</h3>
        <p>Typology Types</p>
    </div>
    """, unsafe_allow_html=True)

# Typology Insights Dashboard
st.subheader("🧠 Typology Analysis & Insights")

# Typology Overview Cards
typology_counts = filtered["Typology"].value_counts()
col1, col2, col3, col4 = st.columns(4)

for i, (typology_name, count) in enumerate(typology_counts.items()):
    if i < 4:  # Display first 4 typologies
        with [col1, col2, col3, col4][i]:
            info = typology_info.get(typology_name, typology_info['UNCLASSIFIED'])
            stage_class = info['stage'].lower().replace(' ', '-')
            st.markdown(f"""
            <div class="insight-card">
                <h4 style="margin: 0; color: {info['color']};">{typology_name}</h4>
                <p style="margin: 0.5rem 0; font-size: 1.2rem; font-weight: bold;">{count} Cases</p>
                <p style="margin: 0; font-size: 0.9rem; color: #666;">{info['description']}</p>
                <span class="typology-stage {stage_class}">{info['stage']}</span>
            </div>
            """, unsafe_allow_html=True)

# Typology Distribution Chart
st.subheader("📊 Typology Distribution")
fig_typology = px.pie(
    values=typology_counts.values, 
    names=typology_counts.index,
    title="Distribution of AML Typologies",
    color_discrete_sequence=[typology_info.get(typ, typology_info['UNCLASSIFIED'])['color'] for typ in typology_counts.index]
)
fig_typology.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig_typology, use_container_width=True)

# Typology Rationale Analysis
st.subheader("📝 Typology Rationale Analysis")
rationale_analysis = filtered[filtered['Typology Rationale'] != 'No rationale provided']
if len(rationale_analysis) > 0:
    st.markdown("**Cases with detailed typology rationale:**")
    
    # Show rationale insights
    for idx, row in rationale_analysis.iterrows():
        info = typology_info.get(row['Typology'], typology_info['UNCLASSIFIED'])
        stage_class = info['stage'].lower().replace(' ', '-')
        
        st.markdown(f"""
        <div class="rationale-text">
            <h5 style="margin: 0; color: {info['color']};">{row['Scenario']}</h5>
            <p style="margin: 0.5rem 0;"><strong>Typology:</strong> {row['Typology']} 
            <span class="typology-stage {stage_class}">{info['stage']}</span></p>
            <p style="margin: 0;"><strong>Rationale:</strong> {row['Typology Rationale']}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No cases with detailed typology rationale found in the current filter.")

# Risk Level Distribution
st.subheader("⚠️ Risk Level Analysis")
risk_counts = filtered["Level"].value_counts()
# Create a DataFrame for the chart
risk_df = pd.DataFrame({
    'Risk Level': risk_counts.index,
    'Count': risk_counts.values
})
fig_risk = px.bar(
    risk_df,
    x='Risk Level', 
    y='Count',
    title="Cases by Risk Level"
)
fig_risk.update_traces(marker_color='red')
fig_risk.update_layout(showlegend=False)
st.plotly_chart(fig_risk, use_container_width=True)

# Detailed Results Table
st.subheader("📋 Detailed Case Analysis")

# Function to get typology badge class
def get_typology_badge_class(typology):
    typology_lower = typology.lower()
    if typology_lower == 'structuring':
        return 'structuring'
    elif typology_lower == 'layering':
        return 'layering'
    elif typology_lower == 'integration':
        return 'integration'
    elif typology_lower == 'placement':
        return 'placement'
    else:
        return 'unclassified'

# Display filtered results with enhanced styling
if len(filtered) > 0:
    st.markdown("**📋 Detailed Case Analysis:**")
    
    for idx, row in filtered.iterrows():
        typology_class = get_typology_badge_class(row["Typology"])
        info = typology_info.get(row["Typology"], typology_info['UNCLASSIFIED'])
        stage_class = info['stage'].lower().replace(' ', '-')
        sar_indicator = "🚨 SAR REQUIRED" if row["SAR"] else "✅ No SAR"
        sar_style = "sar-highlight" if row["SAR"] else ""
        
        # Check if rationale is available
        rationale_text = row['Typology Rationale'] if row['Typology Rationale'] != 'No rationale provided' else 'No detailed rationale available'
        
        st.markdown(f"""
        <div class="{sar_style}">
            <h4>📄 {row['Scenario']}</h4>
            <p><strong>Risk Level:</strong> {row['Level']} | <strong>Score:</strong> {row['Overall Score']} | <strong>Status:</strong> {sar_indicator}</p>
            <p><strong>Typology:</strong> <span class="typology-badge {typology_class}">{row['Typology']}</span> 
            <span class="typology-stage {stage_class}">{info['stage']}</span></p>
            <p><strong>Description:</strong> {info['description']}</p>
            <div class="rationale-text">
                <strong>Rationale:</strong> {rationale_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.warning("No cases match the selected filters.")

# SAR-required Cases Summary
sar_cases = filtered[filtered["SAR"] == True]
if len(sar_cases) > 0:
    st.subheader("🚨 SAR-Required Cases Summary")
    st.markdown(f"**Total SAR-required cases: {len(sar_cases)}**")
    
    # SAR cases by typology
    sar_typology_counts = sar_cases["Typology"].value_counts()
    # Create a DataFrame for the chart
    sar_df = pd.DataFrame({
        'Typology': sar_typology_counts.index,
        'Count': sar_typology_counts.values
    })
    fig_sar = px.bar(
        sar_df,
        x='Typology',
        y='Count',
        title="SAR-Required Cases by Typology"
    )
    fig_sar.update_traces(marker_color='red')
    fig_sar.update_layout(showlegend=False)
    st.plotly_chart(fig_sar, use_container_width=True)
else:
    st.success("✅ No SAR-required cases found with current filters.")

# Comprehensive Insights Summary
st.subheader("🔍 Comprehensive Insights Summary")

# Calculate insights
total_cases = len(filtered)
sar_cases = len(filtered[filtered["SAR"] == True])
sar_rate = (sar_cases / total_cases * 100) if total_cases > 0 else 0

# Typology insights
typology_insights = []
for typology_name in filtered["Typology"].unique():
    typology_data = filtered[filtered["Typology"] == typology_name]
    typology_sar_rate = (len(typology_data[typology_data["SAR"] == True]) / len(typology_data) * 100) if len(typology_data) > 0 else 0
    info = typology_info.get(typology_name, typology_info['UNCLASSIFIED'])
    
    typology_insights.append({
        'typology': typology_name,
        'count': len(typology_data),
        'sar_rate': typology_sar_rate,
        'stage': info['stage'],
        'description': info['description']
    })

# Display insights
col1, col2 = st.columns(2)

with col1:
    st.markdown("**📊 Key Statistics:**")
    st.markdown(f"""
    - **Total Cases Analyzed:** {total_cases}
    - **SAR Required Cases:** {sar_cases} ({sar_rate:.1f}%)
    - **Typology Categories:** {len(filtered["Typology"].unique())}
    - **Cases with Rationale:** {len(filtered[filtered['Typology Rationale'] != 'No rationale provided'])}
    """)

with col2:
    st.markdown("**🎯 Top Risk Typologies:**")
    for insight in sorted(typology_insights, key=lambda x: x['sar_rate'], reverse=True)[:3]:
        st.markdown(f"""
        - **{insight['typology']}** ({insight['stage']}): {insight['count']} cases, {insight['sar_rate']:.1f}% SAR rate
        """)

# Risk Assessment Summary
st.markdown("**⚠️ Risk Assessment Summary:**")
if sar_rate > 70:
    st.error(f"🚨 HIGH RISK: {sar_rate:.1f}% of cases require SAR filing. Immediate attention needed.")
elif sar_rate > 40:
    st.warning(f"⚠️ MODERATE RISK: {sar_rate:.1f}% of cases require SAR filing. Monitor closely.")
else:
    st.success(f"✅ LOW RISK: {sar_rate:.1f}% of cases require SAR filing. Normal operations.")

# Typology Stage Analysis
st.markdown("**🔄 Money Laundering Stage Analysis:**")
stage_analysis = {}
for insight in typology_insights:
    stage = insight['stage']
    if stage not in stage_analysis:
        stage_analysis[stage] = {'count': 0, 'sar_cases': 0}
    stage_analysis[stage]['count'] += insight['count']
    stage_analysis[stage]['sar_cases'] += insight['count'] * (insight['sar_rate'] / 100)

for stage, data in stage_analysis.items():
    stage_sar_rate = (data['sar_cases'] / data['count'] * 100) if data['count'] > 0 else 0
    st.markdown(f"- **{stage}:** {data['count']} cases, {stage_sar_rate:.1f}% SAR rate")
