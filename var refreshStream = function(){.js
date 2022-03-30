var refreshStream = function(){
    $.ajax({
        url: '/url_to_view/',
        method: 'GET',
        data: {},
        success: function(data){
            $('#stream-list').replaceWith($('#stream-list',data));
        },
        error: function(error){
            console.log(error);
            console.log("error");
        }
    });
}

var total_seconds = 5; // refresh every 5 seconds

setInterval(function(){
    refreshStream();
},total_second * 1000);

