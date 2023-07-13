# 2023-1-Grupo-16: RateYourSeat  
## Ingeniería de Software CC4401-1 Otoño 2023  
**Integrantes:**  
- Nicolás Calbucura  
- Gonzalo Cisternas  
- Leonel Espinoza  
- Katia Fredes  
- Javiera Jiménez  

# Sprint 2  
##### _Fecha:_ 04-07-2023   

## Notas de Versión:  
+ Se implementaron las vistas: `/reviews`, `/my_reviews`,`/add-review`  y `/single_review/<id>` 
+ Se implemento la creación de reseñas
+ Se implemento un filtro y un buscador en la vista `/reviews`
+ Se implemento la funcionalidad de editar y eliminar una reseña
+ Se implemento la funcionalidad de votar una reseña
+ Se implemento la funcionalidad de comentar una reseña
+ Se implemento la funcionalidad de editar y eliminar un comentario
+ Se cambió el diseño de las reseñas
+ Se cambió el diseño de la vista `/home` y `/`
+ Se hizo un refactoring de secciones en los templates/htmls

## Direcciones y funcionalidades 
+ **Navbar**:  
A través de la página siempre esta presenta una barra de navegacion con el nombre de la aplicación. También tiene los enlaces a Inicio(**`/home`**), reseñas(**`/reviews`**), agregar reseña(**`/add-review`**) y mis reseñas(**`/my_reviews`**). Y por último, a la izquierda tiene un botón para iniciar sesión (**`/log_in`**) en caso de no estar iniciado o el nombre del perfil con un enlace a mis reseñas junto a un boton para cerrar sesion.  

+ **Reviews**:  
Las reviews o reseñas son lo principal del sitio. Cada reseña se organiza tal que a la izquierda se encuentran los botones de 'upvote' y 'downvote' que son los votos positivos y negativos respectivamente. Entre esos dos botones se encuentra la puntuación de la reseña que es la resta entre votos positivos y negativos. Si el usuario viendo la reseña no tiene sesión iniciada, no sera capaz de interactuar con la reseña. Después de los votos se encuentra la información de la reseña partiendo con el nombre de usuario del autor, la fecha de creación de la reseña, el lugar/estadio del evento y el sector del asiento del que quiere hacer una reseña. Seguido de lo anterior se encuentra el nombre del artista o evento si fue ingresado, la puntuacion en estrellas que le da a su posicion en el concierto y el contenido en texto de la reseña como tal.
Por último a la derecha se encuentra una imagen de como se veía desde ese asiento en caso de que el usuario haya ingresado una imagen.  
Al dejar el cursor encima de una reseña por un momento, aparecerá un pequeño mensaje: __'Click para comentar y más'__, el cual es para indicar que al hacer click en la reseña redirigirá al usuario a `/single_review/id`.


+ **`/home`** y **`/`**:  
Página principal de la aplicación. Aqui se presentarán las 3 reseñas más recientes o populares. Es una presentacion de la página y tiene un boton al centro para explorar reseñas, el cual redirige a **`/reviews`**

+ **`/log_in`**:  
Página para iniciar sesion donde se presenta un form simple que pide el nombre del usuario y su contraseña. Si la informacion entregada es correcta el botón iniciar sesion dirige a `/home`, si es incorrecta indica los campos a corregir. Abajo del botón para iniciar sesion se encuentra un link a `/sign_up` en caso de que el usuario necesite crear su cuenta.  

+ **`/sign_up`**:  
Página para registrarse en la aplicación y agregar un nuevo usuario a la base de datos. Aqui se encuentra un form donde se pide nombre de usuario, email y contraseña, una vez se completan correctamente se envia la informacion con `'POST'` y se procesan los datos para agregarlos a la base de datos. Una vez agregados a la base de datos redirige a `/home`   

+ **`/reviews`**:  
En reseñas se encuentra todas las reseñas de la página en conjunto a un filtro por recintos, opciones para ordenar por novedad, popularidad, antiguedad y puntuación. Y también hay una barra que permite buscar reseñas por artista o nombre de evento.  

+ **`/add-reviews`**:  
Esta página solo se puede acceder con una sesion iniciada, en caso contrario redirige a iniciar sesion (`/log_in`).  
En agregar reseña se presenta un form que tiene los siguientes campos: Recinto, Sector, Artista o evento(opcinal), Evalua tu experiencia(con estrellas), Describe tu experiencia y selecciona archivo. Una vez se envía el form con el botón __'Publicar'__, se procesa el input y se crea una reseña que se mostrará en las demás páginas adecuadamente.   

+ **`/my_reviews`**:  
Esta página solo se puede acceder con una sesion iniciada, en caso contrario redirige a iniciar sesion (`/log_in`).  
Aquí se disponen unicamente las reseñas de la autoría del usuario.

+ **`/single_review/<id>`**:  
En esta página se muestra una única reseña, especificamente la reseña cuyo id es igual al id en el url. Aquí, si la sesión está iniciada, se puede comentar la reseña y si se tiene la autoría de la reseña que se está mostrando también se puede eliminar o editar la reseña. Si no esta iniciada la sesión se mostrara un botón __'Inicia sesión para comentar'__ que redirige a `/log_in`.  
Al apretar el boton __'Eliminar'__ en la esquina inferior derecha de la reseña, aparecera una advertencia indicando que esta acción es irreversible y pidiendo confirmación al usuario.  
Al apretar el botón __'Editar'__ en la esquina inferior derecha de la reseña, aparecerá un modal con los inputs: 'Artista o evento', 'Evalua tu experiencia' con estrellas y el contenido en texto de la reseña. Exepto por 'Evalua tu experiencia', los campos están rellenados según la información original de la reseña, y los cambios se actualizan al apretar el botón Editar reseña del modal.  
Al apretar el botón de **'Escribe tu comentario!'** se abre un modal que recibe el contenido del comentario para publicarlo y dejarlo abajo de la publicación ordenados por antiguedad. Los comentarios se organizan de forma que se enseña el autor, la fecha de creación y el contenido del comentario en texto. Si el usuario tiene la autoría de algún comentario en este aparecerán los botones __'Eliminar'__ y __'Editar'__ con un funcionamiento similar que en una reseña pero para ese comentario en partícular.  

