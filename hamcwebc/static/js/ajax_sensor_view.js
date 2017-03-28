$(document).ready(function(){
    setInterval(function(){
        $.getJSON($SCRIPT_ROOT + '/_JSONSensorRead/' + {{dObject|tojson|safe}}, {}, function(data)) {
            $("#value").text(data.result.{{dObject|safe}}.value) 
            }
        }
    }, 1000);
});
