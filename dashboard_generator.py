import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

# ========== 1. ЗАГРУЗКА ДАННЫХ ==========
folder_path = r"D:\DWNLD\Раз"
df = pd.read_excel(os.path.join(folder_path, "merged_data.xlsx"))

# Очищаем данные
df['Написано профстатей'] = pd.to_numeric(df['Написано профстатей'], errors='coerce').fillna(0)
df['Реализовано крупных проектов'] = pd.to_numeric(df['Реализовано крупных проектов'], errors='coerce').fillna(0)
df['Профвыступлений'] = pd.to_numeric(df['Профвыступлений'], errors='coerce').fillna(0)

# ========== 2. НАСТРОЙКА ЦВЕТОВ ==========
colors = {
    'darkest': '#3d3814',
    'dark': '#4b4230',
    'main': '#a47a58',
    'light': '#d4a271',
    'lightest': '#f4c28a',
    'accent': '#b4c4bb'
}
color_scale = ['#3d3814', '#4b4230', '#a47a58', '#d4a271', '#f4c28a']
color_sequence = ['#3d3814', '#4b4230', '#a47a58', '#d4a271', '#b4c4bb']


# Функция для преобразования HEX в RGBA
def hex_to_rgba(hex_color, alpha=0.25):
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 6:
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return f'rgba({r}, {g}, {b}, {alpha})'
    return 'rgba(0,0,0,0.25)'


print("🚀 Создаём обновлённый дашборд с новой цветовой схемой...")

# ========== 3. СОЗДАНИЕ ГРАФИКОВ ==========
# 1. Доход по отраслям
fig1 = px.box(df, x='Отрасль', y='Annual Income, mln RUR',
              title='💰 Распределение доходов по отраслям',
              color='Отрасль',
              color_discrete_sequence=color_sequence,
              labels={'Annual Income, mln RUR': 'Доход (млн руб.)'})
