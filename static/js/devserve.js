// Data Table
$(document).ready(function() {
    $('#sortedtable').DataTable();
});

// $(document).ready(function() {
//     $('#sortedtable').DataTable({
//         "order": [[1, "desc"]],
//         "pageLength": 10,
//     });
// });


// Binary status changes
function status_change() {
    var abc = confirm('Do you want to change the status on this item?');
    return abc
    }