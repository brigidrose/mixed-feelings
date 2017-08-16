function showReloadResults(results) {
    console.log(results);
    $("#twitter-text").html(results)
    $("#flickr-text").html(results)
}

function reloadResults(evt){
    evt.preventDefault();
    var keyword = $("#feeling-keyword")
    var toggle = $("#toggle-state")

    var dict = {
        "keyword": keyword.val(),
        "toggle": toggle.val()
    }
    $.post("/remix",
        dict,
        showReloadResults);
}

$("#remix-btn").on("click", reloadResults);
