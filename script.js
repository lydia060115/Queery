// 1. 手风琴折叠面板逻辑
function toggleAccordion(element) {
    const item = element.parentElement;
    
    // 关闭其他已展开的面板，保持页面整洁
    document.querySelectorAll('.accordion-item').forEach(otherItem => {
        if (otherItem !== item && otherItem.classList.contains('active')) {
            otherItem.classList.remove('active');
            otherItem.querySelector('.accordion-icon').textContent = '+';
        }
    });

    // 切换当前面板状态
    item.classList.toggle('active');
    const icon = element.querySelector('.accordion-icon');
    icon.textContent = item.classList.contains('active') ? '-' : '+';
}

// 2. 核心国家文案数据库 (JSON格式) - 新增了美国和中国，内容更丰富！
const countryData = {
    "United States": {
        status: "Federal Marriage Equality / Polarized Reality",
        routine: "June is nationally recognized as Pride Month, featuring massive celebrations like NYC Pride (honoring the 1969 Stonewall legacy). However, the reality is highly polarized: while blue states offer robust legal protections, recent years have seen a surge in state-level legislation targeting transgender rights, meaning the LGBTQ+ experience varies drastically depending on the state you live in."
    },
    "China": {
        status: "No Legal Recognition / Grassroots Resilience",
        routine: "While there is no nationwide marriage equality and media censorship of LGBTQ+ topics exists, vibrant communities thrive in major cities. Although large public events like Shanghai Pride have been paused, grassroots activism and private social events continue. Innovatively, many same-sex couples use 'Mutual Guardianship' (意定监护) agreements as a legal workaround to secure basic medical decision-making and property rights."
    },
    "Canada": {
        status: "Marriage Equality & Protections",
        routine: "Toronto Pride is one of the largest globally, with high-level government officials regularly participating. The country has comprehensive anti-discrimination laws reflecting strong societal acceptance."
    },
    "Brazil": {
        status: "Marriage Equality",
        routine: "While São Paulo hosts the world's largest Pride parade, Brazil paradoxically faces some of the highest rates of violence against transgender individuals, highlighting a stark gap between legal rights and lived reality."
    },
    "South Africa": {
        status: "Marriage Equality (Only one in Africa)",
        routine: "The constitution explicitly protects against discrimination based on sexual orientation. However, grassroots organizations continuously work to overcome deep-rooted tribal and cultural resistance in local communities."
    }
};

// 3. 关闭底部滑动弹窗
function closeSheet() {
    document.body.classList.remove('sheet-active');
}

// 4. 监听 Python 地图 iframe 发送的点击消息
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'MAP_CLICKED') {
        const clickedCountry = event.data.country;
        const data = countryData[clickedCountry];
        
        // 填充国家名字
        document.getElementById('sheetCountryName').textContent = clickedCountry;
        
        if (data) {
            // 如果在我们设定的数据库里，显示对应的 Routine activities
            document.getElementById('sheetStatus').textContent = data.status;
            document.getElementById('sheetStatus').style.display = 'inline-block';
            document.getElementById('sheetRoutine').textContent = data.routine;
        } else {
            // 如果没在数据库里，显示通用提示
            document.getElementById('sheetStatus').style.display = 'none';
            document.getElementById('sheetRoutine').textContent = "We are currently compiling localized routine activities and cultural data for this region. Try tapping on highlighted countries like United States, China, Canada, Brazil, or South Africa for detailed insights!";
        }
        
        // 触发 CSS 动画，弹出底部卡片
        document.body.classList.add('sheet-active');
    }
});