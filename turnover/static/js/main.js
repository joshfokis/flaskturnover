
// $(function() {
//     $('#client').change(function() {
//         alert(("#client").val());
//         if($('#client1') === ("#client").val()){
//             $('#client1').removeClass('hidden');
//             $('#client2').addClass('hidden');
//             $('#client3').addClass('hidden');
//             alert(("#client").val());
//         }else if($('#client2') === ("#client").val()){
//             $('#client2').removeClass('hidden');
//             $('#client1').addClass('hidden');
//             $('#client3').addClass('hidden');
//             alert(("#client").val());
//         }else{
//             $('#client3').removeClass('hidden');
//             $('#client2').addClass('hidden');
//             $('#client1').addClass('hidden');
//             alert(("#client").val());
//         }
//     });
// });

$(function () {
    var csrftoken = $('meta[name=csrf-token]').attr('content');

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

    $(function() {
        $('#client').change(function() {
            $('#homeevents').addClass('hidden')

            $.ajax({
                type: 'POST',
                url: "/eventselect/",
                data: {
                    'eventview': $('#client').val(),
                },
                dataType: 'html',
                success: eventSuccess,
            });
        });
    });

    function eventSuccess(data, textStatus, jqXHR)
    {
        $('#eventslog').html(data);
    }
});
