// Selecionando os elementos
const menuBtn = document.getElementById('menu-btn');
const closeBtn = document.getElementById('close-btn');
const sidebar = document.getElementById('sidebar');

// Abre a barra lateral
menuBtn.addEventListener('click', () => {
  sidebar.classList.add('open');
});

// Fecha a barra lateral
closeBtn.addEventListener('click', () => {
  sidebar.classList.remove('open');
});

// Fecha a barra lateral se o usuário clicar fora dela
document.addEventListener('click', (e) => {
  if (!sidebar.contains(e.target) && !menuBtn.contains(e.target)) {
    sidebar.classList.remove('open');
  }
});
