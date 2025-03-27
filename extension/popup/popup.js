// TODO: ADD CACHE FOR SEEN URLS


async function getVideoId() {
    const query = { active: true, lastFocusedWindow: true }
    const [tab] = await chrome.tabs.query(query)

    video_id = tab.url.slice(-11)

    return video_id
}

async function getSentiment(video_id) {
    const response = await fetch(`http://localhost:5000/${video_id}`, { mode: 'cors' })
    const score = await response.json()

    return score
}

function parseSentiment(score) {
    if ('status' in score) {
        displayError(score)

        return
    }

    displaySentiments(score)

    return
}

function displayError(error) {
    errorBlock = document.getElementById('error-block')
    sentimentBlock = document.getElementById('sentiments-block')

    errorBlock.innerHTML = `
        <h1>Error! Status ${error.status}</h1>
        <h2>Reason: ${error.reason}</h2>
        <p>${error.message}</p>
    `
    errorBlock.style.display = 'block'
    sentimentBlock.style.display = 'none'
}

function displaySentiments(score) {
    console.log(document.body.outerHTML)

    errorBlock = document.getElementById('error-block')
    sentimentBlock = document.getElementById('sentiments-block')

    errorBlock.style.display = 'none'
    sentimentBlock.style.display = 'block'

    // Populate label and progress tags with values

    labels = document.getElementsByTagName('label')
    progressBars = document.getElementsByTagName('progress')

    for (label of labels) {
        label.innerHTML = `${formatScore(score[label.htmlFor])}%`
    }

    for (progressBar of progressBars) {
        progressBar.value = formatScore(score[progressBar.id])
    }
}

function formatScore(score) {
    return Math.round( (score + Number.EPSILON) * 100 )
}

function main() {
    getVideoId()
    .then( id => getSentiment(id) )
    .then( score => parseSentiment(score) )
}

window.onload = main

