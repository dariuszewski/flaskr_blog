let avaliableTags = document.querySelector('.available-tags');
let preselectedTags = document.querySelectorAll('.selected')

let selectedTagsArray = [];

let createTagButton = document.querySelector('.append-btn');
let customTagInput = document.getElementById('custom-tag');

let tagsHiddenInput = document.getElementById('tags');
 

// This is for edition of existing tag. 
for (let tag of preselectedTags) {
    selectedTagsArray.push(tag.textContent);
}
tagsHiddenInput.value = selectedTagsArray;


[...avaliableTags.children].forEach(tag =>
    tag.addEventListener('click', () => {
        tagToggle(tag);
    }))


createTagButton.addEventListener('click', () => {
    // always convert tag to lower case.
    let tagTextValue = customTagInput.value.toLowerCase();

    // validate if tag is not empty.
    if (tagTextValue.trim().length < 1) {
        alert("You can't add an empty tag.");
        return ;
    }
    else if(tagTextValue.length > 20) {
        alert('Your tag can be up to 20 characters long.');
        return ;
    }
    else if(tagTextValue.includes(',')) {
        alert('Your tag contains illegal character.');
        return ;
    }
    if (!getTagByText(tagTextValue)) {
        // if typed tag doesn't exist yet, create it and set it to selected.
        let newTag = document.createElement("span");
        newTag.classList.add(...["tag-pill", "not-selected"]);
        newTag.textContent = tagTextValue
        newTag.addEventListener('click', () => tagToggle(newTag))
        tagToggle(newTag);
        avaliableTags.appendChild(newTag);
    }
    else {
        // if typed tag already exists, change it's status.
        let foundTag = getTagByText(tagTextValue);
        tagToggle(foundTag);
    }
    // clear input.
    customTagInput.value = ''
})


function tagToggle(tag) {
    if (tag.classList.contains('not-selected')) {
        // user can add up to 5 tags.
        if (selectedTagsArray.length >= 5) {
            alert('You can select up to 5 tags.');
            return ;
        }
        else {
            tag.classList.remove("not-selected");
            tag.classList.add("selected");
            selectedTagsArray.push(tag.textContent);
            tagsHiddenInput.value = selectedTagsArray;
        }        
    }
    else {
        tag.classList.add("not-selected");
        tag.classList.remove("selected");
        // remove tag from selected values.
        let indexOfTagToBeRemoved= selectedTagsArray.indexOf(tag.textContent);
        selectedTagsArray.splice(indexOfTagToBeRemoved, 1)
        tagsHiddenInput.value = selectedTagsArray;
    };
};


function getTagByText(text) {
    return [...avaliableTags.children].filter(tag => tag.textContent == text)[0];
};

