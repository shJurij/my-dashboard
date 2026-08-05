import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ========== 1. ЗАГРУЗКА ДАННЫХ ==========
# Используем текущую папку проекта
folder_path = os.getcwd()  # или просто "."

# Читаем исходные файлы
df_main = pd.read_excel(os.path.join(folder_path, "Assignm1.xlsx"))
df_finance = pd.read_excel(os.path.join(folder_path, "Assignm2.xlsx"))
df_achievements = pd.read_excel(os.path.join(folder_path, "Assignm3.xlsx"))

# Объединяем данные
df_finance = df_finance.rename(columns={'Name': 'ФИО'})
df_achievements.columns = df_achievements.columns.str.strip()
df_merged = df_main.merge(df_finance, on='ФИО', how='left')
df_merged = df_merged.merge(df_achievements, on='ФИО', how='left')

# Очищаем данные
df_merged['Написано профстатей'] = pd.to_numeric(df_merged['Написано профстатей'], errors='coerce').fillna(0)
df_merged['Реализовано крупных проектов'] = pd.to_numeric(df_merged['Реализовано крупных проектов'], errors='coerce').fillna(0)
df_merged['Профвыступлений'] = pd.to_numeric(df_merged['Профвыступлений'], errors='coerce').fillna(0)

# Сохраняем объединённые данные (опционально)
df_merged.to_excel(os.path.join(folder_path, "merged_data.xlsx"), index=False)

# ========== 2. ДАЛЬШЕ ИДЁТ ВЕСЬ ОСТАЛЬНОЙ ВАШ КОД С ГРАФИКАМИ ==========
# (Здесь должен быть ваш код с fig1, fig2, fig3, fig4, fig5, fig6)
# ...

# ========== 3. СОХРАНЕНИЕ HTML ==========
output_html = os.path.join(folder_path, "index.html")
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Дашборд создан: {output_html}")