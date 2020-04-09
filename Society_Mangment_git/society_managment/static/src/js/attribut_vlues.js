function myFunction(event) { 
    var nm = parseInt(document.getElementById('dem').value)
    nm += 1
    var frm = document.getElementById("value")
    var btn = document.createElement("input");
    btn.name = "value_name" + nm ;
    btn.placeholder = "Add Value";
    btn.id = "value_name" + nm ;
    var values = btn.id;
    document.getElementById("dem").value = nm
    console.log(nm)
    frm.appendChild(btn);
}
function myFunction1() {
    var element = document.getElementById("btn.id");
    element.parentNode.removeChild(element);
} 
function attributeValue(selectObj) {
    $(document).ready(function(){
        window.location.href = '/sub/'+ selectObj.value
    })
}
    // $.post('/sub/'+ selectObj.value)
    // console.log(selectObj.value)
    // location.reload();