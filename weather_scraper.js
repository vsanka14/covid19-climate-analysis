async function scrapeWunderGround(url) {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto(url);
    await page.waitForSelector('.observation-table');
    const weatherData = [];
    const cols = await page.$$('.observation-table > table > tbody > tr > td');
    for(let i=0; i<cols.length; i++) {
        const table = await cols[i].$('table');
        weatherData.push([]);
        const trs = await table.$$('tr');
        for(let j=0; j<trs.length; j++) {
            const td = await trs[j].$('td');
            const txt = await td.getProperty('textContent');
            const rawTxt = await txt.jsonValue();
            weatherData[i].push(rawTxt);
        }
    }
    let weatherJson = {};
    weatherData.splice(2,1);
    weatherData.splice(3);
    for(let i=1; i<weatherData[0].length; i++) {
        weatherJson[`03-${parseInt(weatherData[0][i])}-2020`] = [parseInt(weatherData[1][i]), parseInt(weatherData[2][i])];
    }
    console.log(JSON.stringify(weatherJson));
    browser.close();
}

let weatherUrl = 'https://www.wunderground.com/history/monthly/us/az/phoenix/KPHX/date/2020-3'
scrapeWunderGround(weatherUrl);