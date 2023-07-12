
  $('#example').DataTable({
      ajax: {
          url: '../ajax/data/objects_salary.txt',
          dataSrc: '' // Specify the property name in the response data array
      },
      columns: [
          {
              data: 'name'
          },
          {
              data: 'position',
              render: function(data, type, row) {
                  if (type === 'display') {
                      let link = 'http://datatables.net';

                      if (data[0] < 'H') {
                          link = 'http://cloudtables.com';
                      } else if (data[0] < 'S') {
                          link = 'http://editor.datatables.net';
                      }

                      return '<a href="' + link + '">' + data + '</a>';
                  }

                  return data;
              }
          }
      ]
  });


