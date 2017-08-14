
function join_championship(player_id){
    request_url = "/referee/championship/join/"+ player_id +"/";
    $.ajax({
        url:request_url,
        type:"POST",
        data: {'csrfmiddlewaretoken': getCookie('csrftoken')},
        dataType:"json",
        success:function(status)
        {
            console.log(status);
        }
    })
}
