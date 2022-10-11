
$(document).ready(function () {

    $('#confirmPassword').on('input', function () {
        let setPassword = $('#setPassword').val(),
            confirmPassword = $(this).val();
        if(setPassword === confirmPassword){
            $(this).removeClass('is-invalid');
            $(this).addClass('is-valid');
        }
        else{
            $(this).removeClass('is-valid');
            $(this).addClass('is-invalid');
        }

        if(!setPassword){
            $(this).removeClass('is-valid');
            $(this).removeClass('is-invalid');
        }
    });

    $('#setPassword').on('input', function () {
        let confirmPassword = $('#confirmPassword'),
            setPassword = $(this).val();
        if(setPassword === confirmPassword.val()){
            confirmPassword.removeClass('is-invalid');
            confirmPassword.addClass('is-valid');
        }
        else{
            confirmPassword.removeClass('is-valid');
            confirmPassword.addClass('is-invalid');
        }

        if(!setPassword){
            confirmPassword.removeClass('is-valid');
            confirmPassword.removeClass('is-invalid');
        }
    });

//redirect to author view when click on username | user avatar
    $(".user-name").click(function() {
        window.location = $(this).attr("href");
        return false;
    });
    $(".user-avatar").click(function() {
        window.location = $(this).attr("href");
        return false;
    });

    $("#author .author-name").click(function() {
        window.location = $(this).attr("href");
        return false;
    });
    $("#author .author-avatar").click(function() {
        window.location = $(this).attr("href");
        return false;
    });
});