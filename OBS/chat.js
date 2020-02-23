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
    var message = message_split[2];
    var html = "<div id='message'><div id='center'>" + time + " " + "<username>" + username + "</username> " + message + "</div><div id='end>'</div></div>"
    $("#chat").append(html);
  }
}

updateData();
var old;

$(function() {
  old = messages;
  updateChat();

  setInterval(function() {
    updateData();
    if(old != messages) {
      updateChat();
      old = messages;
    }
  }, 100);

});
