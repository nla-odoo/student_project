document.getElementById('vehicle_type').addEventListener('change', function (event) {
	$.post('/getvehicle_details', {type: event.target.value}, function (result) {
		var data = JSON.parse(result);
		document.getElementsByName('vehicle_capacity')[0].value = data.vehicle_capacity
		document.getElementsByName('vehicle_speed')[0].value = data.vehicle_speed
		document.getElementsByName('vehicle_weight')[0].value = data.vehicle_weight
	})
})