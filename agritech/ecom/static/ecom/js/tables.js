$('#example').DataTable({
    ajax: '../ajax/data/objects_salary.txt',
    columns: [
        {
            data: 'name',
        },
        {
            data: 'position',
            render: function (data, type) {
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
            },
        },
        {
            className: 'f32', // used by world-flags-sprite library
            data: 'office',
            render: function (data, type) {
                if (type === 'display') {
                    let country = '';
 
                    switch (data) {
                        case 'Argentina':
                            country = 'ar';
                            break;
                        case 'Edinburgh':
                            country = '_Scotland';
                            break;
                        case 'London':
                            country = '_England';
                            break;
                        case 'New York':
                        case 'San Francisco':
                            country = 'us';
                            break;
                        case 'Sydney':
                            country = 'au';
                            break;
                        case 'Tokyo':
                            country = 'jp';
                            break;
                    }
 
                    return '<span class="flag ' + country + '"></span> ' + data;
                }
 
                return data;
            },
        },
        {
            data: 'extn',
            render: function (data, type, row, meta) {
                return type === 'display'
                    ? '<progress value="' + data + '" max="9999"></progress>'
                    : data;
            },
        },
        {
            data: 'start_date',
        },
        {
            data: 'salary',
            render: function (data, type) {
                var number = $.fn.dataTable.render
                    .number(',', '.', 2, '$')
                    .display(data);
 
                if (type === 'display') {
                    let color = 'green';
                    if (data < 250000) {
                        color = 'red';
                    } else if (data < 500000) {
                        color = 'orange';
                    }
 
                    return '<span style="color:' + color + '">' + number + '</span>';
                }
 
                return number;
            },
        },
    ],
});

const data = [
    {
      name: "Tiger Nixon",
      position: "System Architect",
      salary: "320800",
      start_date: "2011/04/25",
      office: "Edinburgh",
      extn: "5421"
    },
    {
        "name": "Garrett Winters",
        "position": "Accountant",
        "salary": "170750",
        "start_date": "2011/07/25",
        "office": "Tokyo",
        "extn": "8422"
      },
      {
        "name": "Ashton Cox",
        "position": "Junior Technical Author",
        "salary": "86000",
        "start_date": "2009/01/12",
        "office": "San Francisco",
        "extn": "1562"
      },
      {
        "name": "Cedric Kelly",
        "position": "Senior Javascript Developer",
        "salary": "433060",
        "start_date": "2012/03/29",
        "office": "Edinburgh",
        "extn": "6224"
      },
      {
        "name": "Airi Satou",
        "position": "Accountant",
        "salary": "162700",
        "start_date": "2008/11/28",
        "office": "Tokyo",
        "extn": "5407"
      },
      {
        "name": "Brielle Williamson",
        "position": "Integration Specialist",
        "salary": "372000",
        "start_date": "2012/12/02",
        "office": "New York",
        "extn": "4804"
      },
      {
        "name": "Herrod Chandler",
        "position": "Sales Assistant",
        "salary": "137500",
        "start_date": "2012/08/06",
        "office": "San Francisco",
        "extn": "9608"
      },
      {
        "name": "Rhona Davidson",
        "position": "Integration Specialist",
        "salary": "327900",
        "start_date": "2010/10/14",
        "office": "Tokyo",
        "extn": "6200"
      },
      {
        "name": "Colleen Hurst",
        "position": "Javascript Developer",
        "salary": "205500",
        "start_date": "2009/09/15",
        "office": "San Francisco",
        "extn": "2360"
      },
      {
        "name": "Sonya Frost",
        "position": "Software Engineer",
        "salary": "103600",
        "start_date": "2008/12/13",
        "office": "Edinburgh",
        "extn": "1667"
      },
      {
        "name": "Jena Gaines",
        "position": "Office Manager",
        "salary": "90560",
        "start_date": "2008/12/19",
        "office": "London",
        "extn": "3814"
      },
      {
        "name": "Quinn Flynn",
        "position": "Support Lead",
        "salary": "342000",
        "start_date": "2013/03/03",
        "office": "Edinburgh",
        "extn": "9497"
      },
      {
        "name": "Charde Marshall",
        "position": "Regional Director",
        "salary": "470600",
        "start_date": "2008/10/16",
        "office": "San Francisco",
        "extn": "6741"
      },
      {
        "name": "Haley Kennedy",
        "position": "Senior Marketing Designer",
        "salary": "313500",
        "start_date": "2012/12/18",
        "office": "London",
        "extn": "3597"
      },
    // Add more objects to the array if needed
  ];
