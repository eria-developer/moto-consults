$(document).ready(function () {
  var searchUrl = "http://127.0.0.1:8000/app/search_placements/";
  $("#search-input").keyup(function () {
    var query = $(this).val();
    $.ajax({
      url: searchUrl,
      data: { query: query },
      success: function (data) {
        var placementsTable = $("#placements-table tbody");
        placementsTable.empty();
        for (var i = 0; i < data.placements.length; i++) {
          var placement = data.placements[i];
          var row = "<tr>";
          row += "<td>" + placement.fullname + "</td>";
          row += "<td>" + placement.job + "</td>";
          row += "<td>" + placement.company + "</td>";
          row += "<td>" + placement.status + "</td>";
          row += '<td><div class="d-flex">';
          row +=
            '<a href="' +
            placement.view_url +
            '" class="btn btn-primary shadow btn-xs sharp me-1"><i class="fa fa-eye"></i></a>';
          row +=
            '<a href="' +
            placement.edit_url +
            '" class="btn btn-primary shadow btn-xs sharp me-1"><i class="fa fa-pencil"></i></a>';
          row +=
            '<a href="' +
            placement.delete_url +
            '" class="btn btn-danger shadow btn-xs sharp"><i class="fa fa-trash"></i></a>';
          row += "</div></td>";
          row += "</tr>";
          placementsTable.append(row);
        }
      },
    });
  });
});
