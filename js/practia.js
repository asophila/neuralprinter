$(window).bind('scroll', function () {
    if ($(window).scrollTop() > 70) {
        $('.progress-bar').addClass('fixed');
    } else {
        $('.progress-bar').removeClass('fixed');
    }
});

$("#form-file").submit(function (event) {
    $('.overlay').removeClass('hide');
    $('.progress').removeClass('hide');
    //event.preventDefault();
});

$(document).ready(function () {
    $('select').material_select();

    // for HTML5 "required" attribute
    $("select[required]").css({ display: "block", height: 0, padding: 0, margin: "0 60px", width: 0, position: "relative", top: "-18px" });
    $(".file-field > .btn input[type=file]").css({ bottom: "18px" });
});

