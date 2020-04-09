document.getElementById('pay').addEventListener('click',  function (event) {
    $.post('/payment', 
        {order_id: document.getElementsByName('order_id')[0].value},
        function (result) {
            data_dict = JSON.parse(result);
            form = document.createElement('form');
            form.setAttribute('action',data_dict['redirection_url']);
            delete data_dict['redirection_url'];
            for (const key in data_dict){
                input_element = document.createElement('input');
                input_element.setAttribute('name',key)
                input_element.setAttribute('value',data_dict[key])
                form.append(input_element);
            }
            document.getElementsByTagName('body')[0].append(form);
            form.submit();
        });
})

