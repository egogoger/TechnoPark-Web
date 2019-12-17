// docker run --ulimit nofile=65536:65536 -v /Users/egorbedov/Downloads/Prog/Technopark/Web/Q\&A/Technopark-Web/QA/etc:/centrifugo -p 8001:8000 centrifugo/centrifugo centrifugo -c config.json --client_insecure

var centrifuge = new Centrifuge('ws://127.0.0.1:8001/connection/websocket');

centrifuge.subscribe("new_posts", function(message) { // channel in send_message
    console.log(message.data.question_title);
});

centrifuge.connect();