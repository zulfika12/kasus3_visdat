import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Konfigurasi Halaman
st.set_page_config(
    page_title="Bedah Kasus 3 - Pengamatan Cuaca",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Load Data
@st.cache_data
def load_data():
    return pd.read_csv("dataset_pengamatan_cuaca.csv")

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat dataset_pengamatan_cuaca.csv: {e}")
    st.stop()

# 3. Sidebar Filter
st.sidebar.title("📌 Filter Cuaca")

kota_list = list(df['Kota'].unique())
kota_filter = st.sidebar.multiselect(
    "Pilih Kota:",
    options=kota_list,
    default=kota_list
)

kondisi_list = list(df['Kondisi'].unique())
kondisi_filter = st.sidebar.multiselect(
    "Pilih Kondisi Cuaca:",
    options=kondisi_list,
    default=kondisi_list
)

filtered_df = df[
    (df['Kota'].isin(kota_filter)) &
    (df['Kondisi'].isin(kondisi_filter))
]

# 4. Header & KPI Metrics
st.title("🌤️ Bedah Kasus 3: Dataset Pengamatan Cuaca")
st.caption("Visualisasi Data Nominal (Kota & Kondisi), Interval (Suhu), dan Rasio (Kelembaban)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Stasiun/Kota", f"{len(filtered_df)} stasiun")
with col2:
    avg_temp = filtered_df['Suhu (°C)'].mean() if len(filtered_df) > 0 else 0
    st.metric("Rata-rata Suhu", f"{avg_temp:.1f} °C")
with col3:
    avg_hum = filtered_df['Kelembaban (%)'].mean() if len(filtered_df) > 0 else 0
    st.metric("Rata-rata Kelembaban", f"{avg_hum:.1f} %")
with col4:
    max_temp = filtered_df['Suhu (°C)'].max() if len(filtered_df) > 0 else 0
    st.metric("Suhu Tertinggi", f"{max_temp:.1f} °C")

st.markdown("---")

# 5. Tab Visualisasi Bedah Kasus 3
tab1, tab2, tab3, tab4 = st.tabs([
    "🏷️ Nominal (Kota & Kondisi)", 
    "🌡️ Interval (Suhu)", 
    "💧 Rasio (Kelembaban)", 
    "📋 Data Mentah"
])

# Tab 1: Kategorik Nominal (Kota & Kondisi)
with tab1:
    st.subheader("1. Distribusi Kondisi Cuaca & Kota (Kategorik Nominal)")
    st.write("*Tipe Data: Nominal | Visualisasi: Bar Chart & Pie Chart*")
    
    col_a, col_b = st.columns(2)
    with col_a:
        kondisi_df = filtered_df['Kondisi'].value_counts().reset_index()
        kondisi_df.columns = ['Kondisi', 'Jumlah Kota']
        fig_bar_kondisi = px.bar(
            kondisi_df, x='Kondisi', y='Jumlah Kota',
            title='Jumlah Kota Berdasarkan Kondisi Cuaca',
            color='Kondisi',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        st.plotly_chart(fig_bar_kondisi, use_container_width=True)
        
    with col_b:
        fig_pie_kondisi = px.pie(
            kondisi_df, values='Jumlah Kota', names='Kondisi',
            title='Proporsi Kondisi Cuaca',
            hole=0.4
        )
        st.plotly_chart(fig_pie_kondisi, use_container_width=True)

# Tab 2: Numerik - Interval (Suhu)
with tab2:
    st.subheader("2. Analisis Suhu Per Kota (Numerik Interval)")
    st.write("*Tipe Data: Interval (0°C bukan arti 'tidak ada suhu') | Visualisasi: Bar Chart / Histogram*")
    
    fig_temp = px.bar(
        filtered_df, x='Kota', y='Suhu (°C)',
        color='Kondisi',
        title='Tingkat Suhu per Kota (°C)',
        text_auto='.1f',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    fig_temp.update_layout(xaxis_title="Kota", yaxis_title="Suhu (°C)")
    st.plotly_chart(fig_temp, use_container_width=True)

# Tab 3: Numerik - Rasio (Kelembaban vs Suhu)
with tab3:
    st.subheader("3. Perbandingan Suhu (Interval) vs Kelembaban (Rasio)")
    st.write("*Tipe Data: Rasio (0% berarti benar-benar tidak ada kelembaban) | Visualisasi: Scatter Plot*")
    
    fig_scatter = px.scatter(
        filtered_df, x='Suhu (°C)', y='Kelembaban (%)',
        color='Kondisi', text='Kota', size='Kelembaban (%)',
        title='Hubungan Suhu (°C) vs Kelembaban (%)',
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_scatter.update_traces(textposition='top center')
    st.plotly_chart(fig_scatter, use_container_width=True)

# Tab 4: Data Mentah
with tab4:
    st.subheader("📋 Explorer Data Mentah Pengamatan Cuaca")
    st.dataframe(filtered_df, use_container_width=True)
    
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Unduh Data Cuaca (CSV)",
        data=csv,
        file_name='data_pengamatan_cuaca.csv',
        mime='text/csv',
    )