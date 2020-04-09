window.onload = function() {

	function stuffToRezie(){
	        var h_window = $(window).height();
	        var h_map = h_window - 200;
	        $('#mapid').css('height', h_map);
	}
	$(window).on("resize", stuffToRezie).trigger('resize');
    // var mymap = L.map('mapid').setView([0,0],16);
 //    button = document.createElement('button')
	// button.setAttribute('string',  'my button')


	

    var OpenStreetMap_Mapnik = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }),
	Thunderforest_OpenCycleMap = L.tileLayer('https://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png?apikey={apikey}', {
	attribution: '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	apikey: '<your apikey>',
	maxZoom: 22
	}),
	Thunderforest_Transport = L.tileLayer('https://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png?apikey={apikey}', {
	attribution: '&copy; <a href="http://www.thunderforest.com/">Thunderforest</a>, &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
	apikey: '<your apikey>',
	maxZoom: 22
	}),
	 Esri_WorldImagery = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
	attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
});

    var mymap = L.map('mapid', {
    center: [0, 0],
    zoom: 16,
    layers: [OpenStreetMap_Mapnik,Esri_WorldImagery]
	});
    var baseMaps = {
    "Setelite View": Esri_WorldImagery,
    "OpenStreetMap": OpenStreetMap_Mapnik,
	};

	L.control.layers(baseMaps).addTo(mymap);
	
	var marker = L.marker([0,0], {draggable:'true'}).on('dragend', function(event){	
		$.get('https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat='+event.target._latlng['lat']+'&lon='+event.target._latlng['lng'], function(data){
	    console.log("lat="+event.target._latlng['lat']+"lng"+event.target._latlng['lng']);
	    console.log(data['address']);
	    data = data['address']
	    address = ""
	    for(key in data){
	    	address += data[key]+',';
	    }

	    marker.bindPopup(address).openPopup();
	});

	});

	var  featureGroup = L.featureGroup([marker]).addTo(mymap);

    var geo_options = {
      enableHighAccuracy: true, 
      maximumAge        : 2000, 
      timeout           : 120000
    };

	if ("geolocation" in navigator) {
		console.log("1")
        navigator.geolocation.getCurrentPosition(set_marker,handle_error,geo_options);
    } else {s
        alert("Geolocation Is NOT Supported in your Browser");
    }

    function get_lat_lng(position){
        var lat = position.coords.latitude;
        var lng = position.coords.longitude;
        console.log("lat="+lat)
        console.log("lng="+lng)
        return [lat, lng];
    }
    function set_marker(position){
        pos = get_lat_lng(position);
        lat = pos[0];
        lng = pos[1];
        marker.setLatLng([lat, lng])
        mymap.setView([lat, lng]);





 


// L.Routing.control({
//   waypoints: [
//     L.latLng(23.19307163011698, 72.63540029525758),
//     L.latLng(23.201177753895394, 72.63546466827394)
    
//   ]
// }).addTo(mymap);

    }
    function handle_error(error){
        if (error.code == 1){alert('Error code: '+error.code+"LOCATION PERMISSION DENIED");}
        if (error.code == 2){alert('Error code: '+error.code+"LIVE POSITION UNAVAILABLE");}
        if (error.code == 3){alert('Error code: '+error.code+"TIMEOUT : Did't Get Live Position For Long Time");}
    }


};