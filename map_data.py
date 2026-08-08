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
    range_color=[0, 100],
    title=None 
)

# 3. 移动端终极排版优化（核心修复区）
fig.update_layout(
    geo=dict(
        showframe=False, 
        showcoastlines=True,
        bgcolor='rgba(0,0,0,0)',
        # 默认将地图适度放大，并调整初始中心点，使其充满屏幕
        projection_scale=1.1,
        center=dict(lat=20, lon=0)
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    # 将四周的白边距彻底清零，把所有空间还给地图
    margin=dict(r=0, t=0, l=0, b=0),
    dragmode="pan",
    # 强制控制颜色图例（长条）的尺寸和位置
    coloraxis_colorbar=dict(
        title="",             # 隐藏顶部标题以节省空间
        thickness=10,         # 将长条变得非常细（宽度仅 10px）
        len=0.75,             # 长度占据容器的 75%
        x=1.0,                # 紧紧贴在最右侧边缘
        xanchor="right",
        y=0.5,                # 垂直居中
        yanchor="middle",
        tickfont=dict(size=10) # 缩小刻度数字的字号
    )
)

# 4. 注入点击事件脚本并导出
html_string = fig.to_html(full_html=True, include_plotlyjs='cdn')

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

print("🎉 Success! interactive_map.html has been generated with mobile layout fixes.")