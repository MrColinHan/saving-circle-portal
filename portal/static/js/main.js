// Circle Count Chart
var CHART1_canvas = document.getElementById("circleCount_chart").getContext('2d');
// deposit count chart
var CHART2_canvas = document.getElementById("depositCount_chart").getContext('2d');

//////////////////////////////Initiate Circle Chart//////////////////////////////////////////////////
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

//////////////////////////////Initiate Deposits Chart//////////////////////////////////////////////////

let CHART2 = new Chart(CHART2_canvas, {
  type: 'bar',
  data: {
    labels: daysALL_deposit_created_dates_list,
    datasets: [{
      label: "# of deposits created",
      data: daysALL_deposit_dailyCount_list,
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

//////////////////////////////Button functions//////////////////////////////////////////////////
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

  CHART2.destroy();
  CHART2 = new Chart(CHART2_canvas, {
    type: 'bar',
    data: {
      labels: days30_deposit_created_dates_list,
      datasets: [{
        label: "# of deposits created",
        data: days30_deposit_dailyCount_list,
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
  CHART2.destroy();
  CHART2 = new Chart(CHART2_canvas, {
    type: 'bar',
    data: {
      labels: daysALL_deposit_created_dates_list,
      datasets: [{
        label: "# of deposits created",
        data: daysALL_deposit_dailyCount_list,
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
  CHART2.destroy();
  CHART2 = new Chart(CHART2_canvas, {
    type: 'bar',
    data: {
      labels: days365_deposit_created_dates_list,
      datasets: [{
        label: "# of deposits created",
        data: days365_deposit_dailyCount_list,
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
