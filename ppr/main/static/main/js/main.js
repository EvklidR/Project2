function showSpis() {
    let block = $(".msubcatalog")
        if(block.css('display') === 'none'){
            block.slideDown();
        } else {
            block.slideUp();
        }
}


$(document).ready(function() {
    let slideNow = 1;
    let translateWidth = 0;
    const slideCount = $('.slidewrapper').children().length;

    $('.slidewrapper').css('width', 100 * slideCount + "%");

    $('.slide').css('width', 100 / slideCount + "%");

    if (slideCount > 1){
         $('#prev-btn').css('display', 'block')
         $('#next-btn').css('display', 'block')
    }

    $('#next-btn').click(function() {
        if (slideNow === slideCount || slideNow <= 0 || slideNow > slideCount) {
        $('.slidewrapper').css('transform', 'translate(0, 0)');
        slideNow = 1;
        } else {
            translateWidth = -$('#viewport').width() * (slideNow);
            $('.slidewrapper').css({
                'transform': 'translate(' + translateWidth + 'px, 0)',
            });
            slideNow++;
        }
    });

    $('#prev-btn').click(function() {
        if (slideNow === 1 || slideNow <= 0 || slideNow > slideCount) {
        translateWidth = -$('#viewport').width() * (slideCount - 1);
        $('.slidewrapper').css({
            'transform': 'translate(' + translateWidth + 'px, 0)',
        });
        slideNow = slideCount;
        } else {
            translateWidth = -$('#viewport').width() * (slideNow - 2);
            $('.slidewrapper').css({
                'transform': 'translate(' + translateWidth + 'px, 0)',
            });
            slideNow--;
        }
    });

    const img_show = document.getElementById('img_choosing')
    const img_ch = document.getElementById('id_image')
    if(img_ch){
        img_ch.addEventListener('change', ()=>{
            const img_data = img_ch.files[0]
            const url = URL.createObjectURL(img_data)
            img_show.innerHTML = `<img src='${url}' width='300px'>`
        })
    }

    const forms = document.getElementsByClassName('addForm')
    const Dforms = document.getElementsByClassName('DForm')

    const url = ""
    const csrf = document.getElementsByName('csrfmiddlewaretoken')
//    const fsort = document.getElementsByClassName('form-sort')
//
//    if (fsort){
//        fsort[0].addEventListener('change', e => filtSort(e, url, csrf, fsort[0]))
//    }

    if (forms) {
        Array.from(forms).forEach((form) => {
            form.addEventListener('submit', e => forAdd(e, form, csrf, url))
        });
    }

    if (Dforms) {
        Array.from(Dforms).forEach((form) => {
            form.addEventListener('submit', e => forDel(e, form, csrf, url))
        });
    }
});

//function filtSort(e, url, csrf, fsort){
//    e.preventDefault()
//    const fo = new FormData()
//    fo.append('csrfmiddlewaretoken', csrf[0].value)
//    fo.append('SortData', fsort.children[1].children[0].value)
//    fo.append('min', fsort.children[1].children[1].value)
//    fo.append('max', fsort.children[1].children[2].value)
//    fo.append('searchT', fsort.children[2].value)
//    $.ajax({
//        type: 'POST',
//        url: url,
//        data: fo,
//        success: function (response){
//            console.log("ccccc")
//        },
//        error: function (error){
//            console.log(error)
//        },
//        cache: false,
//        contentType: false,
//        processData: false,
//    })
//}

function forDel(e, form, csrf, url){

                e.preventDefault()
                const url2 = form.children[1].value + '/del_tovar'
                temp = form.closest('.basket_check')

                const fo = new FormData()
                fo.append('csrfmiddlewaretoken', csrf[0].value)
                fo.append('Delbasket', form.children[1].value)
                $.ajax({
                    type: 'POST',
                    url: url2,
                    data: fo,
                    success: function (response){
                        console.log("ddddd")
                        if (temp.children[0].children[2].innerHTML == '<i class="bi bi-bookmark-check-fill"></i>'){
                            temp.innerHTML = "<form class=\"addForm\">\n" +
                            `                <input type='hidden' name='csrfmiddlewaretoken' value='${csrf[0].value}'>` +
                            `                <input name=\"basket\" type=\"hidden\" value='${form.children[1].value}'>\n` +
                            "                <button class=\"btn btn-warning addT\" type=\"submit\"><i class=\"bi bi-basket\"></i></button>\n" +
                            "             </form>"
                        } else {
                            temp.innerHTML = "<form class=\"addForm\">\n" +
                            `                <input type='hidden' name='csrfmiddlewaretoken' value='${csrf[0].value}'>` +
                            `                <input name=\"basket\" type=\"hidden\" value='${form.children[1].value}'>\n` +
                            "                <button class=\"btn btn-warning addT\" type=\"submit\"><i class=\"fas fa-plus-circle\"></i>Добавить в корзину</button>\n" +
                            "             </form>"
                        }
                        temp.children[0].addEventListener('submit', ev => forAdd(ev, temp.children[0], csrf, url))
                    },
                    error: function (error){
                        console.log(error)
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                })
}

function forAdd(e, form, csrf, url){
                e.preventDefault()
                temp = form.closest('.basket_check')
//                console.log(temp)
                const fo = new FormData()
                fo.append('csrfmiddlewaretoken', csrf[0].value)
                fo.append('basket', form.children[1].value)

                $.ajax({
                    type: 'POST',
                    url: url,
                    data: fo,
                    success: function (response){
                        console.log("wwww")
                        if (temp.children[0].children[2].innerHTML == '<i class="bi bi-basket"></i>'){
                            temp.innerHTML = "<form class=\"DForm\">\n" +
                            `                <input type='hidden' name='csrfmiddlewaretoken' value='${csrf[0].value}'>` +
                            `                <input name=\"DelBasket\" type=\"hidden\" value='${form.children[1].value}'>\n` +
                            "                <button class=\"btn btn-warning\" type=\"submit\"><i class=\"bi bi-bookmark-check-fill\"></i></button>\n" +
                            "                </form>"
                        } else {
                            temp.innerHTML = "<form class=\"DForm\">\n" +
                            `                <input type='hidden' name='csrfmiddlewaretoken' value='${csrf[0].value}'>` +
                            `                <input name=\"DelBasket\" type=\"hidden\" value='${form.children[1].value}'>\n` +
                            "                <button class=\"btn btn-warning\" type=\"submit\"><i class=\"bi bi-bookmark-check-fill\"></i>Товар в корзине</button>\n" +
                            "                </form>"
                        }
                        temp.children[0].addEventListener('submit', ev => forDel(ev, temp.children[0], csrf))
                    },
                    error: function (error){
                        console.log(error)
                    },
                    cache: false,
                    contentType: false,
                    processData: false,
                })
}