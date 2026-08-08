import pandas as pd
import plotly.express as px

# 1. Load the dataset
df = pd.read_csv('lgbt-legal-equality-index.csv')

# 2. Data Preprocessing
latest_year = df['Year'].max()
df_latest = df[df['Year'] == latest_year].dropna(subset=['Code'])

index_col = df.columns[3]

# 3. Draw the interactive map
fig = px.choropleth(
    df_latest,
    locations="Code",
    color=index_col,
    hover_name="Entity",
    color_continuous_scale=px.colors.sequential.Sunset, 
    range_color=[0, 100],
    # 隐藏默认的标题，让网页看起来更干净
    title=None 
)

fig.update_layout(
    geo=dict(
        showframe=False, 
        showcoastlines=True,
        bgcolor='rgba(0,0,0,0)'
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    margin={"r":0,"t":0,"l":0,"b":0},
    dragmode="pan"
)

# 4. 生成 HTML 字符串，并注入点击事件监听器
# 这是非常关键的一步：利用 Plotly 的 js 接口捕获点击，并通过 postMessage 发送给父页面
html_string = fig.to_html(full_html=True, include_plotlyjs='cdn')

custom_js = """
<script>
    // 等待图表加载完成
    setTimeout(function() {
        var myPlot = document.querySelector('.plotly-graph-div');
        if (myPlot) {
            myPlot.on('plotly_click', function(data){
                // 提取点击的国家名称
                var countryName = data.points[0].hovertext;
                // 向外层的 index.html 发送消息
                window.parent.postMessage({
                    type: 'MAP_CLICKED',
                    country: countryName
                }, '*');
            });
        }
    }, 1000);
</script>
"""

# 将自定义脚本添加到 HTML 末尾
final_html = html_string.replace('</body>', f'{custom_js}</body>')

# 保存为文件
with open("interactive_map.html", "w", encoding="utf-8") as f:
    f.write(final_html)

print("🎉 Success! interactive_map.html has been generated with click events enabled.")