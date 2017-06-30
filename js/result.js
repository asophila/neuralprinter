$("#form-file").submit(function (event) {
    event.preventDefault();

});

$(window).bind('beforeunload', function () {

    //save info somewhere

    window.location.href = "/result.html";

});
