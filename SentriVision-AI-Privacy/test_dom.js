const fs = require('fs');
const jsdom = require("jsdom");
const { JSDOM } = jsdom;

const html = fs.readFileSync('demo/demo.html', 'utf8');
const dom = new JSDOM(html);
const document = dom.window.document;
const NodeFilter = dom.window.NodeFilter;

function extractText() {
    if (!document.body) {
        return { success: false, error: "No readable page text found" };
    }

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
    
    if (textContent.length === 0) {
        return { success: false, error: "No readable page text found" };
    }
    
    return { success: true, text: textContent.join('\n') };
}

console.log(extractText().text);
