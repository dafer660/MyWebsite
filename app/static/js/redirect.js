window.setTimeout(function(){
    let protocol = window.location.protocol
    let host = window.location.host
    let fullURL = protocol + '//' + host
    window.location.href = fullURL;
}, 5000);
