import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os

# Set page configuration
st.set_page_config(
    page_title="Data Analysis Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if 'loaded_dataframes' not in st.session_state:
    st.session_state.loaded_dataframes = {}

# Function to load data files 
@st.cache_data
def load_data_files(directory_path):
    """Load all CSV and Excel files from a directory"""
    loaded_dfs = {}
    
    if not os.path.exists(directory_path):
        return loaded_dfs
    
    for file_path in Path(directory_path).rglob('*'):
        if file_path.is_file() and file_path.suffix.lower() in ['.csv', '.xls', '.xlsx']:
            filename = file_path.stem
            try:
                if file_path.suffix.lower() == '.csv':
                    df = pd.read_csv(file_path)
                else:
                    df = pd.read_excel(file_path)
                loaded_dfs[filename] = df
            except Exception as e:
                st.error(f"Error loading {file_path.name}: {e}")
    
    return loaded_dfs

# Function to generate summary statistics
def generate_summary_stats(df):
    """Generate comprehensive summary statistics for a dataframe"""
    stats = {
        'Total Rows': len(df),
        'Total Columns': len(df.columns),
        'Missing Values': df.isnull().sum().sum(),
        'Duplicate Rows': df.duplicated().sum(),
        'Memory Usage (MB)': df.memory_usage(deep=True).sum() / (1024 * 1024)
    }
    return stats

# Function to create correlation heatmap
def create_correlation_heatmap(df):
    """Create an interactive correlation heatmap"""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        fig = px.imshow(corr, 
                        text_auto=True, 
                        aspect="auto",
                        color_continuous_scale='RdBu_r',
                        title="Correlation Heatmap")
        return fig
    return None

# Function to create distribution plots
def create_distribution_plot(df, column):
    """Create distribution plot for a column"""
    if pd.api.types.is_numeric_dtype(df[column]):
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=df[column], name='Distribution', nbinsx=30))
        fig.update_layout(
            title=f'Distribution of {column}',
            xaxis_title=column,
            yaxis_title='Frequency',
            showlegend=False
        )
        return fig
    else:
        value_counts = df[column].value_counts().head(20)
        fig = px.bar(x=value_counts.index, y=value_counts.values,
                     title=f'Top 20 Values in {column}',
                     labels={'x': column, 'y': 'Count'})
        return fig

# Function to create time series plot
def create_time_series_plot(df, date_col, value_col):
    """Create time series plot"""
    df_copy = df.copy()
    df_copy[date_col] = pd.to_datetime(df_copy[date_col], errors='coerce')
    df_copy = df_copy.dropna(subset=[date_col])
    df_copy = df_copy.sort_values(date_col)
    
    fig = px.line(df_copy, x=date_col, y=value_col,
                  title=f'{value_col} Over Time',
                  labels={date_col: 'Date', value_col: 'Value'})
    return fig

# Sidebar - Data Loading
st.sidebar.title("📁 Data Management")
st.sidebar.markdown("---")

