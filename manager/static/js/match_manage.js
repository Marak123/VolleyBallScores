window.addEventListener('load', function () {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    document.querySelectorAll('.one_point').forEach(function (e) {

        e.addEventListener('click', function (e) {
            let team_id = parseInt(e.target.getAttribute("data-team-id"))

            let data = {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                team_id: team_id,
                match_id: MATCH_ID,
                point: parseInt(document.querySelector(`input[data-team-id="${team_id}"]`).value) + 1
            };

            fetch(API_ADD_POINT, {
                method: 'POST',
                headers: new Headers({
                    'Content-Type': 'application/json',
                    "X-CSRFToken": getCookie('csrftoken')
                }),
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(json => console.log('Response', json))
            .catch(error => {
                console.error('Wystąpił błąd:', error);
            });
        })
    })

    document.querySelectorAll('.minus_one_point').forEach(function (e) {

        e.addEventListener('click', function (e) {
            let team_id = parseInt(e.target.getAttribute("data-team-id"))
            let point = parseInt(document.querySelector(`input[data-team-id="${team_id}"]`).value)

            let data = {
                csrfmiddlewaretoken: csrfmiddlewaretoken,
                team_id: team_id,
                match_id: MATCH_ID,
                point: (point > 0 ? point - 1 : point)
            };

            fetch(API_ADD_POINT, {
                method: 'POST',
                headers: new Headers({
                    'Content-Type': 'application/json',
                    "X-CSRFToken": getCookie('csrftoken')
                }),
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(json => console.log('Response', json))
            .catch(error => {
                console.error('Wystąpił błąd:', error);
            });
        })
    })

    document.querySelector('#submit-all-data').addEventListener('click', function (e) {
        let data = {
            csrfmiddlewaretoken: csrfmiddlewaretoken,
            match_id: MATCH_ID,
            team_one_score: parseInt(document.querySelector('#point_team_one').value),
            team_two_score: parseInt(document.querySelector('#point_team_two').value),
            finished: document.querySelector('#finist-match').checked
        };

        fetch(API_FINISH_DATA, {
            method: 'POST',
            headers: new Headers({
                'Content-Type': 'application/json',
                "X-CSRFToken": getCookie('csrftoken')
            }),
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(json => console.log('Response', json))
        .catch(error => {
            console.error('Wystąpił błąd:', error);
        });
    })

}, false);