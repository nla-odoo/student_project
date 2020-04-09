document.getElementById('rent_pay').addEventListener('click',  function (event) {
$.post('/payment_controller', {tenant_id: document.getElementsByName('tenantid')[0].value}, function (result) {
			console.log(result);
			data_dict = JSON.parse(result);
			console.log(data_dict);
			form = document.createElement('form');
			form.setAttribute('action', data_dict['redirection_url'])
			delete data_dict['redirection_url'];
			for (const key in data_dict){
				input_element = document.createElement('input');
				input_element.setAttribute('name',key)
				input_element.setAttribute('value', data_dict[key])
				form.append(input_element);
			} 
			document.getElementsByTagName('body')[0].append(form);
			form.submit()
		})
})

function changeFunc() {
	const rent = document.getElementById("rent").value;
	var countrent;
    var selectBox = document.getElementById("selectoption");
    var selectedValue = selectBox.options[selectBox.selectedIndex].value;
    if (selectedValue == 'month') {
		countrent = 200;
	}
    else if (selectedValue == 'annual') {
    	countrent = rent * 12;
    }
    else if (selectedValue == 'week') {
    	countrent = 200 * 7;
    	alert(rent);
	}
	
    document.getElementById("rent").value = countrent;
   }

/*document.getElementById('selectoption').addEventListener('change', function (event) {
$.post('/rent_details', {tenant_id: document.getElementsByName('tenantid')[0].value}, function (result) {
alert(tenant_id);
var data = JSON.parse(result);*/


