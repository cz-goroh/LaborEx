$(document).ready(function () {

    $(".header__burger").on("click", function () {
        let item = $(this).closest(".header__inner");
        if (item.hasClass("active")) {
            item.removeClass("active");
        } else {
            item.addClass("active");
        }
    });

});