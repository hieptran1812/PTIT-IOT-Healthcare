(function () {
  "use strict";

  feather.replace();

  var admin = 0;
  var doctor = 0;
  var patient = 0;
  var roles = document.getElementsByClassName("role");
  for (var i = 0; i < roles.length; i++) {
    if (roles[i].innerText === "admin") admin++;
    else if (roles[i].innerText === "doctor") doctor++;
    else patient++;
  }

  var ctx = document.getElementById("myChart");
  var myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["admin", "doctor", "patient"],
      datasets: [
        {
          data: [admin, doctor, patient],
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(54, 162, 235)",
            "rgb(35, 193, 120)",
          ],
        },
      ],
    },
    options: {},
  });
})();
