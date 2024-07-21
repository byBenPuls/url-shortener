document.addEventListener('DOMContentLoaded', function() {
    const shortenForm = document.getElementById('shortenForm');

    shortenForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Предотвращаем стандартное действие submit
        if (shortenForm.checkValidity()) {
            shortenLink();
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
            console.error('Ошибка при сокращении ссылки');
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