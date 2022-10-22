function like(postId) {
    const likeCount = document.getElementById(`like-count-${postId}`);
    const likeButton = document.getElementById(`like-button-${postId}`);


    fetch(`/${postId}/like`, { method: "POST" })
    .then((res) => res.json())
    .then((data) => {
        likeCount.innerHTML = data["likes"];
        if (data["liked"] === true) {
        likeButton.innerHTML =  "&#128078;"
        } else {
        likeButton.innerHTML = "&#128077;"
        }
    })
    .catch((e) => alert("Could not like post."));
}


function getLikers(postId) {

    const likersModal = document.getElementById(`modal-${postId}`);

    fetch(`/${postId}/likers`, { method: "GET" })
    .then((res) => res.json())
    .then((data) => {
        if (data['likers_count'] > 0) {
            likersModal.style.display = "block";
        }  
        else {
            alert("Nobody likes this yet...");
        }
    })
    .catch((e) => alert("Could not display who likes the post."));
}


function hideModal(postId) {
    const likersModal = document.getElementById(`modal-${postId}`);
    likersModal.style.display = "none";
}