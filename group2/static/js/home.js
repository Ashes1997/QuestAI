
function addToBasket(productId) {
    var url = "/questAI/add_to_basket/" + productId + '/'; 
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'product_id': productId 
        },
        success: function(response) {
            alert("Product added to basket!");
        },
        error: function(xhr, errmsg, err) {
            if(xhr.responseJSON.login_required) { //checks login_required varable, if ye, then error is due to lack of login
                alert("You must log in to add items to the basket.");
                window.location.href = '/questAI/login/'; // Redirect to the login page since user is not logged in
            } else {
                alert("Error: " + xhr.status + ": " + xhr.responseText); //error is due to something else
            }
        }
    });
}

function likeDislikeProduct(productId, like) {
    var url = "/questAI/like_dislike/" + productId + '/'; 
    $.ajax({
        url: url,
        type: 'POST',
        data: {
            'csrfmiddlewaretoken': csrfToken,
            'like': like 
        },
        success: function(response) {
            // Update likes/dislikes count on success
            if(response.status === 'success') {
                $('#likes-count-' + productId).text(response.likes);
                $('#dislikes-count-' + productId).text(response.dislikes);
            } else {
                //alert(response.message);
            }
        },
        error: function(xhr, errmsg, err) {
            //alert("Error: " + xhr.status + ": " + xhr.responseText);
        }
    });
}
