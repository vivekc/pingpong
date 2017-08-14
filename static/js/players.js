
function join_championship(event, player_id){
    /*
    * @param event: target button element
    * @param player_id: player id
    */

    request_url = "/referee/championship/join/"+ player_id +"/";
    $.ajax({
        url:request_url,
        type:"POST",
        data: {'csrfmiddlewaretoken': getCookie('csrftoken')},
        dataType:"json",
        success:function(response)
        {
            event.target.setAttribute("disabled", true);
            console.log(response);
        }
    })
}
