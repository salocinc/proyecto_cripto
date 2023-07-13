// Función para manejar el clic en los botones de voto
function handleVoteClick(event) {
  const buttons = event.currentTarget.parentElement.querySelectorAll('.upvote-button, .downvote-button');
  buttons.forEach(button => button.classList.remove('clicked'));
  event.currentTarget.classList.add('clicked');
}

document.addEventListener('DOMContentLoaded', function() {
  // Obtener todos los botones de voto
  const voteButtons = document.querySelectorAll('.upvote-button, .downvote-button');

  // Asignar evento de clic a cada botón de voto
  voteButtons.forEach(button => {
    button.addEventListener('click', handleVoteClick);
  });
});

