
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
            if($('#client').val() === 'summary'){
                $('#homeevents1').removeClass('hidden');
                $('#eventslog').addClass('hidden');
                $('#archiveevents').addClass('hidden');
            }else{
                $('#homeevents1').addClass('hidden');
                $('#eventslog').removeClass('hidden');
                $('#archiveevents').addClass('hidden');
                $.ajax({
                    type: 'POST',
                    url: "/eventselect/",
                    data: {
                        'eventview': $('#client').val(),
                    },
                    dataType: 'html',
                    success: eventSuccess,
                });
            }
        });
    });

    function eventSuccess(data, textStatus, jqXHR)
    {
        $('#eventslog').html(data);
    }
});

$(function () {
    namespace = '/test';
    var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);
    socket.on('connect', function() {
        socket.emit('my event', {data: 'I\'m connected!'});
    });
    var DB_INSERT_EVENT = 'db.inserted';
    socket.on(DB_INSERT_EVENT, function(data) {
        // $('#test').append(data.posted + ' | ' + data.poster + ' | ' + data.event);
        // console.log(data.client, data.event, data.posted, data.poster);
        if ($('#viewtitle').text() === 'EventsClient1') {
            if(data.client === 'client1'){
                $('#eventtable').append('<tr><td style="text-align: center;"><strong>' + data.posted + '</strong></td><td style="text-align: center;><strong>' + data.poster + ' </strong></td><td><strong> ' + data.event + '</strong></td></tr>');
                console.log(data.client, data.event, data.posted, data.poster);
                console.log($('#viewtitle').text());
            } else {
                console.log('not client1');
            }

        } else{
            console.log($('#viewtitle').text());
        }
    if ($('#viewtitle').text() === 'EventsClient2') {
            if(data.client === 'client2'){
                $('#eventtable').append('<tr><td style="text-align: center;"><strong>' + data.posted + '</strong></td><td style="text-align: center;><strong>' + data.poster + ' </strong></td><td><strong> ' + data.event + '</strong></td></tr>');
                console.log(data.client, data.event, data.posted, data.poster);
                console.log($('#viewtitle').text());
            } else {
                console.log('not client2');
            }

        } else{
            console.log($('#viewtitle').text());
        }
    if ($('#viewtitle').text() === 'EventsClient3') {
            if(data.client === 'client3'){
                $('#eventtable').append('<tr><td style="text-align: center;"><strong>' + data.posted + '</strong></td><td style="text-align: center;><strong>' + data.poster + ' </strong></td><td><strong> ' + data.event + '</strong></td></tr>');
                console.log(data.client, data.event, data.posted, data.poster);
                console.log($('#viewtitle').text());
            } else {console.log('not client3');}
        }else{
            console.log($('#viewtitle').text());
        }
     if ($('#viewtitle').text() === 'Summary') {
            if(data.client === 'client1'){
                $('#client1table').append('<tr><td style="text-align: center;"><strong>' + data.posted + '</strong></td><td style="text-align: center;"><strong>' + data.poster + ' </strong></td><td><strong> ' + data.event + '</strong></td></tr>');
            } else  if(data.client === 'client2') {
                $('#client2table').append('<tr><td style="text-align: center;"><strong>' + data.posted + '</strong></td><td style="text-align: center;"><strong>' + data.poster + ' </strong></td><td><strong> ' + data.event + '</strong></td></tr>');
            } else if(data.client === 'client3'){
                $('#client3table').append('<tr><td style="text-align: center;"><strong>' + data.posted + '</strong></td><td style="text-align: center;"><strong>' + data.poster + ' </strong></td><td><strong> ' + data.event + '</strong></td></tr>');
            } else {  console.log('not client3'); }
        } else{ console.log($('#viewtitle').text());}
    });
});

$(function() {
    $("#alertscount").click(function(){
        $(".alertstitle").toggleClass('hidden');
        $(".alertsbody").not(".hidden").addClass("hidden")
    });
});

$(function() {
    $(".alertstitle").click(function(){
        $(this).next().toggleClass('hidden');
    });
});

$(function() {
    $('#dateside').datepicker({
        todayHighlight: true,
    }).on('changeDate', function() {

        $('#homeevents1').addClass('hidden');
        $('#eventslog').addClass('hidden');
        // $('.view-form').addClass('hidden');
        $('#archiveevents').removeClass('hidden');
        $('#homedate').datepicker(
                                  'setDate', $(this).datepicker('getDate')
                                  );
        $.ajax({
                type: 'POST',
                url: "/archive/",
                data: {
                    'datecal': $('#homedate').val(),
                },
                dataType: 'html',
                success: eventSuccess,
        });
    });
});

function eventSuccess(data, textStatus, jqXHR)
    {
        $('#archiveevents').html(data);
    }

$(function() {
    if(window.location.pathname === '/search/'){
        $("#datecont").addClass('hidden');
    }
});

$(function() {
    $(".addeventbtn").click(function() {
        if($('#clientlist').val() === '') {
            alert("You must select a client.");
        }
    });
});

$(function() {
    $("#on_day").datepicker({
        'format': 'yyyy-mm-dd',
        'orientation': 'top auto',
        'autoclose': true,
    });
    $("#start_date").datepicker({
        'format': 'yyyy-mm-dd',
        'orientation': 'top auto',
        'autoclose': true,
    });
        $("#end_date").datepicker({
        'format': 'yyyy-mm-dd',
        'orientation': 'top auto',
        'autoclose': true,
    });
        $("#alert_startdate").datepicker({
        'format': 'yyyy-mm-dd',
        'orientation': 'top auto',
        'autoclose': true,
    });
        $("#alert_enddate").datepicker({
        'format': 'yyyy-mm-dd',
        'orientation': 'top auto',
        'autoclose': true,
    });
});
