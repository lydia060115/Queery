// 1. 手风琴折叠面板逻辑
function toggleAccordion(element) {
    const item = element.parentElement;
    
    // 关闭其他已展开的面板
    document.querySelectorAll('.accordion-item').forEach(otherItem => {
        if (otherItem !== item && otherItem.classList.contains('active')) {
            otherItem.classList.remove('active');
            otherItem.querySelector('.accordion-icon').textContent = '+';
        }
    });

    // 切换当前面板
    item.classList.toggle('active');
    const icon = element.querySelector('.accordion-icon');
    icon.textContent = item.classList.contains('active') ? '-' : '+';
}

// 2. 国家弹窗文案数据 (已扩充：美、中、加、巴、南非 + 墨、俄、英、法、德、波兰)
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
    },
    "Mexico": {
        status: "Marriage Equality / Cultural Duality",
        routine: "Marriage equality is now legal across all states. Mexico City has a vibrant, progressive LGBTQ+ scene and large Pride celebrations, yet many rural areas still grapple with deep-rooted 'machismo' culture and religious conservatism."
    },
    "Russia": {
        status: "Severe Repression / Extremist Designation",
        routine: "The situation is extremely hostile. 'Non-traditional sexual relations' propaganda laws are strictly enforced, and the international LGBTQ+ movement has been legally classified as 'extremist'. Open expression is highly dangerous, forcing communities deeply underground."
    },
    "United Kingdom": {
        status: "Legal Equality / Trans Rights Debates",
        routine: "The UK offers robust legal protections and marriage equality, with massive celebrations like Pride in London. However, in recent years, the community has faced a highly polarized political and media environment specifically surrounding transgender rights and healthcare."
    },
    "France": {
        status: "Marriage Equality / Historic Communities",
        routine: "Since passing 'Mariage pour tous' (Marriage for all) in 2013, France has solidified its legal protections. Paris boasts the historic Le Marais district and massive Pride marches (Marche des Fiertés), reflecting a largely accepting society."
    },
    "Germany": {
        status: "Marriage Equality / Progressive Hub",
        routine: "Germany legalized 'Ehe für alle' in 2017. Berlin remains one of the world's most historic and liberating hubs for queer culture, hosting massive Christopher Street Day (CSD) parades and enforcing strong anti-discrimination laws."
    },
    "Poland": {
        status: "No Legal Recognition / Political Hostility",
        routine: "While homosexuality is legal, same-sex couples have no legal recognition. The community faces significant political hostility, highlighted by the controversial 'LGBT-ideology free zones' declared by some municipalities, which have sparked intense EU pushback and resilient grassroots activism."
    }
};

// 3. 关闭底部卡片
function closeSheet() {
    document.body.classList.remove('sheet-active');
}

// 4. 监听 iframe 地图的点击消息
window.addEventListener('message', function(event) {
    if (event.data && event.data.type === 'MAP_CLICKED') {
        const clickedCountry = event.data.country;
        const data = countryData[clickedCountry];
        
        document.getElementById('sheetCountryName').textContent = clickedCountry;
        
        if (data) {
            document.getElementById('sheetStatus').textContent = data.status;
            document.getElementById('sheetStatus').style.display = 'inline-block';
            document.getElementById('sheetRoutine').textContent = data.routine;
        } else {
            document.getElementById('sheetStatus').style.display = 'none';
            document.getElementById('sheetRoutine').textContent = "We are currently compiling localized routine activities and cultural data for this region. Try tapping on highlighted countries like United States, China, Russia, Mexico, or European nations for detailed insights!";
        }
        
        // 弹出卡片
        document.body.classList.add('sheet-active');
    }
});