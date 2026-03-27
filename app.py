import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="A1 Mart Sales Forecasting",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== SESSION STATE ==================
if "users" not in st.session_state:
    st.session_state.users = {}
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "page" not in st.session_state:
    st.session_state.page = "🔐 Login"
if "data" not in st.session_state:
    st.session_state.data = None

# ================== SIDEBAR NAVIGATION ==================
if not st.session_state.authenticated:
    options = ["🔐 Login", "📝 Signup", "🔑 Forgot Password"]
else:
    options = ["📂 Upload CSV File", "📊 Dashboard", "🔮 Forecast Sales"]

st.session_state.page = st.sidebar.radio(
    "Navigation",
    options,
    index=options.index(st.session_state.page)
)
page = st.session_state.page

# ================== HEADER BANNER ==================
st.markdown("""
<div style="text-align:center; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
            padding: 30px; border-radius: 15px; margin-bottom: 20px;">
    <h1 style="color: white; margin: 0;">📊 A1 Mart Sales Forecasting</h1>
    <p style="color: #e0e0e0; font-size: 18px; margin-top: 10px;">📈 Unlocking Tomorrow's Insights, Today!</p>
</div>
""", unsafe_allow_html=True)

# ================== AUTHENTICATION PAGES ==================

# LOGIN PAGE
if page == "🔐 Login":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔐 Login to Your Account")
        
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        
        if st.button("🚀 Login", use_container_width=True):
            if username and password:
                if username in st.session_state.users and st.session_state.users[username] == password:
                    st.session_state.authenticated = True
                    st.success("✅ Login Successful! Redirecting...")
                    st.session_state.page = "📂 Upload CSV File"
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")
            else:
                st.warning("⚠️ Please enter username and password.")

# SIGNUP PAGE
elif page == "📝 Signup":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("📝 Create New Account")
        
        username = st.text_input("👤 Username")
        password = st.text_input("🔑 Password", type="password")
        confirm = st.text_input("🔑 Confirm Password", type="password")
        
        if st.button("✅ Submit", use_container_width=True):
            if not username or not password:
                st.warning("⚠️ Please fill all fields.")
            elif username in st.session_state.users:
                st.error("❌ Username already exists!")
            elif password != confirm:
                st.error("❌ Passwords do not match!")
            else:
                st.session_state.users[username] = password
                st.success("✅ Signup successful! Please login now.")

# FORGOT PASSWORD PAGE
elif page == "🔑 Forgot Password":
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("🔑 Reset Your Password")
        
        username = st.text_input("👤 Username")
        new_pass = st.text_input("🔑 New Password", type="password")
        confirm = st.text_input("🔑 Confirm Password", type="password")
        
        if st.button("🔄 Update Password", use_container_width=True):
            if not username or not new_pass:
                st.warning("⚠️ Please fill all fields.")
            elif username not in st.session_state.users:
                st.error("❌ Username not found!")
            elif new_pass != confirm:
                st.error("❌ Passwords do not match!")
            else:
                st.session_state.users[username] = new_pass
                st.success("✅ Password updated! Please login.")

# ================== DATA UPLOAD PAGE ==================
elif page == "📂 Upload CSV File":
    if not st.session_state.authenticated:
        st.error("❌ Please login first!")
    else:
        st.subheader("📂 Upload Your Sales Data")
        
        uploaded_file = st.file_uploader("📥 Choose a CSV file", type=["csv"])
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                
                # Required columns
                required_columns = [
                    "Quantity Purchased", "Product Name", "Date and Time",
                    "Sales Price", "Subcategory", "Category", "Discounted Price"
                ]
                
                # Check for missing columns
                missing = [col for col in required_columns if col not in df.columns]
                
                if missing:
                    st.error(f"❌ Missing columns: {', '.join(missing)}")
                else:
                    st.session_state.data = df
                    st.success("✅ File uploaded successfully!")
                    
                    # Show data preview
                    st.subheader("📋 Data Preview")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Rows", len(df))
                    with col2:
                        st.metric("Total Columns", len(df.columns))
                    with col3:
                        st.metric("Memory Used", f"{df.memory_usage(deep=True).sum() / 1024:.2f} KB")
                    
                    st.session_state.page = "📊 Dashboard"
                    if st.button("✅ Proceed to Dashboard"):
                        st.rerun()

            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")

        # Add Load Sample Data Button
        import os
        sample_file = "sample_sales_data.csv"
        if os.path.exists(sample_file):
            st.info("💡 Tip: You can load the pre-generated sample data to test the app.")
            if st.button("📊 Load Sample Data", use_container_width=True):
                try:
                    df = pd.read_csv(sample_file)
                    st.session_state.data = df
                    st.success("✅ Sample data loaded successfully!")
                    st.session_state.page = "📊 Dashboard"
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error loading sample data: {str(e)}")

