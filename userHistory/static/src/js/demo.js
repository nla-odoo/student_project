function myFunction() {
  var selectBox = document.getElementById("Intrestin").value;
  var tr = document.getElementsByTagName("tr");
  var i;
  for (i = 0; i < tr.length; i++) {
    var td = tr[i].getElementsByTagName("td")[1];
    if (td) {
      var txtValue = td.textContent;
      if (txtValue.indexOf(selectBox) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

window.onload = function (){
	alert("hello");
	var tr = document.getElementsByTagName("tr");
    var i;
    var a = [];
   	var b = [];
  	for (i = 0; i < tr.length; i++) 
  	{
	    var td = tr[i].getElementsByTagName("td")[2];
	    if (td) 
	    {
	      var txtValue = td.textContent;
	      a.push(txtValue.replace('$','').replace(',',''));
		}
		var tdname = tr[i].getElementsByTagName("td")[0];
	    if (td) 
	    {
	      var nameValue = tdname.textContent;
	      b.push(nameValue);
		}
	}
	var ctx = document.getElementById('myChart');
	var chart = new Chart(ctx, 
	{
		type: 'bar',
	    data: {
	      labels: b,
	      datasets: [
	        {
	          label: "Population (millions)",
	          backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f"],
	          data: a
	        }
	      ]
	    },
	});
}

