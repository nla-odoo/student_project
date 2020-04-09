window.onload = function() {
    var element = document.getElementById('map');
    var map = L.map(element)
    const marker = L.marker([0, 0]).addTo(map);
    L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);    

    var geo_options = {
      enableHighAccuracy: true, 
      maximumAge        : 0, 
      timeout           : 120000
    };

    // const api_url = 'https://api.wheretheiss.at/v1/satellites/25544'

    // async function getiss(){
    //     const response = await fetch(api_url);
    //     const data = await response.json();
    //     const {latitude, longitude} = data;
    //     // L.marker([latitude, longitude]).addTo(map);
    //     marker.setLatLng([latitude, longitude])
    //     map.setView([latitude, longitude])
    //     // console.log("latitude="+latitude)
    //     // console.log("longitude="+longitude)
    // }
    // showMap();
    // getiss();
    // setInterval(getiss, 1000)



    if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition(showMap,handle_error,geo_options);
        var watchId = navigator.geolocation.watchPosition(set_marker);
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
        console.log("+")
        pos = get_lat_lng(position);
        lat = pos[0];
        lng = pos[1];
        // var target = L.latLng(lat, lng);
        marker.setLatLng([lat, lng])
        map.setView([lat, lng]);
        // L.marker(target).addTo(map);
        // map.panTo(new L.LatLng(21.1593458,727272727272.7520846));
        // map.setView(new L.LatLng(23.19303, 72.6352207), 12);
    }

    function showMap(position) {
        // debugger;
        function stuffToRezie(){
                var h_window = $(window).height();
                var h_map = h_window - 200;
                $('#map').css('height', h_map);
        }
        $(window).on("resize", stuffToRezie).trigger('resize'); 
        // set_marker(position);  
        map.setView([0,0], 1.5); 
    }

    function handle_error(error){
        if (error.code == 1){alert('Error code: '+error.code+"LOCATION PERMISSION DENIED");}
        if (error.code == 2){alert('Error code: '+error.code+"LIVE POSITION UNAVAILABLE");}
        if (error.code == 3){alert('Error code: '+error.code+"TIMEOUT : Did't Get Live Position For Long Time");}
    }
};