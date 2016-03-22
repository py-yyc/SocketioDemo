$(document).ready(function(){
    // Create the socket.io connection to the specified endpoint (a.k.a "path")
    var socket = io({path: '/api/v1/stream'});

    // event handler for server sent data
    // the data is displayed in the "Received" section of the page
    socket.on('receive system', function(msg) {
        $('#log').prepend($('<div/>').text('(system): ' + msg.data).html() + '<br>');
    });

    socket.on('receive room', function(msg) {
        $('#log').prepend($('<div/>').text('(rooms): ' + msg.data).html() + '<br>');
    });

    socket.on('receive room broadcast', function(msg) {
        $('#log').prepend($('<div/>').text(' (' + msg.room + ') ' + msg.user + ': ' + msg.data).html() + '<br>');
    });

    // handlers for the different forms in the page
    // these send data to the server in a variety of ways
    $('#join').click(function(event) {
        socket.emit('join room', {room: $('#room_name').val()});
        return false;
    });

    $('#leave').click(function(event) {
        socket.emit('leave room', {room: $('#room_name').val()});
        return false;
    });

    $('#close').click(function(event) {
        socket.emit('close room', {room: $('#room_name').val()});
        return false;
    });

    $('form#room_broadcast').submit(function(event) {
        socket.emit('broadcast room', {user: $('#user_name').val(), room: $('#room_name').val(), data: $('#room_data').val()});
        return false;
    });

    $('form#disconnect').submit(function(event) {
        socket.emit('disconnect request');
        return false;
    });
});