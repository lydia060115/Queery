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

# 3. 终极移动端排版调优
fig.update_layout(
    geo=dict(
        showframe=False, 
        showcoastlines=True,
        bgcolor='rgba(0,0,0,0)',
        projection_type='natural earth', # 使用更圆润自然的地球投影
        lataxis_range=[-55, 85],         # 【猛药1】强制裁掉南极洲和极北冰洋，瞬间消灭上下巨大白边！
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(r=0, t=10, l=0, b=40),   # 底部留出 40px 空间给颜色条
    dragmode="pan",
    autosize=True,
    
    # 【猛药2】颜色条改成“横向 (Horizontal)”，乖乖躺在地图下方，绝不遮挡！
    coloraxis_colorbar=dict(
        title=None,           
        orientation="h",      # 横向排列
        thickness=8,          
        len=0.8,              
        x=0.5,                # 居中对齐
        xanchor="center",
        y=-0.1,               # 放在地图区域的最下方
        yanchor="top",
        tickfont=dict(size=10, color="#666"),
        outlinewidth=0        
    )
)

# 4. 导出并注入控制滑动的 CSS
html_string = fig.to_html(
    full_html=True, 
    include_plotlyjs='cdn', 
    config={'displayModeBar': False, 'responsive': True}
)

custom_js = """
<style>
    /* 【猛药3】touch-action: none; 彻底屏蔽系统默认滑动，解决拖拽地图“发抖”的 Bug */
    body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; background-color: #FAF9F6; touch-action: none; }
    .plotly-graph-div { height: 100% !important; width: 100% !important; }
</style>
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

print("🎉 Success! 地图防抖、横向渐变条、去白边版本已生成！")