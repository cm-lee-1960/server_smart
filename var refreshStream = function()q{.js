var refreshStream = function(){
  var getNewDataUrl = '/streams/'
    $.ajax({
        url: getNewDataUrl,
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
},total_seconds * 1000);