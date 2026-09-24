import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------------
# 1. Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Soil Health & Crop Advisory Dashboard",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling cards and metrics
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #2E7D32;
        font-weight: bold;
        text-align: center;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.1rem;
        color: #555555;
        text-align: center;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 15px;
        border-left: 5px solid #2E7D32;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    stButton>button {
        width: 100%;
        background-color: #2E7D32;
        color: white;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Data Loading & Preprocessing
# ---------------------------------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv('Crop_recommendation.csv')
    return df

df = load_data()

# Sample/Average Market Rates Data (per Quintal in INR)
# These represent typical Mandi rates for crops in the dataset
crop_prices = {
    'rice': {'rate': 2300, 'unit': '₹ / Quintal', 'trend': '+2.5%'},
    'maize': {'rate': 2100, 'unit': '₹ / Quintal', 'trend': '+1.2%'},
    'chickpea': {'rate': 5400, 'unit': '₹ / Quintal', 'trend': '-0.5%'},
    'kidneybeans': {'rate': 8500, 'unit': '₹ / Quintal', 'trend': '+3.1%'},
    'pigeonpeas': {'rate': 7000, 'unit': '₹ / Quintal', 'trend': '+0.8%'},
    'mothbeans': {'rate': 6200, 'unit': '₹ / Quintal', 'trend': '0.0%'},
    'mungbean': {'rate': 7700, 'unit': '₹ / Quintal', 'trend': '+1.5%'},
    'blackgram': {'rate': 6900, 'unit': '₹ / Quintal', 'trend': '-1.0%'},
    'lentil': {'rate': 6400, 'unit': '₹ / Quintal', 'trend': '+0.5%'},
    'pomegranate': {'rate': 7500, 'unit': '₹ / Quintal', 'trend': '+4.2%'},
    'banana': {'rate': 1800, 'unit': '₹ / Quintal', 'trend': '+2.0%'},
    'mango': {'rate': 4500, 'unit': '₹ / Quintal', 'trend': '+5.0%'},
    'grapes': {'rate': 5500, 'unit': '₹ / Quintal', 'trend': '-2.1%'},
    'watermelon': {'rate': 1200, 'unit': '₹ / Quintal', 'trend': '+1.0%'},
    'muskmelon': {'rate': 1500, 'unit': '₹ / Quintal', 'trend': '+0.0%'},
    'apple': {'rate': 9000, 'unit': '₹ / Quintal', 'trend': '+1.8%'},
    'orange': {'rate': 3800, 'unit': '₹ / Quintal', 'trend': '+2.3%'},
    'papaya': {'rate': 2200, 'unit': '₹ / Quintal', 'trend': '-0.8%'},
    'coconut': {'rate': 2800, 'unit': '₹ / 1000 Nuts', 'trend': '+0.2%'},
    'cotton': {'rate': 6700, 'unit': '₹ / Quintal', 'trend': '+3.5%'},
    'jute': {'rate': 5050, 'unit': '₹ / Quintal', 'trend': '+1.1%'},
    'coffee': {'rate': 11000, 'unit': '₹ / Quintal', 'trend': '+4.0%'}
}

# ---------------------------------------------------------
# 3. Header
# ---------------------------------------------------------
st.markdown("<h1 class='main-header'>🌱 Soil Health Data Analysis & Farmer Awareness Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-header'>Empowering farmers with smart soil analytics, crop recommendations, and market intelligence.</p>", unsafe_allow_html=True)

# ---------------------------------------------------------
# 4. Sidebar Controls
# ---------------------------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/628/628283.png", width=80)
st.sidebar.title("📌 Navigation & Filters")

nav_choice = st.sidebar.radio(
    "Go to:",
    ["📊 Soil Analytics Dashboard", "🎯 Crop Advisory Tool", "💰 Crop Market Rates", "💡 Soil Care Guidelines"]
)

st.sidebar.markdown("---")
st.sidebar.caption("Project: Soil Health Analysis | Developed for Farmer Awareness")

# ---------------------------------------------------------
# 5. Navigation Tab Logic
# ---------------------------------------------------------

