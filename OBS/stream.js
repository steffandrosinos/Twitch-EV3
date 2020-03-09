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
  if (voting_left > 0) {
    noVotes = true;
  } else if (voting_right > 0) {
    noVotes = true;
  } else if (voting_forward > 0) {
    noVotes = true;
  } else if (voting_backwards > 0) {
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
  if (old_voting_left != voting_left) {
    changed = true;
  } else if (old_voting_right != voting_right) {
    changed = true;
  } else if (old_voting_forward != voting_forward) {
    changed = true;
  } else if (old_voting_backwards != voting_backwards) {
    changed = true;
  }
  if (changed == true) {
    removeData(PieChart);
    removeData(PieChart);
    removeData(PieChart);
    removeData(PieChart);
    addData(PieChart, "Left", voting_left);
    addData(PieChart, "Right", voting_right);
    addData(PieChart, "Forward", voting_forward);
    addData(PieChart, "Backwards", voting_backwards);
    old_voting_left = voting_left;
    old_voting_right = voting_right;
    old_voting_forward = voting_forward;
    old_voting_backwards = voting_backwards;
  }
}
function updateRobotPos() {
  $("#robot").css("top", (17 + (robot_pos_y * 16))*-1 +"%");
  $("#robot").css("left", 3 + (robot_pos_x * 16) +"%");
}

var old_voting_left = 0;
var old_voting_right = 0;
var old_voting_forward = 0;
var old_voting_backwards = 0;
var PieChart;

updateData();

$(function() {

  var voting_data = [0, 0, 0, 0]

  var ctx = $('#voting_pie');
  var data = {
    labels: ['Left','Right','Forward','Backwards'],
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

  setInterval(function() {
    handleNoVotes();
    updateData();
    updateChart();
    updateRobotPos();
  }, 500);
});
