// global variables
let following = [];
let followers = [];

//html parsing 
function cleanup(html) {
    const parser = new DOMParser();
    const doc = parser.parseFromString(html, 'text/html');
    const links = Array.from(doc.querySelectorAll('a'));
    console.log(links);
    return links.map(link => link.textContent);
}

function processFormData() {
	event.preventDefault();
    const followingHtml = document.getElementById('followingInput').value;
    const followersHtml = document.getElementById('followersInput').value;
    following = cleanup(followingHtml);
    followers = cleanup(followersHtml);
    const resultParagraph = document.getElementById('resultParagraph');
    resultParagraph.innerHTML = '';

    for (let person of following) {
        if (!followers.includes(person)) {
            resultParagraph.innerHTML += `${person}<br>`;
        }
    }
}

/*
// Function to find unfollowers
function findUnfollowers() {
    const notFollowingBack = following.filter(username => !followers.includes(username));
    const notFollowedBy = followers.filter(username => !following.includes(username));
}
*/