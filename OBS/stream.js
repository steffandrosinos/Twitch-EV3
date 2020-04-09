function updateData() {
  $("#stream_data_script").remove();
  $("#robot_data_script").remove();
  var stream_script = document.createElement('script');
  stream_script.onload = function () {};
  stream_script.src = "stream_data.js";
  stream_script.id = "stream_data_script";
  document.head.appendChild(stream_script);
  var robot_script = document.createElement('script');
  robot_script.onload = function () {};
  robot_script.src = "robot_data.js";
  robot_script.id = "robot_data_script";
  document.head.appendChild(robot_script);
}
function addData(chart, label, data) {
  chart.data.labels.push(label);
  chart.data.datasets.forEach((dataset) => {
    dataset.data.push(data);
  });
  chart.update();
}
function removeData(chart) {
  chart.data.labels.pop();
  chart.data.datasets.forEach((dataset) => {
    dataset.data.pop();
  });
  chart.update();
}
function handleNoVotes() {
  var noVotes = false;
  if (voting_west > 0) {
    noVotes = true;
  } else if (voting_east > 0) {
    noVotes = true;
  } else if (voting_north > 0) {
    noVotes = true;
  } else if (voting_south > 0) {
    noVotes = true;
  }

  if (noVotes == false || voting == false) {
    $("#voting_pie").css("opacity", 0);
  } else {
    $("#voting_pie").css("opacity", 1);
  }

}
function updateChart() {
  var changed = false;
  if (old_voting_north != voting_north) {
    changed = true;
  } else if (old_voting_east != voting_east) {
    changed = true;
  } else if (old_voting_south != voting_south) {
    changed = true;
  } else if (old_voting_west != voting_west) {
    changed = true;
  }
  if (changed == true) {
    removeData(PieChart);
    removeData(PieChart);
    removeData(PieChart);
    removeData(PieChart);
    addData(PieChart, "North", voting_north);
    addData(PieChart, "East", voting_east);
    addData(PieChart, "South", voting_south);
    addData(PieChart, "West", voting_west);
    old_voting_north = voting_north;
    old_voting_east = voting_east;
    old_voting_south = voting_south;
    old_voting_west = voting_west;
  }
}
function updateRobotPos() {
  $("#robot").css("top", (17 + (robot_pos_y * 16))*-1 +"%");
  $("#robot").css("left", 3 + (robot_pos_x * 16) +"%");
}
function paint() {
  var html = "<div id='grids'>"
  for (var i=6; i>0; i--) {
    html += "<div id='grid_row'>"
    for (var q=0; q<6; q++) {
      var id = ((i-1)*6)+(q+1);
      html += "<div class='row' id='rowid_" + id + "'></div>"
    }
    html += "</div>"
  }
  html += "</div>"
  $("#robot_map").append(html);
  $("#robot_map").append("<div id='robot'></div>");
  for (var i=1; i<=dots_location.length; i++) {
    $("#robot_map").append("<div class='dot' id='dot" + i + "'></div>");
    $("#dot"+i).css("top", (7 + ((5-dots_location[i-1][0]) * 15.7)) +"%");
    $("#dot"+i).css("left", 7 + (dots_location[i-1][1] * 15.85) +"%");
  }

  $("#rowid_8").css("background-color", "#111");
  $("#rowid_3").css("background-color", "#111");
  $("#rowid_10").css("background-color", "#111");
  $("#rowid_21").css("background-color", "#111");
  $("#rowid_26").css("background-color", "#111");

  $("#rowid_9").css("background-color", "#800020");
  $("#rowid_27").css("background-color", "#00FFFF");
  $("#rowid_4").css("background-color", "#00FFFF");
  $("#rowid_6").css("background-color", "#FFFF00");
  $("#rowid_36").css("background-color", "#00FF00");
}
function makeDots() {
  var dots_amount = 0;
  while(dots_amount<3) {
    var randy = Math.floor(Math.random() * 6);
    var randx = Math.floor(Math.random() * 6);
    if(Map[randy][randx] == 0 && Map[randy][randx] != 6 && (randy != robot_pos_y && randx != robot_pos_x)) {
      Map[randy][randx] = 6;
      dots_location_new[dots_amount][0] = randy;
      dots_location_new[dots_amount][1] = randx;
      dots_amount++;
    }
  }
  dots_changed = true;
  //Paint new dots
  for(var i=0; i<3; i++) {
    $("#dot"+i).remove();
  }
  for (var i=1; i<=dots_location_new.length; i++) {
    $("#robot_map").append("<div class='dot' id='dot" + i + "'></div>");
    $("#dot"+i).css("top", (7 + ((5-dots_location_new[i-1][0]) * 15.7)) +"%");
    $("#dot"+i).css("left", 7 + (dots_location_new[i-1][1] * 15.85) +"%");
  }
}
function dotGame() {
  if (robot_pos_y != last_robot_pos_y || robot_pos_x != last_robot_pos_x) {
    var onDots = false;
    var dotid = -1;
    if(dots_changed == false) {
      for (var i=0; i<dots_location.length; i++) {
        if((robot_pos_y == dots_location[i][0]) && (robot_pos_x == dots_location[i][1])) {
          onDots = true;
          dotid = i+1;
        }
      }
    } else {
      for (var i=0; i<dots_location_new.length; i++) {
        if((robot_pos_y == dots_location_new[i][0]) && (robot_pos_x == dots_location_new[i][1])) {
          onDots = true;
          dotid = i+1;
        }
      }
    }
    if(onDots == true) {
      $("#dot" + dotid).remove();
      dots_collected++;
      $("dot_amount").html(dots_collected);
      if(dots_collected == 3) {
        $("body").append("<video autoplay id='video' src='confetti.mp4'></video>");
        setTimeout(function (){
          $("#video").remove();
          dots_collected = 0;
          makeDots();
          $("dot_amount").html(dots_collected);
        }, 10000);
      }
    }
  }
  last_robot_pos_y = robot_pos_y;
  last_robot_pos_x = robot_pos_x;
}

