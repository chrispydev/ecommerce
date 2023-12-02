document.addEventListener('DOMContentLoaded', function () {
  // get the DOM elements
  let toggleBtn = document.getElementById('toggleBtn');
  let ca_ = document.getElementById('cate_hide');
  let userDetailDropdown = document.getElementById('userdetail__dropdown');

  /* toggling the show categories */
  ca_.onclick = function () {
    document.getElementById('cate_hide_').classList.toggle('hideToggle');
  };

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

  // dropdown function
  userDetailDropdown.onclick = function () {
    document
      .getElementById('dropdown__menu')
      .classList.toggle('down__menu-show');
  };

  // search functionality
  const search = document.getElementById('search');
  const searchMobile = document.getElementById('search-mobile');
  const matchList = document.getElementById('match-list');
  const matchListMobile = document.getElementById('match-list-2');

  // Search products in data base
  const searchProduct = async (searchText) => {
    const res = await fetch('/api/');
    const products = await res.json();

    // Get matches to current text input
    let matches = products.filter((product) => {
      const regex = new RegExp(`^${searchText}`, 'gi');
      return product.name.match(regex);
    });

    if (searchText.length === 0) {
      matches = [];
      matchList.style.display = 'none';
      matchListMobile.style.display = 'none';
      matchList.innerHTML = '';
      matchListMobile.innerHTML = '';
    }

    outputHtml(matches);
  };

  // show results in HTML
  const outputHtml = (matches) => {
    if (matches.length > 0) {
      const html = matches
        .map(
          (match) => `
        <div class="search__results">
        <a href="/product-detail/${match.id}/">${match.name}</a>
        </div>
        `
        )
        .join('');
      matchList.style.display = 'block';
      matchListMobile.style.display = 'block';

      matchList.innerHTML = html;
      matchListMobile.innerHTML = html;
    }
  };

  search.addEventListener('input', () => searchProduct(search.value));
  searchMobile.addEventListener('input', () =>
    searchProduct(searchMobile.value)
  );
});
