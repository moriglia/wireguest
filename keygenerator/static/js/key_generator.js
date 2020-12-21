// SPDX-License-Identifier: GPLv3-or-later
// Copyright (C) 2020 Marco Origlia

/* This script requires the module x25519.js by Github user CryptoEsel
 * You can load his module by addind the following html tag:
 * <script src="https://cdn.jsdelivr.net/gh/CryptoEsel/js-x25519/x25519.js"></script>
 * His module is distributed under the MIT license
 */

function generatePrivateKey() {
    const bytes_number = 32;
    var privateKeyBytes = new Uint8Array(bytes_number);
    window.crypto.getRandomValues(privateKeyBytes);

    return privateKeyBytes;
}

function keyToString(keyArray) {
    return btoa(String.fromCharCode.apply(null, keyArray));
}

function getPrivateKey(privateKeyBytes){
    return keyToString(privateKeyBytes);
}

function getPublicKey(privateKeyBytes){
    var publicKeyBytes = X25519.getPublic(privateKeyBytes);
    return keyToString(publicKeyBytes);
}

function generateAndSubmit() {

    var privateKeyBytes = generatePrivateKey();

    $.ajaxSetup({
        beforeSend: function(xhr) {
            xhr.setRequestHeader(
                'X-CSRFToken',
                document.getElementsByName('csrfmiddlewaretoken')[0].value
            );
        }
    });

    $.ajax({
        method: "POST",
        data: {
            interface_public_key: getPublicKey(privateKeyBytes),
            interface_name: document.getElementById('id_interface_name').value || "wg-no-name"
        },
        url: "/create/",
        // on success
        success: function (response) {
            console.log(response);
            console.log(getPrivateKey(privateKeyBytes));
        },
        // on error
        error: function (response) {
            console.log(response.responseJSON);
        }
    });
}

$(document).ready(function () {
    b = document.getElementById('generate_submit_button');
    b.onclick = generateAndSubmit;
});
