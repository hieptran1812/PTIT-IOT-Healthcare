(function () {
  "use strict";

  feather.replace();

  var ctx = document.getElementById("myChart");

  var myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: [
        "admin",
        "Bác sĩ",
        "Bệnh nhân"
      ],
      datasets: [
        {
          data: [1,4,0],
          backgroundColor: [
            "rgba(255, 99, 132, 1)",
            "rgba(54, 162, 235, 1)"
          ],
        },
      ],
    },
    options: {
    },
  });
})();
