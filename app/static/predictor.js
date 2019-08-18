$(function () {
    $("#submit-prediction").click(function () {
        var phrase = $("#phrase-input").val();
        $.ajax({
            url: "/api/predict/" + phrase
        })
            .then(JSON.parse)
            .done(function (data) {
                let people = Object.keys(data)
                    .sort(function(a,b){return data[b]-data[a]})
                    .map(name => ({
                        name: name,
                        percent: (data[name] * 100).toFixed(2)
                    }));

                $("#prediction-result").empty();
                $("#prediction-template").tmpl(people[0]).appendTo('#prediction-result');

                $("#prediction-results").empty();
                $("#percent-template").tmpl(people).appendTo('#prediction-results');
            });
    });
});