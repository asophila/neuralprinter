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
    var code = getUrlParameter('code');
    if(code){
        $('#code').val(code);
        Materialize.updateTextFields();
    }

    $('select').material_select();

    // for HTML5 "required" attribute
    $("select[required]").css({ display: "block", height: 0, padding: 0, margin: "0 60px", width: 0, position: "relative", top: "-18px" });
    $(".file-field > .btn input[type=file]").css({ bottom: "18px" });
});

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};