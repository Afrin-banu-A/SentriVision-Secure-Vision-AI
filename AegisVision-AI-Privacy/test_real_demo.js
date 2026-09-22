const puppeteer = require('puppeteer-core');

(async () => {
    const browser = await puppeteer.launch({
        executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
        headless: "new"
    });
    const page = await browser.newPage();
    await page.goto('http://127.0.0.1:5500/demo.html');

    const result = await page.evaluate(() => {
        let walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
        let node;
        let textContent = [];

        while (node = walker.nextNode()) {
            let parentName = node.parentNode ? node.parentNode.nodeName.toUpperCase() : '';
            if (parentName !== 'SCRIPT' && parentName !== 'STYLE' && parentName !== 'NOSCRIPT') {
                let txt = node.nodeValue.trim();
                if (txt.length > 0) {
                    textContent.push(txt);
                }
            }
        }
        return textContent;
    });

    console.log(JSON.stringify(result, null, 2));
    await browser.close();
})();
