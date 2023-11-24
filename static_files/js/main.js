document.addEventListener('DOMContentLoaded', function () {
  // get the DOM elements
  let toggleBtn = document.getElementById('toggleBtn');
  let userDetailDropdown = document.getElementById('userdetail__dropdown');

  /* Set the width of the side navigation to 100% */
  toggleBtn.onclick = function () {
    document
      .getElementById('navopen__toggle')
      .classList.toggle('mobile__sidemenu__toggle');
    if (toggleBtn.innerHTML === '<i class="fa-solid fa-xmark"></i>') {
      toggleBtn.innerHTML = '<i class="fa-solid fa-bars-staggered"></i>';
    } else {
      toggleBtn.innerHTML = `<i class="fa-solid fa-xmark"></i>`;
    }
  };

  userDetailDropdown.onclick = function () {
    document
      .getElementById('dropdown__menu')
      .classList.toggle('down__menu-show');
  };
});
