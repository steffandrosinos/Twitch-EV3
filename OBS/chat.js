function getUserColour(username) {
  if(username in users) {
    return users[username];
  } else {
    var colour = '#'+Math.floor(Math.random()*16777215).toString(16);
    users[username] = colour;
    return users[username];
  }
}
function updateData() {
  $("#data_script").remove();
  var script = document.createElement('script');
  script.onload = function () {};
  script.src = "chat_data.js";
  script.id = "data_script";
  document.head.appendChild(script);
}
function updateChat() {
  $("#chat").html("");
  for(var i=0; i<messages.length; i++) {
    var message_split = messages[i].split("*.*");
    var time = message_split[0];
    var username = message_split[1];
    var username_ = username.substring(0, username.length-1);
    var message = message_split[2];
    var html = "<div id='message'><div id='center'>" + time + " " + "<div class='" + username_ + "'>" + username + "</div> " + message + "</div><div id='end'></div></div>"
    $("#chat").append(html);
    $("." + username_).css("display", "inline-block");
    if(username_ != "zxqw" && username_ != "zxqwbot") {
      var user_colour = getUserColour(username_);
      $("." + username_).css("color", user_colour);
    }
  }
}

var users = {"zxqw": "#ff0000"};

updateData();

$(function() {
  setInterval(function() {
    updateData();
    updateChat();
  }, 250);
});
