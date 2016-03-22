function clearForm(selector) {
  $( selector ).each(function(){
      this.reset();
  });
}

$(document).ready(function(){
    // Create the socket.io connection to the specified endpoint (a.k.a "path")
    var socket = io({path: '/api/v1/stream'});

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('receive system', function(msg) {
        $('#log').prepend($('<div/>').text(msg.count + ' (System): ' + msg.data).html() + '<br>');
    });

    socket.on('receive echo', function(msg) {
        $('#log').prepend($('<div/>').text(msg.count + ' (Echo): ' + msg.data).html() + '<br>');
    });

    socket.on('receive broadcast', function(msg) {
        $('#log').prepend($('<div/>').text(msg.count + ': ' + msg.data).html() + '<br>');
    });

    // event handler for new connections
    socket.on('connect', function() {
        socket.emit('echo', {data: 'I\'m connected!'});
    });

    // handlers for the different forms in the page
    // these send data to the server in a variety of ways
    $('form#emit').submit(function(event) {
        socket.emit('echo', {data: $('#emit_data').val()});
        clearForm('form#emit');
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('broadcast', {data: $('#broadcast_data').val()});
        clearForm('form#broadcast');
        return false;
    });

    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect request');
        return false;
    });
});