document.getElementById('pay_now').addEventListener('click', function (event) {
$.post('/payment', {payment_id: document.getElementsByName('payment_id')[0].value},
 function (result) {
 	var form = document.createElement('form');
 	form.setAttribute("method", "post");
 	data = JSON.parse(result);
 	form.setAttribute('action', data.redirection_url);

 	for (var key in data){
 		var imp = document.createElement('input')
 		imp.setAttribute('id', key)
 		imp.setAttribute('name', key)
 		imp.setAttribute('value', data[key])
 		form.append(imp);
 	}
 	document.body.append(form);
 	form.submit();
	console.log(JSON.parse(result))})
	
});