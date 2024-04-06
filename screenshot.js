

const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const url = process.argv[2];
const segmentHeight = 4096;
const segmentWidth = 2048;
const timeout = 10000;

(async () => {
    
    const browser = await puppeteer.launch( {
        headless: "false",
        executablePath: '/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary',
        userDataDir: '/Users/scottlai/Library/Application\ Support/Google/Chrome\ Canary/Deafult',
    } );

    const page = await browser.newPage();

    await page.setViewport( {
        width: 1200,
        height: 2000,
        deviceScaleFactor: 1,
    } );

    await page.goto( url, {
        waitUntil: "domcontentloaded",
        timeout: timeout,
    } );

    await new Promise(resolve => setTimeout(resolve, timeout));

    const totalHeight = await page.evaluate(() => document.body.scrollHeight);
    let currentHeight = 0;
    let screenshotIndex = 0;

    while (currentHeight < totalHeight) {
        await page.setViewport({
            width: segmentWidth,
            height: Math.min(segmentHeight, totalHeight - currentHeight), // Adjust height for the last segment if it's shorter
            deviceScaleFactor: 1,
        });

        // Scroll to the current segment
        await page.evaluate((height) => {
            window.scrollTo(0, height);
        }, currentHeight);

        await page.waitForTimeout(timeout);

        await page.screenshot({
            path: `screenshot_${screenshotIndex}.jpg`,
            fullPage: false,
        });

        currentHeight += segmentHeight;
        screenshotIndex++;
    }

    await browser.close();
})();