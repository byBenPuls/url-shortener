document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal');
    const closeModalBtn = document.querySelector('.close');

    closeModalBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});


document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('modal');
    const modalText = document.getElementById('modalText')

    document.getElementById('url_form').addEventListener('submit', function(event) {
        event.preventDefault();

        const url = '/';
        const data = {
            original_url: document.getElementById('original_url').value
        };

        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Ошибка сети');
        })
        .then(data => {
            modal.style.display = 'block';
            console.log(data.endpoint);
            modalText.textContent = data.endpoint;
            console.log(data);
        })
        .catch(error => console.error('Ошибка:', error));
    });
});