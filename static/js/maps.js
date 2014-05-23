var map;
var infowindow;
var service;
var loc = ["Nordestino Carioca", "Restaurante Xinrong", "Empadas do Bosque"];

function initialize() {
  map = new google.maps.Map(document.getElementById('map-canvas'), {
    zoom: 17
  });

  if(navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(function(position) {
      var pos = new google.maps.LatLng(position.coords.latitude,
                                       position.coords.longitude);

    var request = {
      location: pos,
      radius: 1000,
      types: ['restaurant']
    };

    infowindow = new google.maps.InfoWindow();
    service = new google.maps.places.PlacesService(map);
    service.nearbySearch(request, callback);

    map.setCenter(pos);

    google.maps.event.addListener(map, 'center_changed', function(){
      var request = {
          location: map.getCenter(),
          radius: 1000,
          types: ['restaurant']
      };
      service.nearbySearch(request, callback);
    })

    }, function() {
      handleNoGeolocation(true);
    });
  } else {
    // Browser doesn't support Geolocation
    handleN
  }
}

function callback(results, status) {
  if (status == google.maps.places.PlacesServiceStatus.OK) {
    for (var i = 0; i < results.length; i++) {
      createMarker(results[i]);
    }
  }
}

function createMarker(place) {
  var placeLoc = place.geometry.location;
  var marker
  var image = '/static/img/maps_icons/restaurant.png';
  if (loc.indexOf(place.name) === -1){
    marker = new google.maps.Marker({
      map: map,
      position: place.geometry.location
    });
  } else{
    marker = new google.maps.Marker({
      map: map,
      position: place.geometry.location,
      icon: image
    });
  }

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent(place.name);
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
  script.src = "http://maps.googleapis.com/maps/api/js?key=AIzaSyCJvZbxZgko6iW6AuFVUCMwqJDFBw-Nah8&sensor=true&libraries=places&callback=initialize";
  document.body.appendChild(script);
}

window.onload = loadScript; 