
$(document).ready(function (){
    let followAuthor = $('#follow-author');
    let subscribeAuthor = $('#subscribe-author');
    let starPost = $('.star-post');
    let savePost = $('.save-post');
    const current_post_url = $("#postContainer").attr("data-full-path");
    let authorUsername = $('#author').attr('value');

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

//changing class of star icon as current user starred or not to posts    
    $('.star-post').each(function(){
        let endpoint = $(this).attr('href'), thisElement= $(this);
        let post_id = thisElement.parent().parent().attr('postId');

        $.ajax({
            type: 'POST',
            url: endpoint,
            data: {'post_id': post_id, 'response': 'none'},
            action: 'post',
            dataType: 'json',

            success: function(json) {
                if(json['star_post_status'] === 'starred'){
                    if(thisElement.hasClass('bi-star')){
                        thisElement.removeClass('bi-star');
                        thisElement.addClass('bi-star-fill');
                    }
                }

            },
            error: function(xhr, errmsg, err) {
                console.log('error')
                console.log(xhr)
                console.log(errmsg)
                console.log(err)
            }

        });

    });

//changing class of save icon as current user saved or not to posts    
    $('.save-post').each(function(){
        let endpoint = $(this).attr('href'), thisElement= $(this);
        let post_id = thisElement.parent().parent().attr('postId');

        $.ajax({
            type: 'POST',
            url: endpoint,
            data: {'post_id': post_id, 'response': 'none'},
            action: 'post',
            dataType: 'json',

            success: function(json) {
                if(json['save_post_status'] === 'saved'){
                    if(thisElement.hasClass('bi-save')){
                        thisElement.removeClass('bi-save');
                        thisElement.addClass('bi-save-fill');
                    }
                }

            },
            error: function(xhr, errmsg, err) {
                console.log('error')
                console.log(xhr)
                console.log(errmsg)
                console.log(err)
            }

        });

    });

//redirect to author view when click on author name | author avatar
    $("#author-name").click(function() {
        window.location = $(this).attr("href");
        return false;
    });
    $("#author-avatar").click(function() {
        window.location = $(this).attr("href");
        return false;
    });
//follow and unfollow author frontEnd section
    $(document).on('click', '#follow-author',function(event){
        event.preventDefault();

        let endpoint = '/' + authorUsername + '/author-view/follow-author'
        $.ajax({
            type: 'POST',
            url: endpoint,
            data: {
                'author_username': authorUsername,
            },
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
            data: {
                'author_username': authorUsername,
            },
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

    $(document).on('click', '.star-post',function(event){
        event.preventDefault();

        let post_id = $(this).parent().parent().attr('postId');
        let endpoint = $(this).attr('href'), thisElement= $(this);

        $.ajax({
            type: 'POST',
            url: endpoint,
            data: {'post_id': post_id, 'response': 'clicked',},
            action: 'post',
            dataType: 'json',

            success: function(json) {
                thisElement.next().text(json['total_stars']);
                console.log(json);

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

    $(document).on('click', '.save-post',function(event){
        event.preventDefault();
        let endpoint = $(this).attr('href'),thisElement= $(this);
        let post_id = thisElement.parent().parent().attr('postId')

        $.ajax({
            type: 'POST',
            url: endpoint,
            data: {'post_id': post_id, 'response': 'clicked'},
            action: 'post',
            dataType: 'json',

            success: function(json) {
                thisElement.next().text(json['total_saves']);

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

    $("#comment_box").focus(function () {
        $(this).attr("rows", "4");
    });

    $("#comments-section .reply_box").focus(function () { 
        $(this).attr("rows", "4");        
    });

    $("#comments-section .post_comment").on('click', function (event) {
        event.preventDefault();
        const comment_content = $("#comment_box").val();
        if (comment_content === "") {
            alert("Comment is blank!");
            return;
        }
        const post_id = $(this).attr("data-post-id");
        const comment_data = {
            content: comment_content,
            post_id
        };
        $.ajax({
            type: "POST",
            url: current_post_url+"/comment-post",
            data: comment_data,
            dataType: "json",
            success: function (response) {
                $("#comments-section .posted_comments").prepend(response["comment_item"]);
                $("#comment_box").val("");
            },
            error: function(error) {
                alert("Posting comment failed! : ", error);
            },
        });
    });

    $("#comments-section .comment_replies").on("click", function (event) {
        event.preventDefault();
        const parent_comment = ($(this).parent().attr("data-comment-id"));
        $("#replies-of-"+parent_comment).toggle();
    });

    $("#comments-section .reply_btn").on("click", function (event) {
        event.preventDefault();
        const parent_comment = ($(this).parent().parent().attr("data-comment-id"));
        $("#reply-form-of-"+parent_comment).toggle();
    });

    $("#comments-section .post_reply").on("click", function (event) {
        event.preventDefault();
        const parent_comment = $(this).attr("data-comment-id");
        const reply_input_elem = $("#reply-form-of-"+parent_comment+" .reply_box");
        const reply_content = reply_input_elem.val();
        if (reply_content === "") {
            alert("Reply is blank!");
            return;
        }
        const reply_data = {
            content: reply_content,
            parent_id: parent_comment,
        };
        console.log(reply_content, parent_comment);
        $.ajax({
            type: "POST",
            url: current_post_url+"/reply-comment",
            data: reply_data,
            dataType: "json",
            success: function (response) {
                $("#replies-of-"+parent_comment).show().prepend(response["reply_item"]);
                reply_input_elem.val("");
            },
            error: function(error) {
                alert("Posting reply failed! : ", error);
            },
        });

    });

});