import matplotlib.pyplot as plt
import numpy as np

# Şubat ayı kar yağışı ve tatil günleri verileri
years = list(range(2010, 2026))
snow_days = {
    2010: [2, 3],
    2011: [],
    2012: [1, 2, 8, 9, 10, 15, 17, 18, 28],
    2013: [],
    2014: [],
    2015: [19, 18, 17, 12, 11, 10],
    2016: [],
    2017: [14, 13, 12],
    2018: [27],
    2019: [24, 23],
    2020: [8, 6],
    2021: [17, 16, 15, 14],
    2022: [],
    2023: [8, 7, 6, 5],
    2024: [],
    2025: [5, 6, 7, 8]  # 2025 yılı için eklenen tahmini veriler
}
holiday_days = {
    2010: [2],
    2011: [],
    2012: [1, 2, 28],
    2013: [],
    2014: [],
    2015: [19, 18, 17, 10],
    2016: [],
    2017: [],
    2018: [],
    2019: [24, 23],
    2020: [],
    2021: [17, 16],
    2022: [],
    2023: [8, 7, 5],
    2024: [],
    2025: [6, 7]  # 2025 yılı için tatil verileri
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
probability_snow_holiday_final = (probability_holiday_given_snow * probability_snow_holiday) / 100  # Bu kar yağışında tatil olma olasılığı

# Valinin görev süresinin sona erme olasılığı (varsayımsal veri)
governor_resign_probability = {
    2020: 5,  # %5
    2021: 6,  # %6
    2022: 7,  # %7
    2023: 8   # %8
}

# Yeni olasılık: Okulun tatil olma olasılığı * Valinin görev süresinin sona erme olasılığı
probability_snow_holiday_with_governor = {
    year: (probability_snow_holiday_final * governor_resign_probability[year]) / 100 for year in governor_resign_probability
}

# Tüm yıllar için okulun tatil olma olasılığının ortalaması
average_probability_snow_holiday_with_governor = np.mean(list(probability_snow_holiday_with_governor.values()))

# Grafik çizimi
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 12))

# Şubat ayı kar yağışı ve tatil günleri grafiği
snow_counts = [len(days) for days in snow_days.values()]
holiday_counts = [len(days) for days in holiday_days.values()]
snow_holiday_counts = [len(set(snow_days[year]).intersection(set(holiday_days[year]))) for year in years]
x = np.arange(len(years))
width = 0.25

rects1 = ax1.bar(x - width, snow_counts, width, label='Kar Yağışı Günleri')
rects2 = ax1.bar(x, holiday_counts, width, label='Tatil Olan Günler')
rects3 = ax1.bar(x + width, snow_holiday_counts, width, label='Kar Tatili Günleri')

ax1.set_xlabel('Yıl')
ax1.set_ylabel('Gün Sayısı')
ax1.set_title('Şubat Ayında Kar Yağışı, Tatil ve Kar Tatili Günleri')
ax1.set_xticks(x)
ax1.set_xticklabels(years, rotation=45)
ax1.legend()

# Olasılıkları grafikte gösterme
ax1.text(0.02, 0.95, f'Kar Yağma Olasılığı: {probability_snow:.2f}%', transform=ax1.transAxes, fontsize=10, verticalalignment='top')
ax1.text(0.02, 0.90, f'Tatil Olma Olasılığı: {probability_any_holiday:.2f}%', transform=ax1.transAxes, fontsize=10, verticalalignment='top')
ax1.text(0.02, 0.85, f'Kar Tatili Olasılığı: {probability_snow_holiday:.2f}%', transform=ax1.transAxes, fontsize=10, verticalalignment='top')
ax1.text(0.02, 0.80, f'Bu Kar Yağışında Tatil Olasılığı: {probability_snow_holiday_final:.2f}%', transform=ax1.transAxes, fontsize=10, verticalalignment='top')

# Valinin görev süresinin sona erme olasılığı ve okulun tatil olma olasılığı grafiği
ax2.plot(governor_resign_probability.keys(), [probability_snow_holiday_with_governor[year] for year in governor_resign_probability], label='Okulun Tatil Olma Olasılığı (Vali Görev Süresi Sona Erme ile)', marker='o', color='green')
ax2.axhline(average_probability_snow_holiday_with_governor, color='red', linestyle='--', label=f'Tüm Yıllar Ortalaması: {average_probability_snow_holiday_with_governor:.2f}%')
ax2.set_xlabel('Yıl')
ax2.set_ylabel('Olasılık (%)')
ax2.set_title('Okulun Tatil Olma Olasılığı (Valinin Görev Süresi Sona Erme Olasılığı ile)')
ax2.set_xticks(list(governor_resign_probability.keys()))
ax2.legend()

plt.tight_layout()
plt.show()

# Sonuçları yazdır
print(f"Herhangi bir Şubat gününde kar yağma olasılığı: {probability_snow:.2f}%")
print(f"Kar yağdığında okulun tatil olma olasılığı: {probability_holiday_given_snow:.2f}%")
print(f"Herhangi bir Şubat gününde okulun tatil olma olasılığı: {probability_any_holiday:.2f}%")
print(f"Şubat aylarının tatil olmuş olma olasılığı: {probability_snow_holiday:.2f}%")
print(f"Bu kar yağışında okulun tatil olma olasılığı: {probability_snow_holiday_final:.2f}%")
print(f"Tüm yıllar için okulun tatil olma olasılığı ortalaması (Vali Görev Süresi Sona Erme ile): {average_probability_snow_holiday_with_governor:.2f}%")

for year in governor_resign_probability:
    print(f"{year} yılı için:")
    print(f"  Valinin Görev Süresi Sona Erme Olasılığı: {governor_resign_probability[year]:.2f}%")
    print(f"  Okulun Tatil Olma Olasılığı (Vali Görev Süresi Sona Erme ile): {probability_snow_holiday_with_governor[year]:.2f}%")
