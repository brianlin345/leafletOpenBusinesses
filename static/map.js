window.onload = function() {

  var basemap = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
     maxZoom: 18,
     id: 'mapbox.streets',
     accessToken: 'pk.eyJ1IjoiYmxpbjEwMDciLCJhIjoiY2syOG1qY25tMTNiYTNjbzBoNm1jeXpsayJ9.tc--O5r3IBXSUeVmIBbKtA'
  });
  console.log("basemap")


  $.getJSON("/static/businesses.json",function(data){

    var businessPts = L.geoJson(data, {
      onEachFeature: function(feature, layer) {
        layer.bindPopup('<h1>' + feature.properties.name + '</h1>'+"<a href='" + feature.properties.url + "'target=\"_blank\">Yelp link</a>");
      }

  });


  let map = L.map('mapid').setView([37.866510, -122.259800], 25);

  businessPts.addTo(map);
  basemap.addTo(map);

  });

};
