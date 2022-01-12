$(document).ready(function (){
    $(".post").click(function() {
      window.location = $(this).find("a").attr("href");
      return false;
    });
})