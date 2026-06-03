import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="The Sugar Trap — Market Gap Analysis",
    layout="wide",
    page_icon="🫙"
)

#Load data
@st.cache_data
def load_data():
    return pd.read_csv('nutrient_matrix.csv')

df = load_data()

#Header
st.title("The Sugar Trap Plot")
st.subheader("Snack Market Gap Analysis — Helix CPG Partners")
st.markdown("---")

#Sidebar: Category filter 
st.sidebar.header("Filter by Category")

# Categories ordered by your Story 2 findings
category_order = [
    'Cereals & Grains',
    'Dairy & Eggs',
    'Confectionery',
    'Beverages',
    'Meat & Fish',
    'Bakery & Snacks',
    'Condiments & Seasonings',
    'Protein Bars & Suppliments',
    'Legumes & Plant Protein',
    'Fruits & Vegetables',
    'Nuts & Seeds',
]

# Only show categories that exist in the data
available = [c for c in category_order if c in df['primary_category'].unique()]

selected_cats = st.sidebar.multiselect(
    "Select categories:",
    options=available,
    default=available
)

filtered = df[df['primary_category'].isin(selected_cats)]

st.sidebar.markdown("---")
st.sidebar.metric("Products shown",     f"{len(filtered):,}")
st.sidebar.metric("Categories selected", len(selected_cats))

#Story 3: Scatter Plot
st.subheader("Nutrient Matrix — Sugar vs Protein")
st.caption("Color = quadrant zone")

color_map = {
    'High Protein Low Sugar (Blue Ocean)' : '#2E7D32',
    'High Protein High Sugar'             : '#66BB6A',
    'Low Sugar Low Protein'               : '#FFA726',
    'High Sugar Low Protein (Danger Zone)': '#EF5350',
}

figure = px.scatter(
    filtered,
    x='sugars_100g',
    y='proteins_100g',
    color='quadrant',
    color_discrete_map=color_map,
    hover_data=['product_name', 'primary_category'],
    opacity=0.5,
    labels={
        'sugars_100g'  : 'Sugar (g per 100g)',
        'proteins_100g': 'Protein (g per 100g)',
        'quadrant'     : 'Quadrant'
    },
    title='Sugar vs Protein — The Blue Ocean is top-left (high protein, low sugar)'
)

figure.add_vline(
    x=10,
    line_dash='dash',
    line_color='green',
    annotation_text='Low Sugar Threshold (10g)',
    annotation_position='top right'
)
figure.add_hline(
    y=15,
    line_dash='dash',
    line_color='green',
    annotation_text='High Protein Threshold (15g)',
    annotation_position='top right'
)

figure.update_layout(
    height=580,
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=-02,
        xanchor='center',
        x=0.5
    )
)
st.plotly_chart(figure, use_container_width=True)

#Quadrant counts
quad_counts = filtered['quadrant'].value_counts()
c1, c2, c3, c4 = st.columns(4)
c1.metric("🟢 Blue Ocean",    f"{quad_counts.get('High Protein Low Sugar (Blue Ocean)', 0):,}")
c2.metric("🟡 Low Protein",   f"{quad_counts.get('Low Sugar Low Protein', 0):,}")
c3.metric("🟠 High P+S",      f"{quad_counts.get('High Protein High Sugar', 0):,}")
c4.metric("🔴 Danger Zone",   f"{quad_counts.get('High Sugar Low Protein (Danger Zone)', 0):,}")

#Key Insight Box
st.markdown("---")
st.subheader("SUMMARY")
 
best_category  = "Meat & Fish"  
target_protein = "20.0g"    
target_sugar   = "3.4g" 

st.success(
    f"**Based on the data, the biggest market opportunity is in \n"
    f"{best_category}, specifically targeting products with \n"
    f"{target_protein}g of protein and less than {target_sugar}g of sugar.**"
)

# footer
st.markdown("---")
st.caption(
    "Data source: Open Food Facts — openfoodfacts.org  |  "
    "Analysis by Alain Ngabo  |  Helix CPG Partners Dataset"
)