# Option 1: Upload files
uploaded_files = st.sidebar.file_uploader(
    "Upload CSV/Excel files",
    type=['csv', 'xlsx', 'xls'],
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        filename = Path(uploaded_file.name).stem
        try:
            if uploaded_file.name.endswith('.csv'):
                df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
            st.session_state.loaded_dataframes[filename] = df
        except Exception as e:
            st.sidebar.error(f"Error loading {uploaded_file.name}: {e}")

# Option 2: Load from directory
st.sidebar.markdown("### Or load from directory:")
directory_path = st.sidebar.text_input(
    "Enter directory path",
    placeholder="e.g., /path/to/your/data"
)

if st.sidebar.button("Load from Directory"):
    if directory_path:
        loaded_dfs = load_data_files(directory_path)
        st.session_state.loaded_dataframes.update(loaded_dfs)
        if loaded_dfs:
            st.sidebar.success(f"Loaded {len(loaded_dfs)} file(s)")
        else:
            st.sidebar.warning("No files found in directory")

# Main content
st.title("📊 Data Analysis Dashboard")
st.markdown("---")

if not st.session_state.loaded_dataframes:
    st.info("👈 Please upload files or specify a directory path in the sidebar to begin analysis.")
else:
    # Dataset selector
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Select Dataset")
    selected_dataset = st.sidebar.selectbox(
        "Choose a dataset to analyze",
        options=list(st.session_state.loaded_dataframes.keys())
    )
    
    if selected_dataset:
        df = st.session_state.loaded_dataframes[selected_dataset]
        
        # Create tabs for different analyses
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📋 Overview", 
            "📈 Visualizations", 
            "📊 Statistics", 
            "🔍 Trends & Insights",
            "🔢 Raw Data"
        ])
        
        # Tab 1: Overview
        with tab1:
            st.header(f"Overview: {selected_dataset}")
            
            # Summary metrics
            col1, col2, col3, col4, col5 = st.columns(5)
            stats = generate_summary_stats(df)
            
            with col1:
                st.metric("Total Rows", f"{stats['Total Rows']:,}")
            with col2:
                st.metric("Total Columns", stats['Total Columns'])
            with col3:
                st.metric("Missing Values", f"{stats['Missing Values']:,}")
            with col4:
                st.metric("Duplicates", stats['Duplicate Rows'])
            with col5:
                st.metric("Memory (MB)", f"{stats['Memory Usage (MB)']:.2f}")
            
            st.markdown("---")
            
            # Column information
            st.subheader("📋 Column Information")
            col_info = pd.DataFrame({
                'Column Name': df.columns,
                'Data Type': df.dtypes.values,
                'Non-Null Count': df.count().values,
                'Null Count': df.isnull().sum().values,
                'Unique Values': [df[col].nunique() for col in df.columns]
            })
            st.dataframe(col_info, use_container_width=True)
            
            # Sample data
            st.subheader("🔍 Sample Data (First 10 Rows)")
            st.dataframe(df.head(10), use_container_width=True)
        
        # Tab 2: Visualizations
        with tab2:
            st.header("📈 Data Visualizations")
            
            # Column selector for visualizations
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                st.subheader("Single Variable Analysis")
                selected_column = st.selectbox(
                    "Select column to visualize",
                    options=df.columns.tolist(),
                    key="single_var"
                )
                
                if selected_column:
                    fig = create_distribution_plot(df, selected_column)
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Additional statistics for selected column
                    if pd.api.types.is_numeric_dtype(df[selected_column]):
                        st.markdown("**Statistics:**")
                        col_stats = df[selected_column].describe()
                        st.dataframe(col_stats, use_container_width=True)
            
            with viz_col2:
                st.subheader("Correlation Analysis")
                numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                
                if len(numeric_cols) > 1:
                    fig_corr = create_correlation_heatmap(df)
                    if fig_corr:
                        st.plotly_chart(fig_corr, use_container_width=True)
                else:
                    st.info("Not enough numeric columns for correlation analysis")
            
            # Two variable comparison
            st.markdown("---")
            st.subheader("Two Variable Comparison")
            
            comp_col1, comp_col2 = st.columns(2)
            with comp_col1:
                x_axis = st.selectbox("Select X-axis", options=df.columns.tolist(), key="x_axis")
            with comp_col2:
                y_axis = st.selectbox("Select Y-axis", options=df.columns.tolist(), key="y_axis")
            
            if x_axis and y_axis:
                if pd.api.types.is_numeric_dtype(df[x_axis]) and pd.api.types.is_numeric_dtype(df[y_axis]):
                    fig_scatter = px.scatter(df, x=x_axis, y=y_axis, 
                                            title=f'{y_axis} vs {x_axis}',
                                            trendline="ols")
                    st.plotly_chart(fig_scatter, use_container_width=True)
                else:
                    fig_box = px.box(df, x=x_axis, y=y_axis,
                                    title=f'{y_axis} by {x_axis}')
                    st.plotly_chart(fig_box, use_container_width=True)
        
        # Tab 3: Statistics
        with tab3:
            st.header("📊 Statistical Analysis")
            
            # Numeric columns statistics
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                st.subheader("Numeric Columns Summary")
                stat_option = st.selectbox(
                    "Select statistic view",
                    ["Descriptive Statistics", "Quantiles", "Value Ranges"]
                )
                
                if stat_option == "Descriptive Statistics":
                    st.dataframe(df[numeric_cols].describe(), use_container_width=True)
                elif stat_option == "Quantiles":
                    quantiles = df[numeric_cols].quantile([0.1, 0.25, 0.5, 0.75, 0.9])
                    st.dataframe(quantiles, use_container_width=True)
                else:
                    ranges = pd.DataFrame({
                        'Min': df[numeric_cols].min(),
                        'Max': df[numeric_cols].max(),
                        'Range': df[numeric_cols].max() - df[numeric_cols].min()
                    })
                    st.dataframe(ranges, use_container_width=True)
            
            # Categorical columns statistics
            st.markdown("---")
            categorical_cols = df.select_dtypes(include=['object']).columns.tolist()
            if categorical_cols:
                st.subheader("Categorical Columns Analysis")
                selected_cat = st.selectbox("Select categorical column", categorical_cols)
                
                if selected_cat:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown("**Value Counts:**")
                        value_counts = df[selected_cat].value_counts().head(15)
                        st.dataframe(value_counts, use_container_width=True)
                    
                    with col2:
                        fig_pie = px.pie(values=value_counts.values, 
                                        names=value_counts.index,
                                        title=f'Distribution of {selected_cat}')
                        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Tab 4: Trends & Insights
        with tab4:
            st.header("🔍 Trends & Insights")
            
            # Time series analysis
            st.subheader("Time Series Analysis")
            date_columns = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]
            
            if date_columns:
                ts_col1, ts_col2 = st.columns(2)
                with ts_col1:
                    date_col = st.selectbox("Select date column", date_columns)
                with ts_col2:
                    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                    value_col = st.selectbox("Select value column", numeric_cols)
                
                if date_col and value_col:
                    try:
                        fig_ts = create_time_series_plot(df, date_col, value_col)
                        st.plotly_chart(fig_ts, use_container_width=True)
                    except Exception as e:
                        st.error(f"Error creating time series: {e}")
            else:
                st.info("No date columns detected for time series analysis")
            
            # Top/Bottom insights
            st.markdown("---")
            st.subheader("Top & Bottom Values")
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            if numeric_cols:
                insight_col = st.selectbox("Select column for insights", numeric_cols, key="insights")
                n_values = st.slider("Number of values to show", 5, 20, 10)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Top {n_values} Values**")
                    top_values = df.nlargest(n_values, insight_col)[insight_col]
                    fig_top = px.bar(x=top_values.index, y=top_values.values,
                                    title=f'Top {n_values} {insight_col}')
                    st.plotly_chart(fig_top, use_container_width=True)
                
                with col2:
                    st.markdown(f"**Bottom {n_values} Values**")
                    bottom_values = df.nsmallest(n_values, insight_col)[insight_col]
                    fig_bottom = px.bar(x=bottom_values.index, y=bottom_values.values,
                                       title=f'Bottom {n_values} {insight_col}')
                    st.plotly_chart(fig_bottom, use_container_width=True)
        
        # Tab 5: Raw Data
        with tab5:
            st.header("🔢 Raw Data Explorer")
            
            # Filtering options
            st.subheader("Filter Data")
            
            filter_col1, filter_col2 = st.columns(2)
            with filter_col1:
                filter_column = st.selectbox("Select column to filter", ["None"] + df.columns.tolist())
            
            filtered_df = df.copy()
            
            if filter_column != "None":
                if pd.api.types.is_numeric_dtype(df[filter_column]):
                    min_val = float(df[filter_column].min())
                    max_val = float(df[filter_column].max())
                    filter_range = st.slider(
                        f"Filter {filter_column}",
                        min_val, max_val, (min_val, max_val)
                    )
                    filtered_df = filtered_df[
                        (filtered_df[filter_column] >= filter_range[0]) & 
                        (filtered_df[filter_column] <= filter_range[1])
                    ]
                else:
                    unique_values = df[filter_column].unique().tolist()
                    selected_values = st.multiselect(
                        f"Select {filter_column} values",
                        unique_values,
                        default=unique_values[:5] if len(unique_values) > 5 else unique_values
                    )
                    if selected_values:
                        filtered_df = filtered_df[filtered_df[filter_column].isin(selected_values)]
            
            st.markdown(f"**Showing {len(filtered_df)} of {len(df)} rows**")
            st.dataframe(filtered_df, use_container_width=True)
            
            # Download filtered data
            csv = filtered_df.to_csv(index=False)
            st.download_button(
                label="📥 Download Filtered Data as CSV",
                data=csv,
                file_name=f"{selected_dataset}_filtered.csv",
                mime="text/csv"
            )

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### 📌 About")
st.sidebar.info(
    "This dashboard allows you to explore and analyze your data with "
    "interactive visualizations, statistical summaries, and trend analysis."
)