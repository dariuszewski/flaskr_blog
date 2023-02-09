let searchButton = document.querySelector('#search-btn');
let keywordValue = document.querySelector('#keyword').value;

searchButton.addEventListener('click', (keywordValue) => {
        window.location.replace("/index?keyword=" + keywordValue);
})


let alltags = document.querySelectorAll('.tag-pill-sm');

alltags.forEach((tag) => {
    tag.addEventListener('click', () => {
        if (tag.classList.contains('selected')) {
            tag.classList.remove("selected");
            tag.classList.add("not-selected");
            window.location.replace("/index");
        }
        else {
            tag.classList.remove("not-selected");
            tag.classList.add("selected");
            window.location.replace("/index?tag=" + tag.textContent);
        }; 
    })
})

function activateTags(tagValue) {
    let allTags = document.querySelectorAll('.tag-pill-sm');
    for (let tag of allTags) {
        if (tag.textContent == tagValue) {
            tag.classList.remove("not-selected");
            tag.classList.add("selected");
        }
    }
}


checkParams()

function highlight(keyword){
    Array.from(document.querySelectorAll("article, article *:not(script):not(style):not(noscript)"))
      .flatMap(({childNodes}) => [...childNodes])
      .filter(({nodeType, textContent}) => nodeType === document.TEXT_NODE && textContent.includes(keyword))
      .forEach((textNode) => textNode.replaceWith(...textNode.textContent.split(keyword).flatMap((part) => [
          document.createTextNode(part),
          Object.assign(document.createElement("mark"), {
            textContent: keyword
          })
        ])
        .slice(0, -1)));
}


function checkParams() {
    let url = window.location.href;
    let params = url.split('?')
    if (params.length > 1) {
        return evaluateParams(params[1])
    }
}


function evaluateParams(paramsList) {
    let params = paramsList.split('&');
    let paramsObject = {};
    for (let param of params) {
        if (param.includes('=')) {
            let entry = param.split('=');
            paramsObject[entry[0]] = entry[1].replaceAll('%20', ' ')
        };
    };
    if ('keyword' in paramsObject) {
        window.addEventListener('load', function () {
            highlight(paramsObject.keyword)
          })
    };
    if ('tag' in paramsObject) {
        window.addEventListener('load', function () {
            activateTags(paramsObject.tag)
        })
    };
} 