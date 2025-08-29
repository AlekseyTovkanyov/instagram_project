function getCookie(cookieName) {
    let result = null;
    if (document.cookie && document.cookie !== '') {
        const allCookies = document.cookie.split(';');
        for (let i = 0; i < allCookies.length; i++) {
            const singleCookie = allCookies[i].trim();
            if (singleCookie.substring(0, cookieName.length + 1) === (cookieName + '=')) {
                result = decodeURIComponent(singleCookie.substring(cookieName.length + 1));
                break;
            }
        }
    }
    return result;
}
async function sendRequest(requestUrl, httpMethod = "POST", requestBody) {
    let authToken = await getCookie('token');
    let requestHeaders = {};
    requestHeaders['Authorization'] = `Token ${authToken}`;
    requestHeaders['Content-Type'] = 'application/json';

    const httpResponse = await fetch(requestUrl, {
        "method": httpMethod,
        "headers": requestHeaders,
        "body": JSON.stringify(requestBody)
    });

    if (httpResponse.ok) {
        return await httpResponse.json();
    } else {
        let requestError = new Error(httpResponse.text());
        console.log(requestError);
        throw requestError;
    }
}

async function handleLikeClick(clickEvent) {
    clickEvent.preventDefault();

    let clickedButton = clickEvent.currentTarget;
    let targetPostId = clickedButton.dataset.postId;
    let currentAction = clickedButton.dataset.action;
    let requestUrl = `/api/v1/posts/${targetPostId}/${currentAction}/`;

    try {
        let responseData = await sendRequest(requestUrl);

        if (currentAction === 'like') {
            clickedButton.classList.remove('btn-primary');
            clickedButton.classList.add('btn-danger');
            clickedButton.querySelector('i').classList.remove('bi-heart');
            clickedButton.querySelector('i').classList.add('bi-heart-fill');
            clickedButton.dataset.action = 'unlike';
        } else if (currentAction === 'unlike') {
            clickedButton.classList.remove('btn-danger');
            clickedButton.classList.add('btn-primary');
            clickedButton.querySelector('i').classList.remove('bi-heart-fill');
            clickedButton.querySelector('i').classList.add('bi-heart');
            clickedButton.dataset.action = 'like';
        }

        let countElement = document.getElementById(`likes-count-${targetPostId}`);
        if (countElement) {
            countElement.innerText = `${responseData.likes_count} likes`;
        }
    } catch (requestError) {
        console.error('Error handling like button click:', requestError);
    }
}
function initializePage() {
    let allLikeButtons = document.querySelectorAll('[data-js="like-button"]');
    for (let likeButton of allLikeButtons) {
        likeButton.addEventListener('click', handleLikeClick);
    }
}
window.addEventListener('load', initializePage);