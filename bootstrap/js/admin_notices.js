$(document).ready(function() {
    $.ajax({
       url: '/admin/notices/',
       contentType: 'application/json',
       dataType: 'json',
       success: function(data) {
           $.each(data, function(idx, notice) {
               toastr.warning(notice);
           });
       }
    });
});