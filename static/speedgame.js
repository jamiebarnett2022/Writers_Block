let wordGoal = document.getElementById("wordcount");
let wpmGoal = document.getElementById("WPM");
let input = document.getElementById("inputArea");
let timer = document.getElementById("timerValue");

wordCount = 0;
timeElapsed = 0;

function showTitleForm() {
    document.getElementById("makeTitle").style.display = 'block';
}



function submit() {
    document.getElementById("postform").setAttribute("method", "POST");
    document.getElementById("postform").submit();
    
}

function title(title) {
    document.getElementById("title").innerHTML = title;
    submit();
}

function start() {
    document.getElementById("inputArea").innerHTML = "";
    clearInterval(timer);
    timer = setInterval(updateTimer, 1000);
    wordCount = 0;
    timeElapsed = 0;
    document.getElementById("wordsPerMinute").innerHTML = 0;

}

function updateWordCount() {
    words = document.getElementById("inputArea").value;
    wordArray = words.split(' ');
    wordCount = wordArray.length;
    document.getElementById("numWords").innerHTML = wordCount;

}


function cont() {
    timer = setInterval(updateTimer, 1000);
    wordCount = 0;
    timeElapsed = 0;
    document.getElementById("wordsPerMinute").innerHTML = 0;
}

function updateTimer() {
    if(wordCount < wordGoal.value) {
        document.getElementById("timerValue").innerHTML = timeElapsed;
        document.getElementById("wordsPerMinute").innerHTML= wordCount/(timeElapsed/60);
        if(document.getElementById("wordsPerMinute").value < wpmGoal.value) {
            document.getElementById("underWPM").innerHTML = "under";
        }
        else {
            document.getElementById("underWPM").innerHTML = "over";
        }
        timeElapsed++;
    }
    else {
        clearInterval(timer);
        $('#stopWritingModalWin').modal('show');
    }

}
function loadModal() {
    $('#stopWritingModalWin').modal('show');
}