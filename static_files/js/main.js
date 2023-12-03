document.addEventListener('DOMContentLoaded', function () {
  // get the DOM elements
  let toggleBtn = document.getElementById('toggleBtn');
  let ca_ = document.getElementById('cate_hide');
  let userDetailDropdown = document.getElementById('userdetail__dropdown');

  // search functionality
  const search = document.getElementById('search');
  const searchMobile = document.getElementById('search-mobile');
  const matchList = document.getElementById('match-list');
  const matchListMobile = document.getElementById('match-list-2');
  const searchProductBtn = document.getElementById('search__product');
  const searchProductMobileBtn = document.getElementById(
    'search__product__mobile'
  );

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

  searchProductBtn.addEventListener('click', function () {
    const searchQuery = search.value;
    if (searchQuery.length === 0) {
      return;
    } else {
      window.location.href = `http://localhost:8000/product-search/${searchQuery}/`;
    }
  });

  search.addEventListener('keydown', function () {
    if (event.key === 'Enter') {
      const searchQuery = search.value;
      if (searchQuery.length === 0) {
        return;
      } else {
        window.location.href = `http://localhost:8000/product-search/${searchQuery}/`;
      }
    }
  });

  searchProductMobileBtn.addEventListener('click', function () {
    const searchQuery = searchMobile.value;
    console.log(searchQuery);
    if (searchQuery.length === 0) {
      return;
    } else {
      window.location.href = `http://localhost:8000/product-search/${searchQuery}/`;
    }
  });

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

  // load cart quantity when page loads
  fetch('/cart/count/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest',
    },
  })
    .then(function (response) {
      return response.json();
    })
    .then(function (data) {
      if (data.total_quantity === null) {
        document.querySelector('#cart__info').textContent = '0';
      } else {
        document.querySelector('#cart__info').textContent = data.total_quantity;
      }
    });

  /* toggling the show categories */
  ca_.onclick = function () {
    document.getElementById('cate_hide_').classList.toggle('hideToggle');
  };

  // Handle Add to Cart button click
  var addToCartButtons = document.getElementsByClassName('add-to-cart-btn');
  for (var i = 0; i < addToCartButtons.length; i++) {
    addToCartButtons[i].addEventListener('click', function () {
      var productID = this.getAttribute('data-product-id');
      var csrfToken = getCookie('csrftoken');

      // AJAX request
      fetch('/add-to-cart/' + productID + '/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': csrfToken,
        },
        body: 'product_id=' + productID,
      })
        .then(function (response) {
          return response.json();
        })
        .then(function (data) {
          // Update cart icon
          document.querySelector('#cart__info').textContent = data.cart_count;
          // Update cart items in the navbar
        });
    });
  }

  // Function to get CSRF cookie value
  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + '=') {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
