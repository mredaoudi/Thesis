var spin = document.getElementById('spin');
var alert_finished = document.getElementById('alert_finished');
var card_header = document.getElementById('card_header');
var card_body = document.getElementById('card_body');
var tlink = document.getElementById('tlink');
var ttext = document.getElementById('ttext');
var tweet = document.getElementById('tweet');
var id, text;

var posButton = document.getElementById('posButton');
var neuButton = document.getElementById('neuButton');
var negButton = document.getElementById('negButton');
var delButton = document.getElementById('delButton');
var keyboard = {
    "q": posButton,
    "s": neuButton,
    "d": negButton,
    "f": delButton
}

var tweet_counter = document.getElementById('tweet_counter'); 

window.onload = function() {
    showSpin(true)
    getNextTweet();
    spin.style.display = 'none';
    alert_finished.style.display = 'none';
    document.addEventListener('keydown', (event) => {
	    var name = event.key;
        if (name in keyboard){
            keyboard[name].click()
        }
    }, false);
    setupCounter()
};

function setupCounter(){
    td = new Date()
    if ((localStorage.getItem("minuteCounter") === null && localStorage.getItem("currentMinute") === null) || (td.getMinutes().toString() != localStorage.getItem("currentMinute"))){
        localStorage.setItem("minuteCounter", 0);
        localStorage.setItem("currentMinute", td.getMinutes());
    }
    tweet_counter.innerText = localStorage.getItem("minuteCounter");
}

function submitLabel(label) {
    showSpin(true)
    const data = { 'id': id, 'label': label, 'text': text };
    fetch('/tweet', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    }).then(response => response.json()).then(data => getNextTweet()).catch((error) => { console.error('Error:', error); });
    updateCounter()
}

function updateCounter(){
    td = new Date();
    minuteCounter = parseInt(localStorage.getItem("minuteCounter"))
    currentMinute = parseInt(localStorage.getItem("currentMinute"))
    if (currentMinute == td.getMinutes()){
        minuteCounter += 1;
        localStorage.setItem("minuteCounter", minuteCounter);
    } else {
        localStorage.setItem("minuteCounter", 1);
        localStorage.setItem("currentMinute", td.getMinutes());
    }
    tweet_counter.innerText = localStorage.getItem("minuteCounter");
}

function getNextTweet() {
    fetch('/tweet').then(response => response.json()).then(data => (data["empty"]) ? finished() : editCard(data["load"]));
    showSpin(false);
}

function editCard(load) {
    var link = "https://twitter.com/anyuser/status/" + load[0];
    id = load[0];
    text = load[1];
    tlink.href = link;
    tlink.innerText = "Tweet #" + load[2];
    ttext.innerText = load[1];
}

function finished() {
    tweet.style.display = 'none';
    alert_finished.style.display = 'block'
}

function showSpin(show) {
    if (show) {
        spin.style.display = 'block';
        card_header.style.display = 'none';
        card_body.style.display = 'none';
    } else {
        spin.style.display = 'none';
        card_header.style.display = 'block';
        card_body.style.display = 'block';
    }
}
