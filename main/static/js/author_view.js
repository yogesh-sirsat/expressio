$(document).ready(function (){
    //redirect to post view when click on post title | thumbnail
    $("#author-posts-feed .post-title, #author-posts-feed .post-thumbnail").click(function() {
        window.location = $(this).parent().find(".post_link").attr("href");
        return false;
    });
})