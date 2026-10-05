const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch({
    headless: false,
    args: [
      '--disable-extensions-except=' + require('path').resolve('./extension'),
      '--load-extension=' + require('path').resolve('./extension')
    ]
  });
  const page = await browser.newPage();
  await page.goto('http://127.0.0.1:5500/demo.html', {waitUntil: 'networkidle0'});
  const extPage = await browser.newPage();
  const targets = await browser.targets();
  const extensionTarget = targets.find(target => target.type() === 'service_worker');
  const partialExtensionUrl = extensionTarget.url() || '';
  const [, , extensionId] = partialExtensionUrl.split('/');
  await extPage.goto('chrome-extension://' + extensionId + '/popup/popup.html');
  await extPage.waitForSelector('#send-ai-btn:not([disabled])');
  await extPage.click('#send-ai-btn');
  await extPage.waitForFunction('document.getElementById("ai-view-text").value.length > 0');
  const result = await extPage.$eval('#ai-view-text', el => el.value);
  console.log(result);
  await browser.close();
})();
