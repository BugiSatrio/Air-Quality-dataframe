import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import streamlit as st

all_data = pd.read_csv("data.csv")

st.title('Dashboard :rocket:')
st.write('Selamat datang di dashboard aplikasi pengukuran kualitas udara di beijing')

st.dataframe(all_data)

st.header('Kualitas Udara Terbaik Dan Terburuk 💨')
st.write('Menampilkan kualitas udara yang terbaik dan terburuk')

columns_to_consider = ['PM2.5', 'PM10', 'SO2', 'CO', 'O3', 'WSPM']
station_avg = all_data.groupby('station')[columns_to_consider].mean()

station_avg['overall_avg'] = station_avg.mean(axis=1)

station_avg_sorted = station_avg['overall_avg'].sort_values(ascending=False)

best_station = station_avg_sorted.idxmin()
worst_station = station_avg_sorted.idxmax()

plt.figure(figsize=(12, 8))
bar = station_avg_sorted.plot(kind='barh', color='skyblue')

bars = bar.patches

best_station_index = station_avg_sorted.index.get_loc(best_station)
worst_station_index = station_avg_sorted.index.get_loc(worst_station)

bars[best_station_index].set_color('green')
bars[worst_station_index].set_color('red')

plt.xlabel('Rata-rata Kualitas Udara')
plt.ylabel('')
plt.tight_layout()

st.pyplot(plt)

all_data['date'] = pd.to_datetime(all_data['date'])
all_data['year'] = all_data['date'].dt.year

params = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
yearly_avg = all_data.groupby('year')[params].mean()

yearly_avg_norm = (yearly_avg - yearly_avg.min()) / (yearly_avg.max() - yearly_avg.min())
yearly_avg_norm.index = yearly_avg_norm.index.astype(int)

st.header("Grafik Kualitas Udara per Tahun 📊")
st.write("Menampilkan kualitas udara dari tahun ke tahun.")

selected_param = st.selectbox("Pilih Parameter", options=yearly_avg_norm.columns)

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(yearly_avg_norm.index, yearly_avg_norm[selected_param], marker='o', linestyle='-', color='skyblue')
ax.set_title(f"Grafik {selected_param} per Tahun")
ax.set_xlabel('Tahun')
ax.set_ylabel('Nilai Ternormalisasi')
ax.grid(True)
ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))

st.pyplot(fig)