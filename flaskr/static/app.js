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
    const modalContent = document.getElementById(`modal-content-${postId}`);

    fetch(`/${postId}/likers`, { method: "GET" })
    .then((res) => res.json())
    .then((data) => {
        if (data['likers_count'] > 0) {
            var outputString = '<ul>';
            for (liker of data['likers']) {
                outputString = outputString + '<li>' + liker + '</li>'
            };
            outputString += '</ul>';
            likersModal.style.display = "block";
            modalContent.innerHTML = outputString;
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

function openCommentForm(commentFormId) {
    const commentForm = document.getElementById(`comment-form-${commentFormId}`);
    commentForm.style.display = "block";
    const commentEditForm = document.getElementById(`comment-edit-form-${commentFormId}`);
    commentEditForm.style.display = "none";
}

function hideCommentForm(commentFormId) {
    const commentForm = document.getElementById(`comment-form-${commentFormId}`);
    commentForm.style.display = "none";
}

function openCommentEditForm(commentFormId) {
    const commentEditForm = document.getElementById(`comment-edit-form-${commentFormId}`);
    commentEditForm.style.display = "block";
    const commentForm = document.getElementById(`comment-form-${commentFormId}`);
    commentForm.style.display = "none";
}

function hideCommentEditForm(commentFormId) {
    const commentEditForm = document.getElementById(`comment-edit-form-${commentFormId}`);
    commentEditForm.style.display = "none";
}