
$(document).ready(function (){

    $(document).on('click', '#star',function(event){
        event.preventDefault();
        let post_id = $(this).attr('value')
        let endpoint = window.location.href + '/post-stars'
        $.ajax({
            type: 'POST',
            url: endpoint,
            data: {
                'post_id': post_id,
            },
            action: 'post',
            dataType: 'json',

            success: function(json) {
                let total_stars = document.getElementById('post-response-star')
                total_stars.innerHTML = json['total_stars']

            },
            error: function(xhr, errmsg, err) {
                console.log('error')
                console.log(xhr)
                console.log(errmsg)
                console.log(err)
            }

        });

    });

    $(document).on('click', '#save',function(event){
        event.preventDefault();
        let post_id = $(this).attr('value')
        let endpoint = window.location.href + '/post-saves'
        $.ajax({
            type: 'POST',
            url: endpoint,
            data: {
                'post_id': post_id,
            },
            action: 'post',
            dataType: 'json',

            success: function(json) {
                let total_saves = document.getElementById('post-response-save')
                total_saves.innerHTML = json['total_saves']

                console.log(json)
            },
            error: function(xhr, errmsg, err) {
                console.log('error')
                console.log(xhr)
                console.log(errmsg)
                console.log(err)
            }

        });

    });
});