function google_map_init(lat =35, lng=-82, zoomlvl = 1) {

	var map = new google.maps.Map(document.getElementById('map_canvas'), {
		//zoom: 1,
		zoom: zoomlvl,
		//center: new google.maps.LatLng(35.137879, -82.836914),
		center: new google.maps.LatLng(lat, lng),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	});

	var myMarker = new google.maps.Marker({
	 	//position: new google.maps.LatLng(47.651968, 9.478485),
		position: new google.maps.LatLng(lat, lng),
		draggable: true
	});

	google.maps.event.addListener(myMarker, 'dragend', function (evt) {
		
		document.getElementById("new_lat").value = evt.latLng.lat().toFixed(6);
		document.getElementById("new_lng").value =  evt.latLng.lng().toFixed(6);

		document.getElementById('current').innerHTML = '<p>Marker dropped: Current Lat: ' + evt.latLng.lat().toFixed(6) + ' Current Lng: ' + evt.latLng.lng().toFixed(6) + '</p>';
	});

	google.maps.event.addListener(myMarker, 'dragstart', function (evt) {
		document.getElementById('current').innerHTML = '<p>Currently dragging marker...</p>';
	});

	map.setCenter(myMarker.position);
	myMarker.setMap(map);
}
