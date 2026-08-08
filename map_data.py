import pandas as pd
import plotly.express as px

# 1. 读取数据
df = pd.read_csv('lgbt-legal-equality-index.csv')
latest_year = df['Year'].max()
df_latest = df[df['Year'] == latest_year].dropna(subset=['Code'])
index_col = df.columns[3]

# 2. 绘制基础地图
fig = px.choropleth(
    df_latest,
    locations="Code",
    color=index_col,
    hover_name="Entity",
    color_continuous_scale=px.colors.sequential.Sunset, 
    range_color=[0, 100]
)

# 3. 终极排版优化
fig.update_layout(
    geo=dict(
        showframe=False, 
        showcoastlines=True,
        bgcolor='rgba(0,0,0,0)',
        projection_scale=1.2, # 稍微放大初始地图
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(r=0, t=0, l=0, b=0), # 边距彻底清零
    dragmode="pan",
    # 强制图例长条紧贴右侧且极细
    coloraxis_colorbar=dict(
        title=None,           # 完全去掉标题
        thickness=8,          # 极细（只有 8px 宽）
        len=0.7,              # 缩短一点，留出上下空间
        x=0.98,               # 贴紧最右侧
        xanchor="right",
        y=0.5,
        yanchor="middle",
        tickfont=dict(size=10, color="#666"),
        outlinewidth=0        # 去除长条边框，更清爽
    )
)

# 4. 关键：导出时，强制隐藏右上角的原生态工具栏 (displayModeBar: False)
html_string = fig.to_html(full_html=True, include_plotlyjs='cdn', config={'displayModeBar': False})

custom_js = """
<script>
    setTimeout(function() {
        var myPlot = document.querySelector('.plotly-graph-div');
        if (myPlot) {
            myPlot.on('plotly_click', function(data){
                var countryName = data.points[0].hovertext;
                window.parent.postMessage({
                    type: 'MAP_CLICKED',
                    country: countryName
                }, '*');
            });
        }
    }, 1000);
</script>
"""

final_html = html_string.replace('</body>', f'{custom_js}</body>')

with open("interactive_map.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("🎉 Success! 终极版地图已生成！")