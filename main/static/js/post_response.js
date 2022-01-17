
$(document).ready(function (){
    let followAuthor = $('#follow-author');
    let subscribeAuthor = $('#subscribe-author');
    let starPost = $('#star');
    let savePost = $('#save');
    let windowLocationHref = window.location.href;
    let post_id = $('#postContainer').attr('postId');
    let dataForResponse = {'post_id': post_id}, authorUsername = $('#author').attr('value');

    if(followAuthor.attr('value') === 'followed'){
        followAuthor.removeClass('btn-success');
        followAuthor.addClass('btn-outline-success');
        followAuthor.text('Following');
    }

    if(subscribeAuthor.attr('value') === 'subscribed'){
        subscribeAuthor.removeClass('btn-success');
        subscribeAuthor.addClass('btn-outline-success');
        $(this).children('i').removeClass('bi-envelope-plus')
        $(this).children('i').addClass('bi-envelope-check')
    }

    if(starPost.attr('value') === 'starred'){
        starPost.removeClass('bi-star');
        starPost.addClass('bi-star-fill');
    }

    if(savePost.attr('value') === 'saved'){
        savePost.removeClass('bi-save');
        savePost.addClass('bi-save-fill');
    }

//follow and unfollow author frontEnd section
    $(document).on('click', '#follow-author',function(event){
        event.preventDefault();

        let endpoint = '/' + authorUsername + '/author-view/follow-author'
        $.ajax({
            type: 'POST',
            url: endpoint,
            data: dataForResponse,
            action: 'post',
            dataType: 'json',

            success: function(json) {
                let authorFollowers = document.getElementById('author-followers')
                authorFollowers.innerHTML = json['author_followers'] + ' Followers'

            },
            error: function(xhr, errmsg, err) {
                console.log('error')
                console.log(xhr)
                console.log(errmsg)
                console.log(err)
            }

        });

        if($(this).hasClass('btn-success')){
            $(this).removeClass('btn-success');
            $(this).addClass('btn-outline-success');
            $(this).text('Following');
        }
        else{
            $(this).removeClass('btn-outline-success');
            $(this).addClass('btn-success');
            $(this).text('Follow');

        }

    });

//subscribe and unsubscribe author posts mail later frontEnd section
    $(document).on('click', '#subscribe-author',function(event){
        event.preventDefault();

        let endpoint = '/' + authorUsername + '/author-view/subscribe-author'
        $.ajax({
            type: 'POST',
            url: endpoint,
            data: dataForResponse,
            action: 'post',
            dataType: 'json',

            success: function(json) {
                console.log(json)

            },
            error: function(xhr, errmsg, err) {
                console.log('error')
                console.log(xhr)
                console.log(errmsg)
                console.log(err)
            }

        });

        if($(this).hasClass('btn-success')){
            $(this).removeClass('btn-success');
            $(this).addClass('btn-outline-success');
            $(this).children('i').removeClass('bi-envelope-plus')
            $(this).children('i').addClass('bi-envelope-check')
            alert('You Will Be Notified Whenever Author Posts')
        }
        else{
            $(this).removeClass('btn-outline-success');
            $(this).addClass('btn-success');
            $(this).children('i').removeClass('bi-envelope-check')
            $(this).children('i').addClass('bi-envelope-plus')
        }

    });

//star and unstar post frontEnd section

    $(document).on('click', '#star',function(event){
        event.preventDefault();

        let endpoint = windowLocationHref + '/star-post'
        $.ajax({
            type: 'POST',
            url: endpoint,
            data: dataForResponse,
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

        if($(this).hasClass('bi-star')){
            $(this).removeClass('bi-star');
            $(this).addClass('bi-star-fill');
        }
        else{
            $(this).removeClass('bi-star-fill');
            $(this).addClass('bi-star')
        }

    });

//save and unsaved post frontEnd section

    $(document).on('click', '#save',function(event){
        event.preventDefault();
        let endpoint = windowLocationHref + '/save-post'
        $.ajax({
            type: 'POST',
            url: endpoint,
            data: dataForResponse,
            action: 'post',
            dataType: 'json',

            success: function(json) {
                let total_saves = document.getElementById('post-response-save')
                total_saves.innerHTML = json['total_saves']

            },
            error: function(xhr, errmsg, err) {
                console.log('error')
                console.log(xhr)
                console.log(errmsg)
                console.log(err)
            }

        });

        if($(this).hasClass('bi-save')){
            $(this).removeClass('bi-save');
            $(this).addClass('bi-save-fill');
        }
        else{
            $(this).removeClass('bi-save-fill');
            $(this).addClass('bi-save')
        }

    });


});