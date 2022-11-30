import plotly.express as px

def makeBar(data):
    # Создание диаграммы
    fig = px.bar(data, x='Name', y='Uptime, %', title='Uptime Statistics')
    fig.write_image("sources/BarChart.png")