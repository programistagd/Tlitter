var tweet_text = document.getElementById("tweet_text");
var tweet_submit = document.getElementById("tweet_submit");
var tweet_log = document.getElementById("tweet_status");
var tweet_csrf = document.getElementById("tweet_csrf");

function get_tweet_text() {
    return tweet_text.value;
}

function log_tweet(msg) {
    tweet_log.innerHTML = msg;
}

function refresh_counter() {
    log_tweet(get_tweet_text().length + "/140");
}

function initialize_tweeter() {
    tweet_submit.addEventListener("click", function(e) {
        var text = get_tweet_text();
        var formData = new FormData();
        formData.append("text", text);

        var request = new XMLHttpRequest();
        request.open('POST', '/tweet/', true); //Warning: This doesn't check for current route in Django
        //request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
        request.setRequestHeader('X-CSRFToken', tweet_csrf.innerHTML);

        request.onload = function() {
            if (request.status == 200) {
                log_tweet("Tweet posted!");
                location.reload();
            } else {
                log_tweet("Something went wrong...");
            }
        };

        request.onerror = function() {
            log_tweet("Something went wrong...");
        };

        request.send(formData);
        log_tweet("Sending...");
    });

    tweet_text.onkeyup = refresh_counter;
    tweet_text.onchange = refresh_counter;

    refresh_counter();
}

if (tweet_text != null) {
    initialize_tweeter();
}