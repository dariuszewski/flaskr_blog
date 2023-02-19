const fileInput = document.querySelector('#photo');
const removePhotoInput = document.querySelector('#remove_photo');
const photoLabel = document.querySelector('#photo_label');
removePhotoInput.addEventListener('click', () => {
    console.log('click click')
    if (removePhotoInput.checked) {
        fileInput.style.display = "none";
        fileInput.value = null;
        photoLabel.style.display = "none";
    }
    else {
        fileInput.style.display = "block";
    }
})