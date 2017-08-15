
// function Info(id, text) {
//     this.id = id;
// }

// function init() {
//     var submit = document.getElementById("submit");
//     submit.onclick = getDateAndLocation;
// }

alert("CAN ANYONE SEEEEE MEEE?");

function getLocation() {
    alert("WHAT IS GOING ON?!");
    // get the location of the thought
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(location) {
            console.log(location.coords.latitude);
            console.log(location.coords.longitude);
            $('#geo').val(info);
            });
    }
    else {
        console.log("Sorry, no Geolocation support!");
        return;
    }
   
} 

     
// function geoLocation(position) {
//     var latitude = position.coords.latitude;
//     var longitude = position.coords.longitude;
//     var mapDiv = document.getElementById("map");
//     mapDiv.innerHTML = "I'm thinking at " + latitude + ", " + longitude;
// }
$(document).ready(getLocation);