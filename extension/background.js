const url = 'https://www.youtube.com/watch?v='

chrome.runtime.onInstalled.addListener( () => {
    chrome.action.disable()

    // Remove rules since they stay after session
    chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
        const rule = {
            conditions: [
                new chrome.declarativeContent.PageStateMatcher({
                    pageUrl: { urlContains: url }
                })
            ], 
            actions: [new chrome.declarativeContent.ShowAction()]
        }
        chrome.declarativeContent.onPageChanged.addRules([rule])
    })
})