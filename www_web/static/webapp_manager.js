

	// Get the modal
	var modal = document.getElementById('myModal');

	// Get the button that opens the modal
	var btn = document.getElementById("myBtn");
	var updateGpsBtn = document.getElementById("update_gps_btn");

	// Get the <span> element that closes the modal
	var span = document.getElementsByClassName("close")[0];

	// When the user clicks on the button, open the modal
	btn.onclick = function() {
		modal.style.display = "block";
		var txLat = document.getElementById("lat");
		var txLng = document.getElementById("long");
		var lat = txLat.value;
		var lng = txLng.value;
		var zoom = 12;
		if(lat==0 && lng==0) zoom = 1;
		
		document.getElementById("new_lat").value = lat;
		document.getElementById("new_lng").value = lng;
		google_map_init(lat, lng, zoom);
	}

	updateGpsBtn.onclick = function() {
		document.getElementById("appForm").lat.value	= document.getElementById("new_lat").value;
		document.getElementById("appForm").long.value	= document.getElementById("new_lng").value;
		modal.style.display = "none";
	}

	// When the user clicks on <span> (x), close the modal
	span.onclick = function() {
		modal.style.display = "none";
	}

	// When the user clicks anywhere outside of the modal, close it
	window.onclick = function(event) {
		if (event.target == modal) {
		    modal.style.display = "none";
		}
	}


