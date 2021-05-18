(function () {
  "use strict";

  feather.replace();

  var admin = 0;
  var doctor = 0;
  var patient = 0;
  var famPatient = 0;
  var roles = document.getElementsByClassName("role");
  for (var i = 0; i < roles.length; i++) {
    if (roles[i].innerText === "Admin") admin++;
    else if (roles[i].innerText === "Bác sĩ") doctor++;
    else if (roles[i].innerText === "Người nhà bệnh nhân") famPatient++;
    else patient++;
  }

  var ctx = document.getElementById("myChart");
  var myChart = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Bệnh nhân", "Bác sĩ", "Admin", "Người nhà bệnh nhân"],
      datasets: [
        {
          data: [patient, doctor, admin, famPatient],
          backgroundColor: [
            "rgb(255, 99, 132)",
            "rgb(35, 193, 120)",
            "rgb(54, 162, 235)",
            "rgb(133, 212, 171)",
          ],
        },
      ],
    },
    options: {},
  });
})();
