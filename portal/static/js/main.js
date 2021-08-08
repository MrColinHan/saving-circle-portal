// Circle Count Chart
var CHART1_canvas = document.getElementById("circleCount_chart").getContext('2d');
// deposit count chart
var CHART2_canvas = document.getElementById("depositCount_chart").getContext('2d');
// request count chart
var CHART3_canvas = document.getElementById("requestCount_chart").getContext('2d');
// deposit amount chart
var CHART4_canvas = document.getElementById("depositAmount_chart").getContext('2d');
// request amount chart
var CHART5_canvas = document.getElementById("requestAmount_chart").getContext('2d');


//////////////////////////////Initiate Circle Chart//////////////////////////////////////////////////
let CHART1 = new Chart(CHART1_canvas, {
  type: 'bar',
  data: {
    labels: daysALL_circle_created_dates_list,
    datasets: [{
      label: "# of circles created",
      data: daysALL_circle_dailyCount_list,
      backgroundColor: [
        'rgba(53,208,127,1.00)'
      ],
      borderColor: [
        'rgba(53,208,127,1.00)',
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
      label: "# of deposits made",
      data: daysALL_deposit_dailyCount_list,
      backgroundColor: [
        'rgba(53,208,127,1.00)'
      ],
      borderColor: [
        'rgba(53,208,127,1.00)',
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

//////////////////////////////Initiate Deposits Amount Chart//////////////////////////////////////////////////

let CHART4 = new Chart(CHART4_canvas, {
  type: 'bar',
  data: {
    labels: daysALL_deposit_created_dates_list,
    datasets: [{
      label: "$ of deposits made",
      data: daysALL_deposit_dailyAmount_list,
      backgroundColor: [
        'rgba(53,208,127,1.00)'
      ],
      borderColor: [
        'rgba(53,208,127,1.00)',
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

//////////////////////////////Initiate Request Amount Chart//////////////////////////////////////////////////

let CHART5 = new Chart(CHART5_canvas, {
  type: 'bar',
  data: {
    labels: daysALL_request_created_dates_list,
    datasets: [{
      label: "$ of requests made",
      data: daysALL_request_dailyAmount_list,
      backgroundColor: [
        'rgba(53,208,127,1.00)'
      ],
      borderColor: [
        'rgba(53,208,127,1.00)',
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

//////////////////////////////Initiate Request Chart//////////////////////////////////////////////////
let CHART3 = new Chart(CHART3_canvas, {
  type: 'bar',
  data: {
    labels: daysALL_request_created_dates_list,
    datasets: [{
      label: "# of requests made",
      data: daysALL_request_dailyCount_list,
      backgroundColor: [
        'rgba(53,208,127,1.00)'
      ],
      borderColor: [
        'rgba(53,208,127,1.00)',
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
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
        label: "# of deposits made",
        data: days30_deposit_dailyCount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART3.destroy();
  CHART3 = new Chart(CHART3_canvas, {
    type: 'bar',
    data: {
      labels: days30_request_created_dates_list,
      datasets: [{
        label: "# of requests made",
        data: days30_request_dailyCount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART4.destroy();
  CHART4 = new Chart(CHART4_canvas, {
    type: 'bar',
    data: {
      labels: days30_deposit_created_dates_list,
      datasets: [{
        label: "$ of requests made",
        data: days30_deposit_dailyAmount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART5.destroy();
  CHART5 = new Chart(CHART5_canvas, {
    type: 'bar',
    data: {
      labels: days30_request_created_dates_list,
      datasets: [{
        label: "$ of requests made",
        data: days30_request_dailyAmount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
        label: "# of deposits made",
        data: daysALL_deposit_dailyCount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART3.destroy();
  CHART3 = new Chart(CHART3_canvas, {
    type: 'bar',
    data: {
      labels: daysALL_request_created_dates_list,
      datasets: [{
        label: "# of requests made",
        data: daysALL_request_dailyCount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART4.destroy();
  CHART4 = new Chart(CHART4_canvas, {
    type: 'bar',
    data: {
      labels: daysALL_deposit_created_dates_list,
      datasets: [{
        label: "$ of deposits made",
        data: daysALL_deposit_dailyAmount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART5.destroy();
  CHART5 = new Chart(CHART5_canvas, {
    type: 'bar',
    data: {
      labels: daysALL_request_created_dates_list,
      datasets: [{
        label: "$ of requests made",
        data: daysALL_request_dailyAmount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
function change_7days() {
  CHART1.destroy();
  CHART1 = new Chart(CHART1_canvas, {
    type: 'bar',
    data: {
      labels: days7_circle_created_dates_list,
      datasets: [{
        label: "# of circles created",
        data: days7_circle_dailyCount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
      labels: days7_deposit_created_dates_list,
      datasets: [{
        label: "# of deposits made",
        data: days7_deposit_dailyCount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART3.destroy();
  CHART3 = new Chart(CHART3_canvas, {
    type: 'bar',
    data: {
      labels: days7_request_created_dates_list,
      datasets: [{
        label: "# of requests made",
        data: days7_request_dailyCount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART4.destroy();
  CHART4 = new Chart(CHART4_canvas, {
    type: 'bar',
    data: {
      labels: days7_deposit_created_dates_list,
      datasets: [{
        label: "# of deposits made",
        data: days7_deposit_dailyAmount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
  CHART5.destroy();
  CHART5 = new Chart(CHART5_canvas, {
    type: 'bar',
    data: {
      labels: days7_request_created_dates_list,
      datasets: [{
        label: "$ of requests made",
        data: days7_request_dailyAmount_list,
        backgroundColor: [
          'rgba(53,208,127,1.00)'
        ],
        borderColor: [
          'rgba(53,208,127,1.00)',
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
