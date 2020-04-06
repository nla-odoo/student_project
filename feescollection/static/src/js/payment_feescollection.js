document.getElementById('fec_pay').addEventListener('click', function(event) {

    console.log(event);
    $.post('/payment/', { res_user_id: document.getElementsByName('res_user_id')[0].value }, function(result) {
        // console.log(JSON.parse(result))
        data =JSON.parse(result);
        var form = document.createElement('form');
        form.setAttribute("method", "post");
        form.setAttribute("action", data.redirection_url);
        delete data['redirection_url'];
        for (const prop in data) {
            var inp = document.createElement('input');
            inp.setAttribute("type", 'hidden');
            inp.setAttribute("name", prop)
            inp.setAttribute("value", data[prop])
            form.append(inp);
        }
        debugger
        document.body.append(form)
        form.submit()
    });
})