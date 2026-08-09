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
        projection_scale=1.2, 
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(r=0, t=0, l=0, b=0), 
    dragmode="pan",
    autosize=True, # 强制自适应大小
    coloraxis_colorbar=dict(
        title=None,           
        thickness=8,          
        len=0.7,              
        x=0.98,               
        xanchor="right",
        y=0.5,
        yanchor="middle",
        tickfont=dict(size=10, color="#666"),
        outlinewidth=0        
    )
)

# 4. 关键更新：开启 responsive，设置默认宽高为 100%
html_string = fig.to_html(
    full_html=True, 
    include_plotlyjs='cdn', 
    config={'displayModeBar': False, 'responsive': True},
    default_width='100%',
    default_height='100%'
)

# 注入消除滚动条和强制撑满的 CSS 以及点击事件
custom_js = """
<style>
    /* 强制 iframe 内部的地图元素 100% 填满，不留白边 */
    body, html { margin: 0; padding: 0; height: 100%; overflow: hidden; background-color: #FAF9F6; }
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

print("🎉 Success! 手机端自适应修复版地图已生成！")