function initMap() {

  // Specify where the map is centered
  // Defining this variable outside of the map optios markers
  // it easier to dynamically change if you need to recenter

  var myLatLng = {lat: 41.850033, lng: -87.6500523};

  // Create a map object and specify the DOM element for display.
  var map = new google.maps.Map(document.getElementById('feelings-heatmap'), {
    center: myLatLng,
    zoomControlOptions: {
              position: google.maps.ControlPosition.RIGHT_CENTER
          },
    zoom: 4,
    // zoomControl: true,
    panControl: false,
    streetViewControl: false,
    // styles: MAPSTYLES,
    mapTypeId: google.maps.MapTypeId.TERRAIN
  });


  var infoWindow = new google.maps.InfoWindow({
            width: 150

  });

  
//   // Retrieving the information with AJAX
  $.get('/feelings.json', function (result) {
//     
      var feeling, marker, html, img;
     

      for (var key in result) {
          feeling = result[key];

          // img = { url: "/static/img/test.jpeg", size: new google.maps.Size(50,50)};

          if (feeling.sentiment > 1.0){
            img = { url: "/static/img/positive.png", size: new google.maps.Size(50,50)};
          }
          else if (feeling.sentiment < -1.0) {
            img = { url: "/static/img/negative.png", size: new google.maps.Size(50,50)};
          }
          else {
            img = { url: "/static/img/neutral.png", size: new google.maps.Size(50,50)};
          }
        
          // Define the marker
           marker = new google.maps.Marker({
              position: new google.maps.LatLng(feeling.lat, feeling.lng),
              map: map,
              title: 'Feeling ' + feeling.keywords,
              icon: img,
             
          });
          
          // Define the content of the infoWindow
          html = (
              '<div class="window-content">' +
                  '<p><b>Real Person with Real Feelings: </b> <a href="/users/' + feeling.user_id + '">USER</a></p>' +
                '<div class="col-md-5">' +
                  '<img width="254" height="355" src=' + feeling.flickr_id + '>' +
                '</div>' + 
                '<div class="col-md-5">' +
                  '<p><b>Word(s) Searched: </b>' + feeling.keywords + '</p>' +
                  '<p><b>Text:</b>' + feeling.tweet_id + '</p>' +
                  '<p><b>Date Felt: </b>' + feeling.generated_at + '</p>' +
                  '<p><b>All The Gory Details: </b>' + feeling.block_text + '</p>' +
                  '<p><b>Location: </b>' + marker.position + '</p>' +
                  '<p><b>Sentiment: </b>' + feeling.sentiment + '</p>' +
                '</div>' +
              '</div>');

          
          bindInfoWindow(marker, map, infoWindow, html);
          console.log("STUFF HAPPENING HEREEEEE")
      

          // marker.addListener('click', function() {
          //   infoWindow.open(map, marker);
          // });



          // Inside the loop we call bindInfoWindow passing it the marker,
          // map, infoWindow and contentString
          // bindInfoWindow(marker, map, infoWindow, html);
      }

  });

  // This function is outside the for loop.
  // When a marker is clicked it closes any currently open infowindows
  // Sets the content for the new marker with the content passed through
  // then it open the infoWindow with the new content on the marker that's clicked
  function bindInfoWindow(marker, map, infoWindow, html) {
      google.maps.event.addListener(marker, 'click', function () {
          infoWindow.close();
          infoWindow.setContent(html);
          infoWindow.open(map, marker);
          console.log(marker);
      });
  }
}

// //google.maps.event.addDomListener(window, 'load', initMap);
