document.addEventListener('DOMContentLoaded', function() {
    const shortenForm = document.getElementById('shortenForm');
    const shortLinkElement = document.getElementById('shortLink');

    shortenForm.addEventListener('submit', function(event) {
        const originalUrl = document.getElementById('originalUrl').value;
        event.preventDefault();
        if (shortenForm.checkValidity()
            && removeTrailingSlash(originalUrl) !== removeTrailingSlash(shortLinkElement.textContent)) {
            shortenLink();
        } else {
            console.log('links are sames')
        }
        shortenForm.classList.add('was-validated');
    });
});


async function shortenLink() {
    const originalUrl = document.getElementById('originalUrl').value;
    try {
        const response = await fetch('/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({original_url: originalUrl})
        });

        if (response.ok) {
            const data = await response.json();
            displayShortenedLink(data.endpoint);
        } else {
            console.error('Error');
        }
    } catch (error) {
        console.error('Ошибка:', error);
    }
}


function displayShortenedLink(shortLink) {
    const shortenedLink = document.getElementById('shortenedLink');
    const shortLinkElement = document.getElementById('shortLink');
    shortLinkElement.href = shortLink;
    shortLinkElement.textContent = shortLink;

    shortenedLink.classList.remove('d-none');
}


function removeTrailingSlash(url) {
    return url.replace(/\/$/, "");
}