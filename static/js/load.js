const loadBtn = document.getElementById('btn');
const total = JSON.parse(document.getElementById('json-total').textContent);
const alert = document.getElementById('alert');

function loadmorePost() {
    var _current_item = $('.opinion').length
    console.log(_current_item)
    const content_container = document.getElementById("ratings-container");
    $.ajax({
            url: load_url,
        type: 'GET',
        data: {
                'loaded_items': _current_item
        },
        beforeSend: function () {
            loadBtn.classList.add('not-visible');
        },
        success: function (response) {
            const data = response.rate_objs
            data.map(rate => {
                var url = remove_url.replace('00000000-0000-0000-0000-000000000000', rate.author_id)
                var content = ""
                if (rate.author__name || rate.author__surname) {
                    content += '<div class="opinion"><h2>' + rate.author__name + ' ' + rate.author__surname + '</h2>'
                }
                else {
                content += '<div class="opinion"><h2>Gość</h2>'
                }
                content += '<div class ="stars">'
                content += '<a class="remove-button admin-action" href="' + url + '">Usuń</a></h2>'
                for (let x = 1; x < 5 + 1; x++) {
                    if (x < rate.rate + 1)
                        content += '<i class="fa fa-star yellow-star"></i> '
                    else
                        content += '<i class="fa fa-star gray-star"></i> '
                }
                content += '<span>(' + rate.rate + ')</span></div>'
                content += '<p>' + rate.description + '</p></div>'
                content_container.innerHTML += content
            });
            if (_current_item == total)
                {}
            else {
                loadBtn.classList.remove('not-visible');
            }
        },
        error: function (err) {
            console.log(err);
        },
    });
}
loadBtn.addEventListener('click', () => {
    loadmorePost()
});
