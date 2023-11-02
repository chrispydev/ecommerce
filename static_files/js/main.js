document.addEventListener('DOMContentLoaded', function () {
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
      console.log(data);
      // Update cart count in the HTML element
      document.querySelector('#cart__info').textContent = data.total_quantity;
    });

  // add to cart button
  var addToCartButton = document.querySelector('#detail__add');
  addToCartButton.addEventListener('click', function () {
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
      });
  });
});
