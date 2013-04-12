(function($){

    var WEBSOCKET_SERVER = "ws://127.0.0.1:8080/";
    var leds = []

    function onReady() {
        var $petals = $(".petal");

        for (var i=0; i<$petals.length; ++i) {

            var side = $($petals[i]).find(".petal-left");

            for (var j=0; j<90; ++j) {
                var led = $('<div class="led"></div>');
                side.append(led);
                leds.push(led[0]);
            }

            side = $($petals[i]).find(".petal-right");

            for (var j=0; j<90; ++j) {
                var led = $('<div class="led"></div>');
                side.append(led);
                leds.push(led[0]);
            }
        }
    }

    function toColor(num) {
        num >>= 0;
        var b = num & 0xFF,
            g = (num & 0xFF00) >>> 8,
            r = (num & 0xFF0000) >>> 16;
        return "rgb(" + [r, g, b].join(",") + ")";
    }

    function onWebSocketOpen(event) {
        console.log("CONNECTED!");

        var msg = JSON.stringify({"type":"init"});
        ws.send(msg);
    }

    function onWebSocketClose(event) {

    }

    function onWebSocketError(event) {
        console.log("WebSocket Error:", event);
    }

    function onWebSocketMessage(event) {
        var data = JSON.parse(event.data);

        if (data['type'] == 'blossom') {
            console.log("update blossom...");
            var blossom = data['data'];
            var max = blossom.length;

            for (var i=0; i<max; ++i) {
                leds[i].style.backgroundColor = toColor(blossom[i]);
            }
        }
    } 

    var ws = new WebSocket(WEBSOCKET_SERVER);
    ws.onopen = onWebSocketOpen;
    ws.onclose = onWebSocketClose;
    ws.onerror = onWebSocketError;      
    ws.onmessage = onWebSocketMessage;

    $(document).ready(onReady);

}($));