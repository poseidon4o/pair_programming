$(function() {

    var socket;

    var connected = function() {
        socket.subscribe('pair-code-' + window._pair_id);
    };

    var disconnected = function() {
        location = '/';
    };


    var messaged = function(data) {
        console.log(data['code']);
        $('#code_area').val(data['code']);
    };

    setInterval(function(){
        console.log('Sent:');
        socket.send({
            code: $('#code_area').val(),
            user_id: window._user_id,
            pair_id: window._pair_id
        });
    },333);

    var start = function() {
        socket = new io.Socket();
        socket.connect();
        socket.on('connect', connected);
        socket.on('disconnect', disconnected);
        socket.on('message', messaged);
    };

    start();

});