fig1.update_layout(
    font=dict(color=colors['dark']),
    title_font=dict(color=colors['darkest']),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# 2. Количество сотрудников по отраслям
fig2 = px.histogram(df, x='Отрасль',
                    title='👥 Количество сотрудников по отраслям',
                    color='Отрасль',
                    color_discrete_sequence=color_sequence,
                    labels={'count': 'Количество'})
fig2.update_layout(
    font=dict(color=colors['dark']),
    title_font=dict(color=colors['darkest']),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# 3. Зависимость дохода от достижений
fig3 = px.scatter(df, x='Реализовано крупных проектов',
                  y='Annual Income, mln RUR',
                  size='Написано профстатей',
                  color='Отрасль',
                  hover_name='ФИО',
                  color_discrete_sequence=color_sequence,
                  title='📈 Доход vs Проекты (размер = кол-во статей)',
                  labels={'Реализовано крупных проектов': 'Крупных проектов',
                          'Annual Income, mln RUR': 'Доход (млн руб.)'},
                  size_max=30)
fig3.update_layout(
    font=dict(color=colors['dark']),
    title_font=dict(color=colors['darkest']),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# 4. Топ-10 сотрудников по доходу
top10 = df.nlargest(10, 'Annual Income, mln RUR')
fig4 = px.bar(top10, x='ФИО', y='Annual Income, mln RUR',
              title='🏆 Топ-10 сотрудников по доходу',
              color='Annual Income, mln RUR',
              color_continuous_scale=color_scale,
              labels={'Annual Income, mln RUR': 'Доход (млн руб.)'},
              text='Annual Income, mln RUR')
fig4.update_traces(texttemplate='%{text:.0f}', textposition='outside')
fig4.update_layout(
    font=dict(color=colors['dark']),
    title_font=dict(color=colors['darkest']),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# 5. Радар достижений для топ-5 сотрудников (ИСПРАВЛЕН)
top5 = df.nlargest(5, 'Annual Income, mln RUR')
fig5 = go.Figure()
radar_colors_hex = ['#3d3814', '#4b4230', '#a47a58', '#d4a271', '#b4c4bb']

for i, (_, row) in enumerate(top5.iterrows()):
    hex_color = radar_colors_hex[i % len(radar_colors_hex)]
    rgba_color = hex_to_rgba(hex_color, 0.25)

    fig5.add_trace(go.Scatterpolar(
        r=[row['Реализовано крупных проектов'],
           row['Профвыступлений'],
           row['Написано профстатей']],
        theta=['Проекты', 'Выступления', 'Статьи'],
        fill='toself',
        name=row['ФИО'],
        line_color=hex_color,
        fillcolor=rgba_color
    ))

fig5.update_layout(
    polar=dict(
        radialaxis=dict(
            visible=True,
            range=[0, max(df['Реализовано крупных проектов'].max(),
                          df['Профвыступлений'].max(),
                          df['Написано профстатей'].max()) * 1.1],
            color=colors['dark']
        ),
        angularaxis=dict(color=colors['dark'])
    ),
    title='🎯 Профиль достижений топ-5 сотрудников',
    showlegend=True,
    font=dict(color=colors['dark']),
    title_font=dict(color=colors['darkest']),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

# 6. Средний доход по отраслям
avg_income_by_industry = df.groupby('Отрасль')['Annual Income, mln RUR'].mean().reset_index()
fig6 = px.bar(avg_income_by_industry, x='Отрасль', y='Annual Income, mln RUR',
              title='📊 Средний доход по отраслям',
              color='Annual Income, mln RUR',
              color_continuous_scale=color_scale,
              labels={'Annual Income, mln RUR': 'Средний доход (млн руб.)'},
              text='Annual Income, mln RUR')
fig6.update_traces(texttemplate='%{text:.1f}', textposition='outside')
fig6.update_layout(
    font=dict(color=colors['dark']),
    title_font=dict(color=colors['darkest']),
    plot_bgcolor='white',
    paper_bgcolor='white'
)

print("📊 Генерируем HTML с обновлённым дизайном...")

# ========== 4. ГЕНЕРАЦИЯ HTML ==========
html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>📊 Дашборд сотрудников</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: {colors['lightest']};
            padding: 20px;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        .header {{
            background: white;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            box-shadow: 0 10px 30px rgba(61, 56, 20, 0.15);
            text-align: center;
            border: 2px solid {colors['light']};
        }}
        .header h1 {{
            font-size: 2.5em;
            color: {colors['darkest']};
        }}
        .header p {{
            color: {colors['dark']};
            font-size: 1.1em;
            margin-top: 10px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            text-align: center;
            box-shadow: 0 5px 15px rgba(61, 56, 20, 0.1);
            transition: transform 0.3s;
            border: 1px solid {colors['light']};
        }}
        .stat-card:hover {{
            transform: translateY(-5px);
            border-color: {colors['main']};
        }}
        .stat-number {{
            font-size: 2.5em;
            font-weight: bold;
            color: {colors['darkest']};
        }}
        .stat-label {{
            color: {colors['dark']};
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .chart-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-bottom: 30px;
        }}
        .chart-card {{
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(61, 56, 20, 0.1);
            border: 1px solid {colors['light']};
            transition: border-color 0.3s;
        }}
        .chart-card:hover {{
            border-color: {colors['main']};
        }}
        .full-width {{
            grid-column: 1 / -1;
        }}
        @media (max-width: 768px) {{
            .chart-grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Дашборд сотрудников</h1>
            <p>Аналитика по доходам, проектам и достижениям</p>
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{len(df)}</div>
                <div class="stat-label">👥 Всего сотрудников</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{df['Отрасль'].nunique()}</div>
                <div class="stat-label">🏢 Отраслей</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{df['Annual Income, mln RUR'].mean():.1f}</div>
                <div class="stat-label">💰 Средний доход (млн руб.)</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{df['Annual Income, mln RUR'].max():.0f}</div>
                <div class="stat-label">🏆 Максимальный доход (млн руб.)</div>
            </div>
        </div>

        <div class="chart-grid">
            <div class="chart-card">
                {fig1.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div class="chart-card">
                {fig2.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div class="chart-card">
                {fig6.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div class="chart-card">
                {fig4.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div class="chart-card full-width">
                {fig3.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
            <div class="chart-card full-width">
                {fig5.to_html(full_html=False, include_plotlyjs='cdn')}
            </div>
        </div>
    </div>
</body>
</html>
"""

# ========== 5. СОХРАНЕНИЕ ФАЙЛА ==========
output_html = os.path.join(folder_path, "index.html")
with open(output_html, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"✅ Дашборд обновлён: {output_html}")
print("📂 Откройте файл в браузере для просмотра!")
print("\n🎨 Использованы цвета из вашей палитры:")
for name, hex_color in colors.items():
    print(f"   {name}: {hex_color}")