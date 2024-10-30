import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')


def create_monthly_orders_df(df):
    monthly_orders_df = df.groupby(by=['mnth_x', 'yr_x']).agg({
        'cnt' : 'sum'
    })
    return monthly_orders_df

def create_season_orders_df(df):
    season_orders_df = df.groupby(by='season_x').cnt.sum().sort_values(ascending=False)
    return season_orders_df

def create_weather_orders_df(df):
    weather_orders_df = df.groupby(by='weathersit_x').agg({
        'cnt' : 'sum'
    })
    return weather_orders_df

def create_daily_orders_df(df):
    daily_orders_df = df.groupby(by='dteday_x').agg({
        'cnt' : 'sum'
    })
    return daily_orders_df

#Load data
all_df = pd.read_csv("https://raw.githubusercontent.com/NajmahFemalea/bike-sharing/main/dashboard/all_df.csv")


#Date column
datetime_columns = ['dteday_x']
all_df.sort_values(by='dteday_x', inplace=True)
all_df.reset_index(inplace=True)   

for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date_days = all_df['dteday_x'].min()
max_date_days = all_df['dteday_x'].max()

#Side bar
with st.sidebar:
    #Menambahkan logo
    st.image("https://img2.pngdownload.id/20171127/0ed/cyclist-silhouette-png-clip-art-image-5a1bf9e4edd614.1848116315117828849742.jpg")

    #Mengambil start date dan end date dari date input
    start_date, end_date = st.date_input(
        label='Time Range',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days])

main_df = all_df[(all_df['dteday_x'] >= str(start_date)) & (all_df['dteday_x'] <= str(end_date))]

#Memanggil helper function
monthly_orders_df = create_monthly_orders_df(main_df)
season_orders_df = create_season_orders_df(main_df)
weather_orders_df = create_weather_orders_df(main_df)
daily_orders_df = create_daily_orders_df(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Raw Dataset all_df.csv')
st.dataframe(data=all_df, width=500, height=300)

#Questions
st.subheader('Pertanyaan Bisnis?')
st.write('''1. Apa pengaruh cuaca terhadap penyewaan sepeda?
2. Pada bulan apa saja yang paling banyak dan paling sedikit peminjaman sepeda dilakukan?
3. Pada musim apa saja yang paling banyak dan paling sedikit peminjaman sepeda dilakukan?
''')

#Hasil analisis
st.subheader('Hasil Analisis')
tab1, tab2, tab3 = st.tabs(["Pertanyaan 1", "Pertanyaan 2", "Pertanyaan 3"])
 
with tab1:
    st.header("Apa pengaruh cuaca terhadap penyewaan sepeda?")

    weather_names = ['Clear', 'Light snow/Rain', 'Misty']
    # Membuat bar chart dengan Matplotlib
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(weather_names, weather_orders_df['cnt'].values)
    ax.set_ylabel("Average Number of Daily Rentals")
    ax.set_xlabel("Weather")
    ax.set_title("Influence of Weather on Daily Bicycle Rentals", loc="center")

    # Menampilkan grafik dalam aplikasi Streamlit
    st.pyplot(fig)

    with st.expander("Conlusion"):
        st.write('''Pengaruh cuaca terhadap penyewaan sepeda : Berdasarkan grafik diatas, bisa dilihat bahwa peminjam sepeda lebih suka mengendarai sepeda pada saat cerah hari (clear) daripada mengendarai pada saat berkabut (misty) dan hujan (Light Snow/Rain).''')

with tab2:
    st.header("Pada bulan apa saja yang paling banyak dan paling sedikit peminjaman sepeda dilakukan?")
    monthly_orders_df.reset_index(inplace=True)
    month_names = monthly_orders_df['mnth_x'].tolist()
    average_rentals = monthly_orders_df['cnt'].tolist()
    
    # Membuat line chart dengan Matplotlib
    plt.figure(figsize=(10, 5))
    plt.plot(month_names, average_rentals, marker='o', linewidth=2, color="blue")
    plt.xlabel("Month")
    plt.ylabel("Average Number of Daily Rentals")
    plt.title("Influence of Month on Daily Bicycle Rentals", loc="center")
    plt.xticks(rotation=45)  # Mengatur rotasi label bulan
    
    # Menggunakan set_xticks() sebelum set_xticklabels()
    plt.xticks(ticks=range(len(month_names)), labels=month_names, fontsize=10)  # Menggunakan month_names sebagai labels
    plt.yticks(fontsize=10)
    plt.grid(True)

    # Menampilkan grafik dalam aplikasi Streamlit
    st.pyplot(plt)

    with st.expander("Conlusion"):
        st.write('''Bulan yang paling banyak dan paling sedikit dilakukan penyewaan :
        Berdasarkan grafik diatas, diketahui bahwa ada peningkatan peminjaman sepeda pada bulan February - Juni - July - September - Desember dan terjadi penurusan drastis pada bulan April dan Mei.''')

with tab3:
    st.header("Pada musim apa saja yang paling banyak dan paling sedikit peminjaman sepeda dilakukan?")
    season_names = ['Spring', 'Summer', 'Fall', 'Winter']
    season_counts = season_orders_df.values.ravel()

    # Membuat bar chart untuk musim
    plt.figure(figsize=(10, 5))
    plt.bar(season_names, season_counts)
    plt.ylabel("Average Number of Daily Rentals")
    plt.xlabel("Season")
    plt.title("Influence of Season on Daily Bicycle Rentals", loc="center")

    # Menampilkan grafik dalam aplikasi Streamlit
    st.pyplot(plt)

    with st.expander("Conlusion"):
        st.write('''Musim yang paling banyak dan paling sedikit dilakukan penyewaan : Berdasarkan grafik diatas, bisa dilihat bahwa jumlah peminjam sepeda paling banyak terdapat di musim semi/spring season dan paling sedikit pada musim salju/winter season''')

st.caption('Najmah Femalea (c) 2024')
