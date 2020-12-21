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

function createConfigurationFile(interface_name, interface_address, privateKeyBytes){
    var config_text = "[Interface]\n\
# The public key is: " + getPublicKey(privateKeyBytes) + "\n\
PrivateKey = " + getPrivateKey(privateKeyBytes) + "\n\
ListenPort = TO_CONFIGURE\n\
Address = " + interface_address + "\n\
\n\
[Peer]\n\
PublicKey = WIREGUARD_SERVER_PUBLIC_KEY\n\
Endpoint = WIREGUARD_ENDPOINT:WIREGUARD_INTERFACE_PORT\n\
AllowedIPs = 0.0.0.0/0\n\
"
    var b = new Blob([config_text], {type: "text/plain;charset=UTF-8"});
    var dummy_node = document.createElement('a');
    document.body.appendChild(dummy_node);
    dummy_node.href = URL.createObjectURL(b);
    dummy_node.download = interface_name + ".conf";
    dummy_node.click();
}

function generateAndSubmit() {

    var privateKeyBytes = generatePrivateKey();
    var interface_name = document.getElementById('id_interface_name').value || "wg-no-name"

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
            interface_name: interface_name
        },
        url: "/create/",
        // on success
        success: function (response) {
            createConfigurationFile(interface_name, response.address, privateKeyBytes);
        },
        // on error
        error: function (response) {
            console.log(response.error);
        }
    });
}

$(document).ready(function () {
    b = document.getElementById('generate_submit_button');
    b.onclick = generateAndSubmit;
});
