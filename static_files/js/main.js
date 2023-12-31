// make a button display and disappear when shipping is empty or filled
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

  // Payment
  const paymentButton = document.querySelector('#checkout__button');
  const paymentShipping = document.querySelector('#calculate__shipping');

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
  if (userDetailDropdown) {
    userDetailDropdown.onclick = function () {
      document
        .getElementById('dropdown__menu')
        .classList.toggle('down__menu-show');
    };
  }

  searchProductBtn.addEventListener('click', function () {
    const searchQuery = search.value;
    if (searchQuery.length === 0) {
      return;
    } else {
      window.location.href = `/product-search/${searchQuery}/`;
    }
  });

  search.addEventListener('keydown', function () {
    if (event.key === 'Enter') {
      const searchQuery = search.value;
      if (searchQuery.length === 0) {
        return;
      } else {
        window.location.href = `/product-search/${searchQuery}/`;
      }
    }
  });

  searchProductMobileBtn.addEventListener('click', function () {
    const searchQuery = searchMobile.value;
    console.log(searchQuery);
    if (searchQuery.length === 0) {
      return;
    } else {
      window.location.href = `/product-search/${searchQuery}/`;
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
  if (ca_) {
    ca_.onclick = function () {
      document.getElementById('cate_hide_').classList.toggle('hideToggle');
    };
  }

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
          if (!response.ok) {
            console.log('error');
            // Update the message section
            document.querySelector('#cart__message').style.display = 'block';
            document.querySelector('#cart__message').innerHTML = `
           <p>Please login first</p>
          `;
            setTimeout(() => {
              document.querySelector('#cart__message').style.display = 'none';
            }, 2000);
          } else if (response.ok) {
            return response.json();
          }
        })
        .then(function (data) {
          // Update cart icon
          document.querySelector('#cart__info').textContent = data.cart_count;
          // Update the message section
          document.querySelector('#cart__message').style.display = 'block';
          document.querySelector('#cart__message').innerHTML = `
          <p>Product added succesfully</p>
          `;
          setTimeout(() => {
            document.querySelector('#cart__message').style.display = 'none';
          }, 2000);
        });
    });
  }

  // Payment method
  if (paymentButton) {
    paymentButton.addEventListener('click', () => {
      var reference = Date.now().toString(); // Generate a unique reference based on the current timestamp
      const total = document.getElementById('total').innerText;
      const email = document.querySelector('#id_email').value;
      const address = document.querySelector('#id_address').value;
      const phone_number = document.querySelector('#id_phone_number').value;
      const region = document.querySelector('#id_region').value;
      const city = document.querySelector('#id_city').value;
      const nearest_location = document.querySelector(
        '#id_nearest_location'
      ).value;
      let pesewasAmount = total * 100; // Equivalent amount in Pesewas
      var pesewasAmount_ = pesewasAmount.toFixed(2); // Equivalent amount in Pesewas
      const helperText = document.querySelectorAll('.form-text');
      const shippingfee = document.querySelector('#shipping__fees');
      console.log(shippingfee.textContent.length);

      if (
        address.length === 0 ||
        phone_number.length === 0 ||
        region.length === 0 ||
        city.length === 0 ||
        shippingfee.textContent.length === 0
      ) {
        for (let index = 0; index < helperText.length; index++) {
          const element = helperText[index];
          element.className = 'form-text text-danger';
        }
      } else {
        var paystackPopup = PaystackPop.setup({
          key: 'pk_test_098b290ad40589ec8a95cc8d28d15c3708f2f6ef',
          email: email,
          amount: pesewasAmount_,
          currency: 'GHS',
          ref: reference, // Use the unique reference for the transaction
          callback: function (response) {
            // Handle the payment response
            if (response.status === 'success') {
              // Make an AJAX request to save the order and delete cart items
              document.getElementById('preloader').classList.toggle('hide');
              saveOrderAndDeleteCartItems(
                address,
                phone_number,
                region,
                city,
                nearest_location,
                response.transaction
              );
            } else if (response.status !== 'success') {
              alert(response.status);
            }
          },
        });
        paystackPopup.openIframe();
      }
    });
  }

  // save order into the database
  function saveOrderAndDeleteCartItems(
    address,
    phone_number,
    region,
    city,
    nearest_location,
    transaction
  ) {
    var csrfToken = getCookie('csrftoken');
    total = document.getElementById('total').innerText;
    var requestData = {
      total: total,
      address: address,
      phone_number: phone_number,
      transaction: transaction,
      region: region,
      city: city,
      nearest_location: nearest_location,
    };
    fetch('/api/order-confirm/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrfToken,
      },
      body: JSON.stringify(requestData), // Convert the request body to JSON format
    })
      .then((response) => {
        if (response.ok) {
          window.location.href = `/order-confirm/`;
        } else {
          window.location.href = `/order-confirm/`;
          throw new Error('Error saving order and deleting cart items');
        }
      })
      .catch((error) => {
        console.error('Error', error);
      });
  }

  // Calculate shipping fees
  if (paymentShipping) {
    paymentShipping.addEventListener('click', () => {
      const region = document.querySelector('#id_region').value;
      const city = document.querySelector('#id_city').value;
      const shippingfee = document.querySelector('#shipping__fees');

      fetch('/api/shipping-rate/')
        .then((response) => response.json())
        .then((data) => {
          const filteredResult = data.filter(
            (item) => item.region === region && item.city === city
          );
          if (filteredResult.length > 0) {
            const shippingCost = filteredResult[0].shipping_cost;
            // console.log(
            //   `Shipping cost for ${region}, ${city}: ${shippingCost}`
            // );
            shippingfee.textContent = `GHC ${shippingCost}`;
          } else {
            // console.log(`No shipping cost found for ${region}, ${city}`);
          }
        })
        .catch((error) => {
          console.error('Error:', error);
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
