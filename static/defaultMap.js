window.onload = function() {

  let basemap = L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
     maxZoom: 18,
     id: 'mapbox.streets',
     accessToken: 'pk.eyJ1IjoiYmxpbjEwMDciLCJhIjoiY2syOG1qY25tMTNiYTNjbzBoNm1jeXpsayJ9.tc--O5r3IBXSUeVmIBbKtA'
  });

  let map = L.map('defaultMap').setView([0, 0], 2);

  basemap.addTo(map);
};
