document.addEventListener('DOMContentLoaded', function () {
  /* Set the width of the side navigation to 100% */
  let toggleBtn = document.getElementById('toggleBtn');
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
});
