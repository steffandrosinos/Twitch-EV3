function updateData() {
  $("#data_script").remove();
  var script = document.createElement('script');
  script.onload = function () {};
  script.src = "data.js";
  script.id = "data_script";
  document.head.appendChild(script);
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
  updateData();
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
    updateChart();
  }, 500);
});