var Map = [
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0],
  [0,0,0,0,0,0]
];
//Blocks
Map[1][1] = 1
Map[0][2] = 1
Map[1][3] = 1
Map[3][2] = 1
Map[4][1] = 1
//Coloured tiles
Map[1][2] = 5 //Burgandy
Map[0][3] = 4 //Cyan
Map[4][2] = 4 //Cyan
Map[0][5] = 3 //Yellow
Map[5][5] = 2 //Green

var old_voting_north = 0;
var old_voting_east = 0;
var old_voting_south = 0;
var old_voting_west = 0;
var dots_collected = 0;
var last_robot_pos_y = -1;
var last_robot_pos_x = -1;
var PieChart;

updateData();
var dots_changed = false;
var dots_location_new;

$(function() {

  dots_location_new = dots_location;

  var voting_data = [0, 0, 0, 0]

  var ctx = $('#voting_pie');
  var data = {
    labels: ['North', 'East', 'South', 'West'],
    datasets: [{
      data: voting_data,
      backgroundColor: ["#FF0000", "#00FF00","#0000FF","#FFFF00"],
      borderColor: 'rgb(0,0,0)',
      borderWidth: 2
    }]
  };
  PieChart = new Chart(ctx, {
    type: 'pie',
    data: data,
    options: {
      color: ['red', 'blue', 'green', 'yellow'],
      legend: {
        position: 'bottom',
        labels: {
          fontColor: 'black',
          fontSize: 14,
          fontStyle: 'bold'
        }
      },
      animation: {
        duration: 100
      }
    }
  });

  updateData();
  paint();

  setInterval(function() {
    handleNoVotes();
    updateData();
    updateChart();
    updateRobotPos();
    dotGame();
  }, 500);
});