if nav_choice == "📊 Soil Analytics Dashboard":
    st.subheader("📊 Dataset Overview & Parameter Analysis")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Samples", len(df))
    col2.metric("Total Crop Varieties", len(df['label'].unique()))
    col3.metric("Avg Nitrogen (N)", f"{df['N'].mean():.1f} kg/ha")
    col4.metric("Avg Soil pH", f"{df['ph'].mean():.2f}")
    
    st.markdown("---")
    
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.markdown("#### Soil N-P-K Levels by Crop")
        selected_crop = st.selectbox("Select Crop for Soil Profile:", sorted(df['label'].unique()))
        crop_df = df[df['label'] == selected_crop]
        
        avg_npk = pd.DataFrame({
            'Nutrient': ['Nitrogen (N)', 'Phosphorus (P)', 'Potassium (K)'],
            'Value': [crop_df['N'].mean(), crop_df['P'].mean(), crop_df['K'].mean()]
        })
        
        fig_bar = px.bar(
            avg_npk, x='Nutrient', y='Value', color='Nutrient',
            title=f"Average N-P-K Requirement for {selected_crop.capitalize()}",
            text_auto='.1f',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        st.markdown("#### Environmental Parameters Scatter Analysis")
        x_axis = st.selectbox("Select X-Axis Parameter:", ['temperature', 'humidity', 'ph', 'rainfall'], index=0)
        y_axis = st.selectbox("Select Y-Axis Parameter:", ['temperature', 'humidity', 'ph', 'rainfall'], index=3)
        
        fig_scatter = px.scatter(
            df, x=x_axis, y=y_axis, color='label',
            title=f"{x_axis.capitalize()} vs {y_axis.capitalize()} Distribution",
            hover_data=['label']
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

elif nav_choice == "🎯 Crop Advisory Tool":
    st.subheader("🎯 Input Soil & Weather Values to Find Suitable Crops")
    
    col_input1, col_input2, col_input3 = st.columns(3)
    
    with col_input1:
        input_n = st.number_input("Nitrogen (N) - kg/ha", min_value=0, max_value=200, value=70)
        input_p = st.number_input("Phosphorus (P) - kg/ha", min_value=0, max_value=200, value=45)
        input_k = st.number_input("Potassium (K) - kg/ha", min_value=0, max_value=200, value=40)
        
    with col_input2:
        input_temp = st.slider("Temperature (°C)", min_value=0.0, max_value=50.0, value=25.0)
        input_hum = st.slider("Humidity (%)", min_value=0.0, max_value=100.0, value=70.0)
        
    with col_input3:
        input_ph = st.slider("Soil pH Level", min_value=0.0, max_value=14.0, value=6.5)
        input_rain = st.slider("Rainfall (mm)", min_value=0.0, max_value=300.0, value=150.0)

    if st.button("🔎 Analyze Soil & Recommend Crop"):
        # Distance-based simple recommendation (Nearest Centroid)
        means = df.groupby('label')[['N', 'P', 'K', 'temperature', 'humidity', 'ph', 'rainfall']].mean()
        user_vals = np.array([input_n, input_p, input_k, input_temp, input_hum, input_ph, input_rain])
        
        distances = np.linalg.norm(means.values - user_vals, axis=1)
        best_match_idx = np.argmin(distances)
        recommended_crop = means.index[best_match_idx]
        
        st.success(f"🎉 **Recommended Crop:** `{recommended_crop.upper()}`")
        
        # Display crop market details
        crop_info = crop_prices.get(recommended_crop, {'rate': 'N/A', 'unit': 'N/A', 'trend': '0.0%'})
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("Estimated Market Price", f"{crop_info['rate']} {crop_info['unit']}", delta=crop_info['trend'])
        with res_col2:
            st.info(f"The recommended crop **{recommended_crop.capitalize()}** matches your soil N-P-K ratios and environmental conditions.")

elif nav_choice == "💰 Crop Market Rates":
    st.subheader("💰 Live Market Rates & Price Index (Estimated Mandi Rates)")
    
    # Filter search
    search = st.text_input("🔍 Search Crop Price:", "")
    
    price_data = []
    for crop, data in crop_prices.items():
        if search.lower() in crop.lower():
            price_data.append({
                "Crop Name": crop.capitalize(),
                "Market Price": f"{data['rate']} {data['unit']}",
                "Price Trend": data['trend']
            })
            
    price_df = pd.DataFrame(price_data)
    st.dataframe(price_df, use_container_width=True)
    
    # Price Comparison Chart
    st.markdown("#### 📈 Crop Price Comparison")
    top_crops_df = pd.DataFrame([
        {"Crop": k.capitalize(), "Price (INR)": v['rate']} for k, v in crop_prices.items()
    ]).sort_values(by="Price (INR)", ascending=False)
    
    fig_price = px.bar(
        top_crops_df, x="Crop", y="Price (INR)",
        title="Market Rate per Quintal across Crop Types",
        color="Price (INR)",
        color_continuous_scale="Greens"
    )
    st.plotly_chart(fig_price, use_container_width=True)

elif nav_choice == "💡 Soil Care Guidelines":
    st.subheader("💡 Farmer Awareness & Soil Health Management Guide")
    
    st.markdown("""
    ### 🌿 1. Understanding N-P-K Balance
    * **Nitrogen (N):** Promotes leaf and vegetative growth. Deficiencies cause yellowing of leaves.
    * **Phosphorus (P):** Stimulates root growth, flowering, and seed development.
    * **Potassium (K):** Enhances disease resistance, drought tolerance, and overall plant vigor.

    ### 🧪 2. Soil pH Management
    * **Acidic Soil (pH < 6.0):** Apply agricultural lime (calcium carbonate) or wood ash to raise pH.
    * **Neutral Soil (pH 6.0 - 7.5):** Ideal for most crops.
    * **Alkaline Soil (pH > 7.5):** Apply organic compost, sulfur, or gypsum to reduce alkalinity.

    ### 💧 3. Water & Irrigation Advice
    * Ensure efficient drainage systems to prevent root rot.
    * Practice drip irrigation for high-value crops like grapes, pomegranate, and bananas.
    """)