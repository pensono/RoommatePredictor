$(function () {
    $("#submit-prediction").click(function () {
        var phrase = $("#phrase-input").val();
        $.ajax({
            url: "/api/predict/" + phrase
        })
            .then(JSON.parse)
            .done(function (data) {
                var highest = Object.keys(data).reduce((a, b) => data[a] > data[b] ? a : b);
                $("#prediction-image").attr("src", `/static/people/${highest}.jpg`);
                $("#prediction-image-wrapper").removeClass("hidden")
            });
    });
});