$(document).ready(function () {
  var searchUrl = "http://127.0.0.1:8000/app/search_customers/";
  $("#search-input").keyup(function () {
    var query = $(this).val();
    $.ajax({
      url: searchUrl,
      data: { query: query },
      success: function (data) {
        var customersTable = $("#customers-table tbody");
        customersTable.empty();
        for (var i = 0; i < data.customers.length; i++) {
          var customer = data.customers[i];
          var row = "<tr>";
          row += "<td>" + customer.firstname + "</td>";
          row += "<td>" + customer.othernames + "</td>";
          row += "<td>" + customer.phonenumber_1 + "</td>";
          row += "<td>" + customer.phonenumber_2 + "</td>";
          row += "<td>" + customer.email + "</td>";
          row += "<td>" + customer.address + "</td>";
          row += '<td><div class="d-flex">';
          row +=
            '<a href="' +
            customer.view_url +
            $(document).ready(function () {
              var searchUrl = "http://127.0.0.1:8000/app/search_customers/";
              $("#search-input").keyup(function () {
                var query = $(this).val();
                $.ajax({
                  url: searchUrl,
                  data: { query: query },
                  success: function (data) {
                    var customersTable = $("#customers-table tbody");
                    customersTable.empty();
                    for (var i = 0; i < data.customers.length; i++) {
                      var customer = data.customers[i];
                      var row = "<tr>";
                      row += "<td>" + customer.firstname + "</td>";
                      row += "<td>" + customer.othernames + "</td>";
                      row += "<td>" + customer.phonenumber_1 + "</td>";
                      row += "<td>" + customer.phonenumber_2 + "</td>";
                      row += "<td>" + customer.email + "</td>";
                      row += "<td>" + customer.address + "</td>";
                      row += '<td class="text-center">';
                      row += '<a href="' + customer.view_url + '">';
                      row +=
                        '<button type="button" class="btn btn-xs btn-info mb-2"><i class="fa fa-eye"></i></button>';
                      row += "</a>";
                      row +=
                        '<button type="button" class="btn btn-xs btn-warning mb-2" data-bs-toggle="modal" data-bs-target="#editCustomer' +
                        customer.id +
                        '"><i class="fa fa-pencil"></i></button>';
                      row +=
                        '<button type="button" class="btn btn-xs btn-primary mb-2" data-bs-toggle="modal" data-bs-target="#deleteCustomer' +
                        customer.id +
                        '"><i class="fa fa-trash"></i></button>';
                      row += "</td>";
                      row += "</tr>";
                      customersTable.append(row);
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
            customer.edit_url +
            '" class="btn btn-primary shadow btn-xs sharp me-1"><i class="fa fa-pencil"></i></a>';
          row +=
            '<a href="' +
            customer.delete_url +
            '" class="btn btn-danger shadow btn-xs sharp"><i class="fa fa-trash"></i></a>';
          row += "</div></td>";
          row += "</tr>";
          customersTable.append(row);
        }
      },
    });
  });
});
