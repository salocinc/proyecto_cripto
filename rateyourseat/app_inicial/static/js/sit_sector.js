const sit={
    "recintos": [
      {
        "nombre": "Movistar Arena",
        "tipos_asiento": ["Cancha", "Cancha VIP", "Platea Alta", "Platea Baja", "Tribuna", "Movilidad reducida", "Otros"]
      },
      {
        "nombre": "Teatro Cariola",
        "tipos_asiento": ["Platea Alta", "Platea Baja", "Galería", "Palcos", "Cancha", "Otros"]
      },
      {
        "nombre": "Teatro Caupolicán",
        "tipos_asiento": ["Cancha", "Platea Alta", "Platea Baja", "Palco", "Movilidad reducida", "Otros"]
      },
      {
        "nombre": "Estadio Nacional",
        "tipos_asiento": ["Cancha", "Cancha VIP", "Andes", "Pacifico", "Galería", "Movilidad reducida", "Otros"]
      },
      {
        "nombre": "Club Hípico",
        "tipos_asiento": ["Pacífico", "Andes", "Cancha", "Cancha VIP", "Galería", "Movilidad reducida", "Otros"]
      },
      {
        "nombre": "Estadio Monumental",
        "tipos_asiento": ["Cancha", "Cancha VIP", "Arica", "Magallanes", "Rapa Nui", "Océano", "Cordillera", "Movilidad reducida","Otros"]
      },
      {
        "nombre": "Estadio Bicentenario de la Florida",
        "tipos_asiento": ["Cancha", "Platea", "Tribuna", "Pit", "Pacífico", "Andes", "Movilidad reducida", "Otros"]
      },
      { "nombre": "Casa CEI",
        "tipos_asiento": ["Patio", "Otros"]
      },
      {
        "nombre": "Allianz Parque",
        "tipos_asiento": ["Cadeira Superior", "Cadeira Inferior", "Pista", "Pista Premium", "Pista VIP", "Otros"]
      },
      {
        "nombre": "UBS Arena",
        "tipos_asiento": ["Concert Floor", "300 Level", "200 Level", "100 Level", "Lower Club Level", "Suite and Loft Level", "Otros"]
      },
      {
        "nombre": "SoFi Stadium",
        "tipos_asiento": ["Concert Floor", "500 Level", "400 Level", "300 Level", "200 Level", "100 Level", "Suite", "Otros"]
      },
    ]
}

const recintoSelect = document.getElementById("place-select");
const sectorSelect = document.getElementById("sit-select");

// Llenar el select de recintos con las opciones del JSON
sit.recintos.forEach(recinto => {
    const option = document.createElement("option");
    option.value = recinto.nombre;
    option.textContent = recinto.nombre;
    recintoSelect.appendChild(option);
});

recintoSelect.addEventListener("change", e => {
    const recintoSeleccionado = e.target.value;
  
    // Obtener el recinto correspondiente del JSON
    const recinto = sit.recintos.find(recinto => recinto.nombre === recintoSeleccionado);
  
    // Limpiar el select de sectores
    sectorSelect.innerHTML = "<option selected>Selecciona sector</option>";
  
    // Llenar el select de sectores con las opciones del recinto seleccionado
    recinto.tipos_asiento.forEach(sector => {
        const option = document.createElement("option");
        option.value = sector;
        option.textContent = sector;
        sectorSelect.appendChild(option);
    });
});
