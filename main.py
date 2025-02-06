    2024: [],
    2025: [7]  # 2025 yılı için tatil verileri
}

# Toplam gün sayılarını hesapla
total_february_days = len(years) * 28  # Şubat ayı 28 gün kabul edildi
total_snow_days = sum(len(days) for days in snow_days.values())
total_holiday_days = sum(len(days) for days in holiday_days.values())

# Kar tatili günlerini hesapla (hem kar yağdı hem tatil)
snow_holiday_days = 0
for year in years:
    snow_holiday_days += len(set(snow_days[year]).intersection(set(holiday_days[year])))

# Toplam Şubat ayı sayısı
total_february_months = len(years)

# En az bir gün tatil olan Şubat aylarını sayma
total_holiday_february_months = sum(1 for year in years if len(holiday_days[year]) > 0)

# Olasılık hesaplamaları
probability_snow = (total_snow_days / total_february_days) * 100  # Herhangi bir Şubat gününde kar yağma olasılığı
probability_holiday_given_snow = (snow_holiday_days / total_snow_days) * 100  # Kar yağdığında tatil olma olasılığı
probability_any_holiday = (total_holiday_days / total_february_days) * 100  # Herhangi bir Şubat gününde tatil olma olasılığı
probability_snow_holiday = (total_holiday_february_months / total_february_months) * 100  # Şubat aylarının tatil olmuş olma olasılığı

# Yeni eklenen olasılık hesaplaması
probability_snow_holiday_final = (probability_holiday_given_snow * probability_snow_holiday) / 100

# Sonuçları yazdır
print(f"Herhangi bir Şubat gününde kar yağma olasılığı: {probability_snow:.2f}%")
print(f"Kar yağdığında okulun tatil olma olasılığı: {probability_holiday_given_snow:.2f}%")
print(f"Herhangi bir Şubat gününde okulun tatil olma olasılığı: {probability_any_holiday:.2f}%")
print(f"Şubat aylarının tatil olmuş olma olasılığı: {probability_snow_holiday:.2f}%")
print(f"Bu kar yağışında okulun tatil olma olasılığı: {probability_snow_holiday_final:.2f}%")

# Grafik çizimi
snow_counts = [len(days) for days in snow_days.values()]
holiday_counts = [len(days) for days in holiday_days.values()]
snow_holiday_counts = [len(set(snow_days[year]).intersection(set(holiday_days[year]))) for year in years]

x = np.arange(len(years))
width = 0.25

fig, ax = plt.subplots()
rects1 = ax.bar(x - width, snow_counts, width, label='Kar Yağışı Günleri')
rects2 = ax.bar(x, holiday_counts, width, label='Tatil Olan Günler')
rects3 = ax.bar(x + width, snow_holiday_counts, width, label='Kar Tatili Günleri')

# Olasılıkları grafikte gösterme
ax.text(0.02, 0.95, f'Kar Yağma Olasılığı: {probability_snow:.2f}%', transform=ax.transAxes, fontsize=10, verticalalignment='top')
ax.text(0.02, 0.90, f'Tatil Olma Olasılığı: {probability_any_holiday:.2f}%', transform=ax.transAxes, fontsize=10, verticalalignment='top')
ax.text(0.02, 0.85, f'Kar Tatili Olasılığı: {probability_snow_holiday:.2f}%', transform=ax.transAxes, fontsize=10, verticalalignment='top')
ax.text(0.02, 0.80, f'Bu Kar Yağışında Tatil Olasılığı: {probability_snow_holiday_final:.2f}%', transform=ax.transAxes, fontsize=10, verticalalignment='top')

ax.set_xlabel('Yıl')
ax.set_ylabel('Gün Sayısı')
ax.set_title('Şubat Ayında Kar Yağışı, Tatil ve Kar Tatili Günleri')
ax.set_xticks(x)
ax.set_xticklabels(years, rotation=45)
ax.legend()

fig.tight_layout()
plt.show()
