var nameko = require("node-nameko-client");
var express = require("express");

var app = express();
var namekoClient;

nameko.connect({ host: "127.0.0.1", port: 5672 }).then(rpc => {
  namekoClient = rpc;

  console.log("Connected to AMQP.");

  app.listen(9000, function() {
    console.log("Server started on port 9000.");
  });
});

app.get("/movies", function(req, res) {
  namekoClient.call(
    "http_schedule_service",
    "get_schedule_rpc",
    [],
    {}, 
    function(e, r) {
      if (e) {
        res.send("Oops! RPC error: " + e);
      } else {
        res.send("Success: Result is " + r);
      }
    }
  );
});

app.get("/movie/:id", function(req, res) {
  namekoClient.call(
    "http_schedule_service",
    "get_schedule_by_movie_id_rpc",
    [req.params.id],
    {}, 
    function(e, r) {
      if (e) {
        res.send("Oops! RPC error: " + e);
      } else {
        res.send("Success: Result is " + r);
      }
    }
  );
})


