$(function() {

    var isMyTurn = window._pair_owner_id == window._user_id ;
    var other_id = -1;
    var myCode = '';


    $('#leave').click(function(){
        location = '/';
    });



    var socket;

    var connected = function() {
        socket.subscribe('pair-code-' + window._pair_id);
    };

    var disconnected = function() {
        location = '/';
    };


    var messaged = function(data) {
        if( parseInt(data['user_id']) != parseInt(window._user_id) ) {
            other_id = data['user_id'];
            $('#code_area').val(data['code']);
            console.log('upd: '+ data['code']);
        }

    };

    setInterval(function(){
        var code = $('#code_area').val();
        if (code != myCode ) {
            myCode = code;

            socket.send({
                code: code,
                pair_id: window._pair_id
            });
        }

    },333);

    var start = function() {
        socket = new io.Socket();
        socket.connect('http://127.0.0.1:9000')

        socket.on('connect', connected);
        socket.on('disconnect', disconnected);
        socket.on('message', messaged);
    };

    start();

});
