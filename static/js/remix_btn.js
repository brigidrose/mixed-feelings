function showReloadResults(results) {
    console.log(results);
    $("#photo").attr("src", results["photo"]);
    $("#giphy-url").val(results["photo"]);
    $("#text").html(results["tweets"]);
    $("#twitter-text").val(results["tweets"]);
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
