(function($, createjs){
    var LOTUS_WIDTH = 24;
    var LOTUS_HEIGHT = 30;
    var LOTUS_PETALS = 12;
    var STAGE_WIDTH = 640;
    var STAGE_HEIGHT = 640;
    var BASE_WIDTH = 70;
    var INNER_RADIUS = 110;
    var OUTER_RADIUS = 300;
    var IN_STEP = 50;
    var WEBSOCKET_SERVER = "ws://127.0.0.1:8080/";

    var leds = [];
    var stage;
    var blossom;

    function onReady() {

        createBlossom();
    }

    function createBlossom() {
        var inner;
        var outer;
        var step = Math.PI * 2 / LOTUS_PETALS;

        stage = new createjs.Stage(document.getElementById("canvas"));

        blossom = new createjs.Container();
        blossom.x = STAGE_WIDTH / 2;
        blossom.y = STAGE_HEIGHT / 2;

        for (var i=0; i<LOTUS_PETALS; ++i) {
            petal = new createjs.Container();
            strips = new createjs.Container();
            mask = new createjs.Shape();

            if (i % 2 === 0) {
                inner = INNER_RADIUS;
                outer = OUTER_RADIUS;
            } else {
                inner = INNER_RADIUS - IN_STEP;
                outer = OUTER_RADIUS - IN_STEP;
            }

            var tx = 0;
            var ty = outer;
            var lx = BASE_WIDTH / 2;
            var ly = inner;
            var rx = BASE_WIDTH / -2;
            var ry = inner;

            mask.graphics.beginFill(createjs.Graphics.getRGB(255,0,0));
            mask.graphics.moveTo(tx, ty);
            mask.graphics.lineTo(lx, ly);
            mask.graphics.lineTo(rx, ry);
            mask.graphics.lineTo(tx, ty);
            mask.graphics.endFill();

            var incX = (tx - lx) / (LOTUS_HEIGHT + 1);
            var incY = (ty - ly) / (LOTUS_HEIGHT + 1);

            for (var j=0; j<LOTUS_HEIGHT; ++j) {
                led = new createjs.Shape();
                led.x = lx + (incX * j);
                led.y = ly + (incY * j);

                leds.push(led);

                strips.addChild(led);
            }

            incX = (rx - tx) / (LOTUS_HEIGHT + 1);
            incY = (ry - ty) / (LOTUS_HEIGHT + 1);

            for (j=0; j<LOTUS_HEIGHT; ++j) {
                led = new createjs.Shape();
                led.x = tx + (incX * (j + 2));
                led.y = ty + (incY * (j + 2));
                leds.push(led);

                strips.addChild(led);
            }

            strips.mask = mask;
            petal.addChild(strips);

            petal.rotation = step * i * 180/Math.PI;
            blossom.addChild(petal);
        }

        stage.addChild(blossom);
        stage.update();
    }

    function updateLEDs(colors) {
        var max = colors.length;

        for (var i=0; i<max; ++i) {
            var led;
            var color = colors[i];
            color >>= 0;
            var b = color & 0xFF,
                g = (color & 0xFF00) >>> 8,
                r = (color & 0xFF0000) >>> 16;
            var fillColor = createjs.Graphics.getRGB(r, g, b, 0.3);

            led = leds[i];
            led.graphics.clear();
            led.graphics.beginFill(fillColor);
            led.graphics.drawRect(-BASE_WIDTH/4, -3, BASE_WIDTH/2, 6);
            led.graphics.endFill();
        }
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
            updateLEDs(data['data']);
            stage.update();
        }
    }

    function onPreviewImage(e) {
        lotusImage = new Image();

        lotusImage.src = URL.createObjectURL(e.target.files[0]);
        $("#fullImage")[0].src = URL.createObjectURL(e.target.files[0]);

        lotusImage.onload = function() {
            drawImage();
        };
    }

    var ws = new WebSocket(WEBSOCKET_SERVER);
    ws.onopen = onWebSocketOpen;
    ws.onclose = onWebSocketClose;
    ws.onerror = onWebSocketError;
    ws.onmessage = onWebSocketMessage;

    $(document).ready(onReady);

}($, createjs));