window.onload = function() {

  let basemap = L.tileLayer('https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}', {
     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
     tileSize: 512,
     maxZoom: 18,
     zoomOffset: -1,
     id: 'mapbox/streets-v11',
     accessToken: 'pk.eyJ1IjoiYmxpbjEwMDciLCJhIjoiY2syOG1qY25tMTNiYTNjbzBoNm1jeXpsayJ9.tc--O5r3IBXSUeVmIBbKtA'
  });

  let map = L.map('defaultMap').setView([0, 0], 2);

  basemap.addTo(map);
};
