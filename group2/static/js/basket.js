function redirectToCheckout() {
    // Show the spinner
    document.querySelector('.spinner-border').style.display = 'inline-block';

    // Redirect to the checkout page
    window.location.href = "/questAI/checkout/";
}

function updateBasket(itemId, action) {
    $.ajax({
        url: '/questAI/update_basket/',
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'item_id': itemId,
            'action': action
        },
        dataType: 'json',
        success: function (data) {
            if (data.status === 'success') {
                location.reload();
            } else {
                alert("Something went wrong: " + data.message);
            }
        },
        error: function (xhr, errmsg, err) {
            alert("Ajax error: " + xhr.status + ": " + xhr.responseText);
        }
    });
}