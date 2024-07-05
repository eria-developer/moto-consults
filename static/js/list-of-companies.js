$(document).ready(function () {
  var searchUrl = "http://127.0.0.1:8000/app/search_companies/";
  $("#search-input").keyup(function () {
    var query = $(this).val();
    $.ajax({
      url: searchUrl,
      data: { query: query },
      success: function (data) {
        var companiesTable = $("#companies-table tbody");
        companiesTable.empty();
        for (var i = 0; i < data.companies.length; i++) {
          var company = data.companies[i];
          var row = "<tr>";
          row += "<td>" + company.name + "</td>";
          row += "<td>" + company.email + "</td>";
          row += "<td>" + company.phone_number + "</td>";
          row += "<td>" + company.address + "</td>";
          row += '<td><div class="d-flex">';
          row +=
            '<a href="' +
            company.view_url +
            $(document).ready(function () {
              var searchUrl = "http://127.0.0.1:8000/app/search_companies/";
              $("#search-input").keyup(function () {
                var query = $(this).val();
                $.ajax({
                  url: searchUrl,
                  data: { query: query },
                  success: function (data) {
                    var companiesTable = $("#companies-table tbody");
                    companiesTable.empty();
                    for (var i = 0; i < data.companies.length; i++) {
                      var company = data.companies[i];
                      var row = "<tr>";
                      row += "<td>" + company.name + "</td>";
                      row += "<td>" + company.email + "</td>";
                      row += "<td>" + company.phone_number+ "</td>";
                      row += "<td>" + company.address + "</td>";
                      row += '<td class="text-center">';
                      row += '<a href="' + company.view_url + '">';
                      row +=
                        '<button type="button" class="btn btn-xs btn-info mb-2"><i class="fa fa-eye"></i></button>';
                      row += "</a>";
                      row +=
                        '<button type="button" class="btn btn-xs btn-warning mb-2" data-bs-toggle="modal" data-bs-target="#editCompany' +
                        company.id +
                        '"><i class="fa fa-pencil"></i></button>';
                      row +=
                        '<button type="button" class="btn btn-xs btn-primary mb-2" data-bs-toggle="modal" data-bs-target="#deleteCompany' +
                        company.id +
                        '"><i class="fa fa-trash"></i></button>';
                      row += "</td>";
                      row += "</tr>";
                      companiesTable.append(row);
                    }
                  },
                  error: function () {
                    console.error(
                      "An error occurred while fetching search results."
                    );
                  },
                });
              });
            });

          ('" class="btn btn-primary shadow btn-xs sharp me-1"><i class="fa fa-eye"></i></a>');
          row +=
            '<a href="' +
            company.edit_url +
            '" class="btn btn-primary shadow btn-xs sharp me-1"><i class="fa fa-pencil"></i></a>';
          row +=
            '<a href="' +
            company.delete_url +
            '" class="btn btn-danger shadow btn-xs sharp"><i class="fa fa-trash"></i></a>';
          row += "</div></td>";
          row += "</tr>";
          companiesTable.append(row);
        }
      },
    });
  });
});
