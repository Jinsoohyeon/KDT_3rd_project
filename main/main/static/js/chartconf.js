const data = {
              labels: labels,
              datasets: [{
                label: '리뷰수',
                backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(255, 159, 64, 0.2)',
                'rgba(255, 205, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(201, 203, 207, 0.2)'
                ],
                borderColor: [
                'rgb(255, 99, 132)',
                'rgb(255, 159, 64)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
                'rgb(54, 162, 235)',
                'rgb(153, 102, 255)',
                'rgb(201, 203, 207)'
                ],
                borderWidth: 1,
                data: cnt_review ,
                datalabels: {
                align: 'center',
                anchor: 'center'
                }
              }]
            };
            const config = {
              type: 'bar',
              data: data,
              options: {
                plugins: {
                    legend: {
                        display: false
                    }
                },
              scales: {
                x: {
                    ticks: {
                        Align: 'end',
                        // fontColor: 'red'
                },
                    grid: {
                    display: false,
                    }
                },
                y: {
                    grid: {
                    display: false
                    },
                },
                }
            }};

const data2 = {
  labels: labels2,
  datasets: [{
    label: '언급량',
    backgroundColor: [
    'rgba(255, 99, 132, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgba(255, 205, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(201, 203, 207, 0.2)'
    ],
    borderColor: [
    'rgb(255, 99, 132)',
    'rgb(255, 159, 64)',
    'rgb(255, 205, 86)',
    'rgb(75, 192, 192)',
    'rgb(54, 162, 235)',
    'rgb(153, 102, 255)',
    'rgb(201, 203, 207)'
    ],
    borderWidth: 1,
    data: cnt_word,
  }]
};
const config2 = {
  type: 'bar',
  data: data2,
  options: {
    plugins: {
        legend: {
            display: false
        }
    },
  scales: {
    x: {
        ticks: {
            Align: 'end',
            // fontColor: 'red'
    },
        grid: {
        display: false,
        }
    },
    y: {
        grid: {
        display: false
        },
    },
    }
}};

const data3 = {
  labels: labels3,
  datasets: [{
    label: '리뷰수',
    backgroundColor: [
    'rgba(255, 99, 132, 0.2)',
    'rgba(255, 159, 64, 0.2)',
    'rgba(255, 205, 86, 0.2)',
    'rgba(75, 192, 192, 0.2)',
    'rgba(54, 162, 235, 0.2)',
    'rgba(153, 102, 255, 0.2)',
    'rgba(201, 203, 207, 0.2)'
    ],
    borderColor: [
    'rgb(255, 99, 132)',
    'rgb(255, 159, 64)',
    'rgb(255, 205, 86)',
    'rgb(75, 192, 192)',
    'rgb(54, 162, 235)',
    'rgb(153, 102, 255)',
    'rgb(201, 203, 207)'
    ],
    borderWidth: 1,
    data: cnt_keyword,
    datalabels: {
      align: 'center',
      anchor: 'center'
      }
  }]
};
const config3 = {
  type: 'bar',
  data: data3,
  // data: [1,1,2,3],
  options: {
    plugins: {
        legend: {
            display: false
        }
    },
  scales: {
    x: {
        ticks: {
            Align: 'end',
            // fontColor: 'red'
    },
        grid: {
        display: false,
        }
    },
    y: {
        grid: {
        display: false
        },
    },
    }
}};

$(function() {
    const myChart = new Chart(
        document.getElementById('myChart'),
        config
      );
      const cntChart = new Chart(
          document.getElementById('bar-chart'),
          config2
      );
      const wordChart = new Chart(
          document.getElementById('wordcnt-chart'),
          config3
      )
});