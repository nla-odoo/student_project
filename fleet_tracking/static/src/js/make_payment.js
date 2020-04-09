document.getElementById('pay_now').addEventListener('click', function(event){
 	$.post('/confirm_order', {contract_id: document.getElementsByName('contract_id')[0].value,
 							amount: document.getElementsByName('amount')[0].value},
 							function(result) {
 								data =JSON.parse(result);
 								form = document.createElement('form')
 								form.setAttribute('action',  data.redirection_url)
 								form.setAttribute('method', 'post')
 								delete data['redirection_url']
								for (const key in data) {
							   		var new_element= document.createElement("input");
								 	new_element.type = 'hidden'
								 	new_element.setAttribute('name',key) 
								 	new_element.setAttribute('value',data[key]) 
								 	form.append(new_element)
								}
								document.getElementsByTagName('body')[0].append(form)
 								form.submit()
 							}
 							)

})
