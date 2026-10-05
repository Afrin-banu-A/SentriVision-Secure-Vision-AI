const puppeteer = require('puppeteer');
const path = require('path');

const wait = (ms) => new Promise(resolve => setTimeout(resolve, ms));

(async () => {
    try {
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
        popupPage.on('dialog', async dialog => {
            console.log('ALERT: ' + dialog.message());
            await dialog.dismiss();
        });
        console.log("Navigating to popup...");
        await popupPage.goto(`chrome-extension://${extensionId}/popup/popup.html`);

        await popupPage.waitForSelector('#send-ai-btn:not([disabled])', { timeout: 10000 });
        console.log("Clicking SEND PAGE TO AI button...");
        await popupPage.click('#send-ai-btn');

        await popupPage.waitForFunction('document.getElementById("ai-view-text").value.length > 0', { timeout: 5000 });

        const aiViewText = await popupPage.$eval('#ai-view-text', el => el.value);
        console.log("========== AI VIEW TEXT ==========");
        console.log(aiViewText);
        console.log("==================================");
        
        await browser.close();
    } catch (e) {
        console.error(e);
        process.exit(1);
    }
})();
