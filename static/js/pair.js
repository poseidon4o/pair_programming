$(function() {

    var name, started = false;


    var socket;

    var connected = function() {
        console.log('Conected');
    };

    var disconnected = function() {
        location = '/';
    };


    var messaged = function(data) {
        $('#code_area').val(data);
    };

    setInterval(function(){
        socket.send($('#code_area').val());
    },100)

    var start = function() {
        socket = new io.Socket();
        socket.connect();
        socket.on('connect', connected);
        socket.on('disconnect', disconnected);
        socket.on('message', messaged);
    };

    start();

});
