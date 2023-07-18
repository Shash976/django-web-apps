document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll(".post").forEach(post => {
        post.querySelector("#unlike").addEventListener('click', () => like(post, 'unlike'));
        post.querySelector("#like").addEventListener('click', () => like(post, 'like'));
    });
});

function like(post, condition) {
    const post_id = post.querySelector("#post_id").innerHTML;
    var post_likes = parseInt(post.querySelector("#likes").innerHTML);
    if (condition == "like") {
        post_likes++
    } else if (condition == "unlike") {
        post_likes--
    }    
    fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            likes: post_likes
        })
    })
    fetch(`/posts/${post_id}`)
    .then(response => response.json())
    .then(data => {
        post.querySelector("#likes").innerHTML = data.likes;
    })
}