// Circle Count Chart
var CHART1_canvas = document.getElementById("circleCount_chart").getContext('2d');

let CHART1 = new Chart(CHART1_canvas, {
  type: 'bar',
  data: {
    labels: daysALL_circle_created_dates_list,
    datasets: [{
      label: "# of circles created",
      data: daysALL_circle_dailyCount_list,
      backgroundColor: [
        'rgba(75, 192, 192, 0.2)'
      ],
      borderColor: [
        'rgba(75, 192, 192, 1)',
      ],
      borderWidth: 0.5
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      },
      xAxes: {
        display: true
      }
      },
    responsive: false,
  }
});
function change_30days() {
  CHART1.destroy();
  CHART1 = new Chart(CHART1_canvas, {
    type: 'bar',
    data: {
      labels: days30_circle_created_dates_list,
      datasets: [{
        label: "# of circles created",
        data: days30_circle_dailyCount_list,
        backgroundColor: [
          'rgba(75, 192, 192, 0.2)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 0.5
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        },
        xAxes: {
          display: true
        }
        },
      responsive: false,
    }
  });
};
function change_ALLdays() {
  CHART1.destroy();
  CHART1 = new Chart(CHART1_canvas, {
    type: 'bar',
    data: {
      labels: daysALL_circle_created_dates_list,
      datasets: [{
        label: "# of circles created",
        data: daysALL_circle_dailyCount_list,
        backgroundColor: [
          'rgba(75, 192, 192, 0.2)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 0.5
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        },
        xAxes: {
          display: true
        }
        },
      responsive: false,
    }
  });
};
function change_365days() {
  CHART1.destroy();
  CHART1 = new Chart(CHART1_canvas, {
    type: 'bar',
    data: {
      labels: days365_circle_created_dates_list,
      datasets: [{
        label: "# of circles created",
        data: days365_circle_dailyCount_list,
        backgroundColor: [
          'rgba(75, 192, 192, 0.2)'
        ],
        borderColor: [
          'rgba(75, 192, 192, 1)',
        ],
        borderWidth: 0.5
      }]
    },
    options: {
      scales: {
        y: {
          beginAtZero: true
        },
        xAxes: {
          display: true
        }
        },
      responsive: false,
    }
  });
};





////////////////////////////////////////////////////////////////////////////////





// Deposit Count Chart
const CHART2_canvas = document.getElementById("depositCount_chart").getContext('2d');

let CHART2 = new Chart(CHART2_canvas, {
  type: 'bar',
  data: {
    labels: deposit_created_dates_list,
    datasets: [{
      label: "# of deposits",
      data: deposit_dailyCount_list,
      backgroundColor: [
        //'rgba(255, 99, 132, 0.2)',
        //'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.5)'
        //'rgba(75, 192, 192, 0.2)'
        //'rgba(153, 102, 255, 0.2)',
        //'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        //'rgba(255, 99, 132, 1)',
        //'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)'
        //'rgba(75, 192, 192, 1)',
        //'rgba(153, 102, 255, 1)',
        //'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 0.5
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
      },
    responsive: false,
  }
});

// loan request Count Chart
const CHART3_canvas = document.getElementById("loanRequestCount_chart").getContext('2d');

let CHART3 = new Chart(CHART3_canvas, {
  type: 'bar',
  data: {
    labels: ['7/5/21','7/6/21','7/7/21','7/8/21','7/9/21','7/10.21'],
    datasets: [{
      label: "# of loan requests",
      data: [0,0,0,0,0,1],
      backgroundColor: [
        //'rgba(255, 99, 132, 0.2)',
        //'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.5)'
        //'rgba(75, 192, 192, 0.2)'
        //'rgba(153, 102, 255, 0.2)',
        //'rgba(255, 159, 64, 0.2)'
      ],
      borderColor: [
        //'rgba(255, 99, 132, 1)',
        //'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)'
        //'rgba(75, 192, 192, 1)',
        //'rgba(153, 102, 255, 1)',
        //'rgba(255, 159, 64, 1)'
      ],
      borderWidth: 0.5
    }]
  },
  options: {
    scales: {
      y: {
        beginAtZero: true
      }
      },
    responsive: false,
  }
});