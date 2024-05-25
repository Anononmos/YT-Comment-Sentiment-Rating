async function getVideoId() {
    const query = { active: true, lastFocusedWindow: true }
    const [tab] = await chrome.tabs.query(query)

    video_id = tab.url.slice(-11)

    return video_id
}

async function getSentiment(video_id) {
    const response = await fetch(`http://localhost:8000/${video_id}`)
    const score = await response.json()

    // TODO: Add error checking in case of bad response

    return score
}

function main() {
    getVideoId()
    .then( id => getSentiment(id) )
    .then()
}

window.onload = main

