document.getElementById('pay_now').addEventListener('click', function(event){
console.log();
    $.post('/payment_confirm/', {
        appointments_id: document.getElementsByName('appointments_id')[0].value,
        visit_charges: document.getElementsByName('visit_charges')[0].value},
    function(result) 
    {
        data =JSON.parse(result);
        form = document.createElement('form')
        form.setAttribute('action',  data.redirection_url)
        form.setAttribute('method', 'post')
        delete data['redirection_url']
        for (const key in data)
        {
            var new_element= document.createElement("input");
            new_element.type = 'hidden'
            new_element.setAttribute('name',key)
            new_element.setAttribute('value',data[key])
            form.append(new_element)
        }
        document.getElementsByTagName('body')[0].append(form)
        form.submit()
    })

})
document.onkeydown = function(e) 
{
    if(event.keyCode == 123) {
    return false;
    }
    if(e.ctrlKey && e.shiftKey && e.keyCode == 'I'.charCodeAt(0)){
    return false;
    }
    if(e.ctrlKey && e.shiftKey && e.keyCode == 'J'.charCodeAt(0)){
    return false;
    }
    if(e.ctrlKey && e.keyCode == 'U'.charCodeAt(0)){
    return false;
}
}