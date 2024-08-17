(function ($) {
  'use strict';
  $(function () {

    if ($("#performanceLine").length) {
      const ctx = document.getElementById('performanceLine').getContext('2d');
      var saleGradientBg = ctx.createLinearGradient(5, 0, 5, 100);
      saleGradientBg.addColorStop(0, 'rgba(26, 115, 232, 0.18)');
      saleGradientBg.addColorStop(1, 'rgba(26, 115, 232, 0.02)');
      var saleGradientBg2 = ctx.createLinearGradient(100, 0, 50, 150);
      saleGradientBg2.addColorStop(0, 'rgba(0, 208, 255, 0.19)');
      saleGradientBg2.addColorStop(1, 'rgba(0, 208, 255, 0.03)');

      new Chart(ctx, {
        type: 'line',
        data: {
          labels: ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
          datasets: [{
            label: 'This week',
            data: [50, 110, 60, 290, 200, 115, 130],
            backgroundColor: saleGradientBg,
            borderColor: '#1F3BB3',
            borderWidth: 1.5,
            fill: true,
            pointBorderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 2,
            pointBackgroundColor: '#1F3BB3',
            pointBorderColor: '#fff'
          },
          {
            label: 'Last week',
            data: [30, 150, 190, 250, 120, 150, 130],
            backgroundColor: saleGradientBg2,
            borderColor: '#52CDFF',
            borderWidth: 1.5,
            fill: true,
            pointBorderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 2,
            pointBackgroundColor: '#52CDFF',
            pointBorderColor: '#fff'
          }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4
            }
          },
          scales: {
            y: {
              display: true,
              grid: {
                display: true,
                color: "#F0F0F0",
                drawBorder: false
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 4,
                color: "#6B778C",
                font: {
                  size: 10
                }
              }
            },
            x: {
              display: true,
              grid: {
                display: false,
                drawBorder: false
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                color: "#6B778C",
                font: {
                  size: 10
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });
    }

    if ($("#status-summary").length) {
      const ctxStatusSummary = document.getElementById('status-summary').getContext('2d');
      new Chart(ctxStatusSummary, {
        type: 'line',
        data: {
          labels: ["SUN", "MON", "TUE", "WED", "THU", "FRI"],
          datasets: [{
            label: '# of Votes',
            data: [50, 68, 70, 10, 12, 80],
            backgroundColor: "#ffcc00",
            borderColor: '#01B6A0',
            borderWidth: 2,
            fill: false,
            pointBorderWidth: 0,
            pointRadius: 0,
            pointHoverRadius: 0,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4,
            }
          },
          scales: {
            y: {
              display: false,
              grid: {
                display: false,
              },
            },
            x: {
              display: false,
              grid: {
                display: false,
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
        }
      });
    }

    if ($("#marketingOverview").length) {
      const ctxMarketingOverview = document.getElementById('marketingOverview').getContext('2d');
      new Chart(ctxMarketingOverview, {
        type: 'bar',
        data: {
          labels: ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"],
          datasets: [{
            label: 'Last week',
            data: [110, 220, 200, 190, 220, 110, 210, 110, 205, 202, 201, 150],
            backgroundColor: "#52CDFF",
            borderColor: '#52CDFF',
            borderWidth: 0,
            barPercentage: 0.35,
            fill: true,
          },
          {
            label: 'This week',
            data: [215, 290, 210, 250, 290, 230, 290, 210, 280, 220, 190, 300],
            backgroundColor: "#1F3BB3",
            borderColor: '#1F3BB3',
            borderWidth: 0,
            barPercentage: 0.35,
            fill: true,
          }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4,
            }
          },
          scales: {
            y: {
              display: true,
              grid: {
                display: true,
                drawTicks: false,
                color: "#F0F0F0",
                zeroLineColor: '#F0F0F0',
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 4,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            },
            x: {
              display: true,
              stacked: true,
              grid: {
                display: false,
                drawTicks: false,
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
        }
      });
    }

    if ($("#doughnutChart").length) {
      const ctxDoughnutChart = document.getElementById('doughnutChart').getContext('2d');
      new Chart(ctxDoughnutChart, {
        type: 'doughnut',
        data: {
          labels: ['Total', 'Net', 'Gross', 'AVG'],
          datasets: [{
            data: [40, 20, 30, 10],
            backgroundColor: [
              "#1F3BB3",
              "#FDD0C7",
              "#52CDFF",
              "#81DADA"
            ],
            borderColor: [
              "#1F3BB3",
              "#FDD0C7",
              "#52CDFF",
              "#81DADA"
            ],
          }]
        },
        options: {
          cutout: 90,
          animationEasing: "easeOutBounce",
          animateRotate: true,
          animateScale: false,
          responsive: true,
          maintainAspectRatio: true,
          showScale: true,
          plugins: {
            legend: {
              display: false,
            }
          }
        }
      });
    }

    if ($("#leaveReport").length) {
      const ctxLeaveReport = document.getElementById('leaveReport').getContext('2d');
      new Chart(ctxLeaveReport, {
        type: 'bar',
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May"],
          datasets: [{
            label: 'Last week',
            data: [18, 25, 39, 11, 24],
            backgroundColor: "#52CDFF",
            borderColor: '#52CDFF',
            borderWidth: 0,
            fill: true,
            barPercentage: 0.5,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4,
            }
          },
          scales: {
            y: {
              display: true,
              grid: {
                display: false,
                drawBorder: false,
                color: "rgba(255,255,255,.05)",
                zeroLineColor: "rgba(255,255,255,.05)",
              },
              ticks: {
                beginAtZero: true,
                autoSkip: true,
                maxTicksLimit: 5,
                fontSize: 10,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            },
            x: {
              display: true,
              grid: {
                display: false,
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
        }
      });
    }

    if ($("#candleStick").length) {
      const ctxCandleStick = document.getElementById('candleStick').getContext('2d');
      new Chart(ctxCandleStick, {
        type: 'bar',
        data: {
          labels: ["Jan", "Feb", "Mar", "Apr", "May"],
          datasets: [{
            label: 'Last week',
            data: [18, 25, 39, 11, 24],
            backgroundColor: "#52CDFF",
            borderColor: '#52CDFF',
            borderWidth: 0,
            fill: true,
            barPercentage: 0.5,
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4,
            }
          },
          scales: {
            y: {
              display: true,
              grid: {
                display: false,
                drawBorder: false,
                color: "rgba(255,255,255,.05)",
                zeroLineColor: "rgba(255,255,255,.05)",
              },
              ticks: {
                beginAtZero: true,
                autoSkip: true,
                maxTicksLimit: 5,
                fontSize: 10,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            },
            x: {
              display: true,
              grid: {
                display: false,
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                color: "#6B778C",
                font: {
                  size: 10,
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false,
            }
          }
        }
      });
    }

    if ($("#average").length) {
      const ctxAverage = document.getElementById('average').getContext('2d');
      new Chart(ctxAverage, {
        type: 'line',
        data: {
          labels: ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"],
          datasets: [{
            label: 'This week',
            data: [50, 110, 60, 290, 200, 115, 130],
            backgroundColor: saleGradientBg,
            borderColor: '#1F3BB3',
            borderWidth: 1.5,
            fill: true,
            pointBorderWidth: 1,
            pointRadius: 4,
            pointHoverRadius: 2,
            pointBackgroundColor: '#1F3BB3',
            pointBorderColor: '#fff'
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          elements: {
            line: {
              tension: 0.4
            }
          },
          scales: {
            y: {
              display: true,
              grid: {
                display: true,
                color: "#F0F0F0",
                drawBorder: false
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 4,
                color: "#6B778C",
                font: {
                  size: 10
                }
              }
            },
            x: {
              display: true,
              grid: {
                display: false,
                drawBorder: false
              },
              ticks: {
                beginAtZero: false,
                autoSkip: true,
                maxTicksLimit: 7,
                color: "#6B778C",
                font: {
                  size: 10
                }
              }
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });
    }







  });

})(jQuery);
