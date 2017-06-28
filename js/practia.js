
$(document).ready(function () {
    $('select').material_select();

    // for HTML5 "required" attribute
    $("select[required]").css({ display: "block", height: 0, padding: 0, margin: "0 60px", width: 0, position: "relative", top: "-18px" });
    $(".file-field > .btn input[type=file]").css({ bottom: "18px" });
});
