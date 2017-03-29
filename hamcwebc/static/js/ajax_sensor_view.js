$(document).ready(function(){
    setInterval(function(){
        $.getJSON('http://127.0.0.1:5000/_JSONSensorRead/' + $SENSOR_NAME, {}, function(data) {
            $("#value").text("Value: " + data.value);
        })
    }, 3000);
    $('.updateButton').on('click', function() {
        var limit_id = $(this).attr('limit_id');
        var value = $('#limitInput'+limit_id).val();
        console.log(limit_id);
        req = $.ajax({
            url: 'http://127.0.0.1:5000/update/',
            type: 'POST',
            data: { id: limit_id, value: value}
        });
        console.log(limit_id);
    });
});
