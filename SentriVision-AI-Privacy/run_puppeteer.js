const puppeteer = require('puppeteer');
const path = require('path');

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
    console.log("Starting Puppeteer test...");
    const extensionPath = path.join(__dirname, 'extension');

    const browser = await puppeteer.launch({
        headless: "new",
        args: [
            `--disable-extensions-except=${extensionPath}`,
            `--load-extension=${extensionPath}`
        ]
    });

    const page = await browser.newPage();
    console.log("Navigating to demo page...");
    await page.goto('http://127.0.0.1:5500/demo.html');
    await wait(2000); // let extension load

    const targets = browser.targets();
    let extensionId = '';
    
    // Find extension id by iterating through all targets
    for (let target of targets) {
        if (target.url().startsWith('chrome-extension://')) {
            extensionId = target.url().split('/')[2];
            break;
        }
    }
    
    console.log("Extension ID: " + extensionId);
    if (!extensionId) {
        console.error("Could not find extension ID.");
        await browser.close();
        return;
    }

    const popupPage = await browser.newPage();
    console.log("Navigating to popup...");
    await popupPage.goto(`chrome-extension://${extensionId}/popup/popup.html`);

    let sanitizeCount = 0;
    let aiProcessCount = 0;

    popupPage.on('request', request => {
        if (request.url().includes('/sanitize')) {
            sanitizeCount++;
            console.log("-> Intercepted /sanitize request: " + sanitizeCount);
        }
        if (request.url().includes('/ai/process')) {
            aiProcessCount++;
            console.log("-> Intercepted /ai/process request: " + aiProcessCount);
        }
    });

    await popupPage.waitForSelector('#send-ai-btn', { timeout: 5000 });
    
    // Wait for button to be enabled (backend connected)
    await popupPage.waitForFunction(() => {
        const btn = document.getElementById('send-ai-btn');
        return !btn.disabled;
    }, { timeout: 10000 });

    console.log("Clicking SEND PAGE TO AI button...");
    await popupPage.click('#send-ai-btn');

    console.log("Waiting for results...");
    await popupPage.waitForSelector('#results:not(.hidden)', { timeout: 10000 });
    await wait(1000); // Wait a little more just in case

    const aiViewText = await popupPage.$eval('#ai-view-text', el => el.value);
    console.log("========== AI VIEW TEXT ==========");
    console.log(aiViewText);
    console.log("==================================");
    
    console.log(`Total /sanitize requests: ${sanitizeCount}`);
    console.log(`Total /ai/process requests: ${aiProcessCount}`);

    await browser.close();
})();
