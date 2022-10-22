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