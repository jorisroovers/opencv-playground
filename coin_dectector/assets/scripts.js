var UTIL = {};
(function (parent) {
    var parent = parent || {};

    parent.postJSON = function (url, data, success) {
        data = JSON.stringify(data);
        $.ajax({type: "POST", url: url, data: data, contentType: "application/json", success: success});
    }

})(UTIL);

$(document).ready(function () {

    var overlay = $("#image-overlay");

    // set the initial value spans
    $("#param1-range-value").html($("#param1-range").val());
    $("#param2-range-value").html($("#param2-range").val());


    $("#param1-range,#param2-range").on("input change", function () {
        console.log($(this).val());
        var valElementSelector = "#" + $(this).attr('id') + "-value";
        $(valElementSelector).html($(this).val());
    });


    $("#detect").click(function (e) {
        overlay.show();
        data = {
            'param1': $("#param1-range").val(),
            'param2': $("#param2-range").val()
        }

        UTIL.postJSON('/detect', data, function (data) {
            overlay.hide();
            $("#coin-image").attr("src", data.url);
        });
        e.preventDefault();

    });


});