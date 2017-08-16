

function getLocation() {
    // get the location of the thought
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function(location) {
            $('#lat').val(location.coords.latitude);
            $('#long').val(location.coords.longitude);
            });
    }
    else {
        console.log("Sorry, no Geolocation support!");
        return;
    }
   
} 

     
$(document).ready(getLocation);