# ================== DASHBOARD PAGE ==================
elif page == "📊 Dashboard":
    if not st.session_state.authenticated:
        st.error("❌ Please login first!")
    elif st.session_state.data is None:
        st.warning("⚠️ Please upload a CSV file first!")
        if st.button("📂 Go to Upload"):
            st.session_state.page = "📂 Upload CSV File"
            st.rerun()
    else:
        df = st.session_state.data.copy()
        
        # Data Preprocessing
        df['Date and Time'] = pd.to_datetime(df['Date and Time'])
        df['Month'] = df['Date and Time'].dt.strftime('%B')
        df['Profit'] = df['Sales Price'] - df['Discounted Price']
        
        month_order = ['January', 'February', 'March', 'April', 'May', 'June', 
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        # --- TAB 1: SALES OVERVIEW ---
        st.subheader("📊 Sales Overview")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("💰 Total Sales", f"₹{df['Sales Price'].sum():,.0f}")
        with col2:
            st.metric("📦 Total Quantity", f"{df['Quantity Purchased'].sum():,.0f}")
        with col3:
            st.metric("💵 Total Profit", f"₹{df['Profit'].sum():,.0f}")
        with col4:
            st.metric("📈 Avg Sale Value", f"₹{df['Sales Price'].mean():,.0f}")
        
        st.markdown("---")
        
        # Sales by Category
        st.subheader("Sales Distribution by Category")
        category_sales = df.groupby("Category")["Sales Price"].sum().reset_index()
        
        fig_sales = px.pie(
            category_sales, 
            values='Sales Price', 
            names='Category',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_sales.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_sales, use_container_width=True)
        
        st.markdown("---")
        
        # Profit Distribution
        st.subheader("💹 Profit Distribution by Category")
        profit_data = df.groupby("Category")["Profit"].sum().reset_index()
        
        fig_profit = px.pie(
            profit_data, 
            values='Profit', 
            names='Category',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        fig_profit.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_profit, use_container_width=True)
        
        st.markdown("---")
        
        # Sales by Category Over Months
        st.subheader("📅 Sales by Category Over Time")
        
        unique_cats = sorted(df["Category"].unique().tolist())
        selected_cat = st.selectbox("Select Category:", ["All Categories"] + unique_cats)
        
        if selected_cat == "All Categories":
            filt_df = df
        else:
            filt_df = df[df["Category"] == selected_cat]
        
        bar_data = filt_df.groupby(['Month', 'Category'])['Sales Price'].sum().reset_index()
        
        fig_bar = px.bar(
            bar_data, 
            x='Month', 
            y='Sales Price', 
            color='Category',
            barmode='group',
            category_orders={"Month": month_order},
            color_discrete_sequence=px.colors.qualitative.Vivid
        )
        fig_bar.update_layout(
            xaxis_title="Month",
            yaxis_title="Sales (₹)",
            hovermode="x unified",
            height=500
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("---")
        
        # Top Products
        st.subheader("🏆 Top 10 Products by Sales")
        top_products = df.groupby("Product Name")["Sales Price"].sum().sort_values(ascending=False).head(10).reset_index()
        
        fig_top = px.bar(
            top_products,
            x='Sales Price',
            y='Product Name',
            orientation='h',
            color='Sales Price',
            color_continuous_scale='Viridis'
        )
        fig_top.update_layout(height=400)
        st.plotly_chart(fig_top, use_container_width=True)

# ================== FORECAST PAGE ==================
elif page == "🔮 Forecast Sales":
    if not st.session_state.authenticated:
        st.error("❌ Please login first!")
    elif st.session_state.data is None:
        st.warning("⚠️ Please upload a CSV file first!")
        if st.button("📂 Go to Upload"):
            st.session_state.page = "📂 Upload CSV File"
            st.rerun()
    else:
        df = st.session_state.data.copy()
        
        st.subheader("🔮 Sales Forecasting")
        
        # Data Preprocessing
        df['Date and Time'] = pd.to_datetime(df['Date and Time'])
        df['Day'] = df['Date and Time'].dt.day
        df['Month'] = df['Date and Time'].dt.month
        df['Year'] = df['Date and Time'].dt.year
        df['Profit'] = df['Sales Price'] - df['Discounted Price']
        
        # Select Category for Forecast
        selected_category = st.selectbox("Select Category to Forecast:", df['Category'].unique())
        filtered_df = df[df['Category'] == selected_category].copy()
        
        if len(filtered_df) < 10:
            st.warning("⚠️ Not enough data for forecasting. Need at least 10 records.")
        else:
            # Prepare data for ML model
            X = filtered_df[['Day', 'Month', 'Year', 'Quantity Purchased']].values
            y = filtered_df['Sales Price'].values
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Train Random Forest Model
            model = RandomForestRegressor(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            # Predictions
            y_pred_test = model.predict(X_test)
            
            # Metrics
            mse = mean_squared_error(y_test, y_pred_test)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, y_pred_test)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("R² Score", f"{r2:.4f}")
            with col2:
                st.metric("RMSE", f"₹{rmse:,.2f}")
            with col3:
                st.metric("Model Accuracy", f"{(r2 * 100):.2f}%")
            
            st.markdown("---")
            
            # Forecast visualization
            st.subheader("📈 Forecast vs Actual Sales")
            
            forecast_df = pd.DataFrame({
                'Actual': y_test,
                'Predicted': y_pred_test,
                'Index': range(len(y_test))
            })
            
            fig_forecast = go.Figure()
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['Index'],
                y=forecast_df['Actual'],
                mode='lines+markers',
                name='Actual Sales',
                line=dict(color='blue', width=2)
            ))
            fig_forecast.add_trace(go.Scatter(
                x=forecast_df['Index'],
                y=forecast_df['Predicted'],
                mode='lines+markers',
                name='Predicted Sales',
                line=dict(color='red', width=2, dash='dash')
            ))
            
            fig_forecast.update_layout(
                title=f"Sales Forecast for {selected_category}",
                xaxis_title="Test Sample",
                yaxis_title="Sales (₹)",
                height=500,
                hovermode='x unified'
            )
            st.plotly_chart(fig_forecast, use_container_width=True)
            
            # Feature Importance
            st.subheader("🎯 Feature Importance")
            feature_names = ['Day', 'Month', 'Year', 'Quantity Purchased']
            importances = model.feature_importances_
            
            fig_importance = px.bar(
                x=importances,
                y=feature_names,
                orientation='h',
                color=importances,
                color_continuous_scale='Viridis'
            )
            fig_importance.update_layout(height=300)
            st.plotly_chart(fig_importance, use_container_width=True)

# ================== LOGOUT ==================
if st.session_state.authenticated:
    if st.sidebar.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.data = None
        st.session_state.page = "🔐 Login"
        st.rerun()

# ================== FOOTER ==================
st.markdown("""
---
<div style="text-align: center; color: gray; font-size: 12px; margin-top: 30px;">
    <p>© 2024 A1 Mart Sales Forecasting | Built with Streamlit & Machine Learning</p>
</div>
""", unsafe_allow_html=True)
