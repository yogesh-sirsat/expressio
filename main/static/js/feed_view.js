$(document).ready(function () {

    //redirect to post view when click on post title | thumbnail
    $(".post_item .card-img-top, .post_item .card-title").click(function() {
        window.location = $(this).parent().find(".post_link").attr("href");
        return false;
    });
});