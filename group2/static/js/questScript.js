$(document).ready(function() {
    function sendChatbotMessage() {
        const message = $('#chatbot-input').val();
        $('#chatbot-input').val(''); // Clear input field
        const quest = $('#quest_text').text();
        $.ajax({
            url: '/questAI/questbot_ask/', 
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': djangoData.csrfToken,
                'message': message,
                'quest': quest  
            },
            dataType: 'json',
            success: function(data) {
                const messagesContainer = $('#chatbot-messages');
                messagesContainer.append(`<div>You: ${message}</div><br/>`);
                messagesContainer.append(`<div>Wizard: ${data.reply}</div><br/>`);
                messagesContainer.scrollTop(messagesContainer.prop("scrollHeight"));
            },
            error: function(xhr, errmsg, err) {
                alert("Ajax error: " + xhr.status + ": " + xhr.responseText);
            }
        });
    }

    $('button').click(function(e) {
        e.preventDefault(); 
        sendChatbotMessage();
    });
});

// get random number of elements from an array
function getRandomElements(arr, numElements) {
    const shuffled = arr.slice().sort(() => 0.5 - Math.random());
    return shuffled.slice(0, numElements);
}

// function to assign values like A,B,C... to our items
function generateQuestDescription(startLocation, basketItems, endLocations) {
    const alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    let description = [];
    description[0] = `Location A: ${startLocation} is your location.`;
    basketItems.forEach((item, index) => {
        const letter = alphabet.charAt(index + 1); // ASCII value of A is 65
        description[index + 1] = `Location ${letter}: ${endLocations[index]} is the location for ${item}.`;
    });
    return description;
}

let startLocation = djangoData.startLocation; // get the start location (address of the user)
let numberOfItems = djangoData.numberOfItems; // get the number of items in the basket
let basketItems = djangoData.basketItems; // get the names of items in the basket

// random addresses(5)
let locations = [
    'Glasgow G2 1DH',
    '10 Shawfield Dr, Glasgow G5 0AN',
    '100 Pointhouse Rd, Govan, Glasgow G3 8RS',
    '220 Robroyston Rd, Glasgow G33 1JQ',
    'North St, Glasgow G3 7DN',
];

let endLocations = getRandomElements(locations, numberOfItems);

let description = generateQuestDescription(startLocation, basketItems, endLocations);
console.log(description);

// create the <ul> element for our list of items
const ul = document.createElement('ul');

// add items into the list
description.forEach(item => {
    const li = document.createElement('li');
    li.textContent = item;
    ul.appendChild(li);
});

const container = document.getElementById('items_list');
container.appendChild(ul);

function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        zoom: 6,
        center: { lat: 55.860916, lng: -4.251433 }, // the center of the map (we can change that) which is Glasgow
    });
    const directionsService = new google.maps.DirectionsService();
    const directionsRenderer = new google.maps.DirectionsRenderer();
    directionsRenderer.setMap(map);

    calculateAndDisplayRoute(directionsService, directionsRenderer);
}

function calculateAndDisplayRoute(directionsService, directionsRenderer) {
    // convert each address in endLocations into a waypoint, except for the last one (the destination)
    let waypoints = endLocations.slice(0, -1).map(location => ({
        location: location,
        stopover: true
    }));

    // use the first location as the start point and the last location as the destination
    const start = startLocation;
    const end = endLocations[endLocations.length - 1];

    directionsService.route({
        origin: start,
        destination: end,
        waypoints: waypoints,
        optimizeWaypoints: true,
        travelMode: google.maps.TravelMode.DRIVING,
    }, (response, status) => {
        if (status === google.maps.DirectionsStatus.OK) {
            directionsRenderer.setDirections(response);
        } else {
            window.alert("Directions request failed due to " + status);
        }
    });
}
