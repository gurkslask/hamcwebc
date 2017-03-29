$(document).ready(function(){
    setInterval(function(){
        $.getJSON('http://127.0.0.1:5000/_JSONSensorRead/' + $SENSOR_NAME, {}, function(data) {
            $("#value").text("Value: " + data.value);
        })
    }, 3000);
});
