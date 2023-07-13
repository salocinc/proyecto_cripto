var select = document.getElementById('order');
var inputFecha = document.getElementById('fecha');
var calendar = document.getElementById('calendar');


select.addEventListener("click", function() {
    var options = activities.querySelectorAll("option");
    //unhide
});

select.addEventListener("change", function() {
    if(select.value == 'Fecha especifica'){
      inputFecha.style.display = 'block';
    }
    else{
      inputFecha.style.display = 'none';
    }
});

// Establecer la fecha mínima en la fecha actual
const fechaActual = new Date().toISOString().split("T")[0];
calendar.setAttribute("max", fechaActual);