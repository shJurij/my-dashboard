import pandas as pd
import os

# Путь к папке с файлами
folder_path = r"D:\DWNLD\Раз"

# Загружаем файлы
df_main = pd.read_excel(os.path.join(folder_path, "Assignm1.xlsx"))
df_finance = pd.read_excel(os.path.join(folder_path, "Assignm2.xlsx"))
df_achievements = pd.read_excel(os.path.join(folder_path, "Assignm3.xlsx"))

print("="*60)
print("📊 Исходные данные")
print("="*60)
print(f"Assignm1: {df_main.shape}")
print(f"Assignm2: {df_finance.shape}")
print(f"Assignm3: {df_achievements.shape}")

# 1. Переименовываем столбец Name в ФИО в финансовом файле
df_finance = df_finance.rename(columns={'Name': 'ФИО'})

# 2. Чистим названия столбцов от лишних пробелов
df_achievements.columns = df_achievements.columns.str.strip()

# 3. Объединяем все таблицы по ФИО
df_merged = df_main.merge(df_finance, on='ФИО', how='left')
df_merged = df_merged.merge(df_achievements, on='ФИО', how='left')

print("\n" + "="*60)
print("📊 Итоговый датафрейм")
print("="*60)
print(f"Размер: {df_merged.shape[0]} строк, {df_merged.shape[1]} столбцов")
print("\nПервые 5 строк:")
print(df_merged.head())

print("\nСтолбцы:", df_merged.columns.tolist())

# 4. Проверяем, все ли сотрудники подтянулись
print("\n" + "="*60)
print("🔍 Проверка пропусков")
print("="*60)
print(df_merged.isnull().sum())

# 5. Сохраняем объединённые данные
output_file = os.path.join(folder_path, "merged_data.xlsx")
df_merged.to_excel(output_file, index=False)
print(f"\n✅ Объединённые данные сохранены в {output_file}")

# 6. Базовая статистика
print("\n" + "="*60)
print("📈 Базовая статистика по финансам")
print("="*60)
print(df_merged['Annual Income, mln RUR'].describe())