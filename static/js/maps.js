var map;
var infowindow;
var service;

function initialize() {
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 17
  });

  if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(-22.9533, -43.341259);
 
      updatePlaces(-22.9533, -43.341259);
      // updatePlaces(position.coords.latitude, position.coords.longitude);
      map.setCenter(pos);

      google.maps.event.addListener(map, 'center_changed', function(){
        updatePlaces(map.getCenter().k, map.getCenter().A);
      })

    }, function() {
      handleNoGeolocation(true);
    });
  } else {
    // Browser doesn't support Geolocation
    handleN
  }
}

function setUp(results){
  for (var i = 0; i < results.length; i++) {
    createMarker(results[i]);
  }
}

function updatePlaces(latitude, longitude){
  $.ajax({
    url: "http://localhost:5000/places",
    type: "GET",
    dataType: "json",
    data: {latitude: latitude, longitude: longitude},
    async: false, 
    success: function(data){
      setUp(data.return);
    }
  });
}


function createMarker(place) {
  infowindow = new google.maps.InfoWindow();
  var marker
  console.log(place.name);
  if (place.isPoint){
      marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(place.latitude, place.longitude),
        icon: '/static/img/maps_icons/restaurantPoint.png'
      }) 
  } else{
      marker = new google.maps.Marker({
        map: map,
        position: new google.maps.LatLng(place.latitude, place.longitude),
        icon: '/static/img/maps_icons/restaurant.png'
      });
  }

  google.maps.event.addListener(marker, 'click', function() {
    console.log(place.referencePlaces)
    var content = '<p>' + place.name + '</p>' + '<a href="/profile/' + place.referencePlaces + '"">Veja mais</a>';
    infowindow.setContent(content);
    infowindow.open(map, this);
  });
}

function handleNoGeolocation(errorFlag) {
  if (errorFlag) {
    var content = 'Error: The Geolocation service failed.';
  } else {
    var content = 'Error: Your browser doesn\'t support geolocation.';
  }

  var options = {
    map: map,
    position: new google.maps.LatLng(0, 0),
    content: content
  };

  var infowindow = new google.maps.InfoWindow(options);
  map.setCenter(options.position);
}

function loadScript() {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyCJvZbxZgko6iW6AuFVUCMwqJDFBw-Nah8&sensor=true&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript;