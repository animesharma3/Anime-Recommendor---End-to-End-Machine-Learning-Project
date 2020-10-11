const animeData = document.querySelector('.anime-data')
const animeInput = document.getElementById('anime-input')
const searchBtn = document.getElementById('search')
const searchInput = document.querySelector('.input')
const form = document.querySelector('form')
const animeInfo = document.getElementById('info')
const rec_text = document.getElementsByClassName('recommended')[0]

searchInput.addEventListener('keyup', searchAnimeData)

async function searchAnimeData() {
    animeTitle = searchInput.value
    if (animeInfo) animeInfo.innerHTML = ''
    if (rec_text) rec_text.innerHTML = ''
    form.setAttribute('action', `/${animeTitle}`)
    let animes = await getAnimeData(`https://kitsu.io/api/edge/anime/?filter[text]=${animeTitle},limit=20`)
    animeData.innerHTML = ""
    let output = ''
    animes.forEach((anime) => {
        let animeTitle = anime['attributes']['titles']['en']
        if (!animeTitle) {
            animeTitle = anime['attributes']['titles']['en_jp']
        }
        let posterImage = anime['attributes']['posterImage']['original']
        output += `<div>
                    <img src=${posterImage} id='recommend'>
                    <br>
                    <button class='btn text-white form-control' id='submit' type='submit'>${animeTitle}</h3>
                </div>`
    })
    animeData.innerHTML = output
}

async function getAnimeData(url) {
    res = await fetch(url)
    jsonData = await res.json()
    return jsonData['data']
}

async function displayAnimeData() {
    let animes = await getAnimeData('https://kitsu.io/api/edge/anime?page%5Blimit%5D=20')
    let output = ''
    animes.forEach((anime) => {
        let animeTitle = anime['attributes']['titles']['en']
        if (!animeTitle) {
            animeTitle = anime['attributes']['titles']['en_jp']
        }
        let posterImage = anime['attributes']['posterImage']['original']
        output += `<div>
                    <img src=${posterImage} id='recommend'>
                    <br>
                    <button class='btn text-white form-control' id='submit' type='submit'>${animeTitle}</h3>
                </div>`
    })
    animeData.innerHTML = output
}

function addToInput() {
    bindEvent(document, 'click', (e) => {
        if (e.target) {
            if (e.target.id === 'submit') {
                e.preventDefault()
                let title = String(e.target.innerHTML)
                animeInput.value = title
                form.setAttribute('action', `/${title}`)
                searchBtn.click()
            } else if (e.target.id === 'recommend') {
                animeInput.value = e.target.parentElement.children[2].innerHTML
                form.setAttribute('action', `/${animeInput.value}`)
                searchBtn.click()
            }
        }
    })
}

let bindEvent = function(elem ,evt,cb) {
    if ( elem.addEventListener ) {
        elem.addEventListener(evt,cb,false);
    } else if ( elem.attachEvent ) {
        elem.attachEvent('on' + evt, function(){
            cb.call(e.srcElement,e);
        });
    }
}

if (animeData.innerHTML.trim() === '') {
    displayAnimeData()
}

addToInput()
