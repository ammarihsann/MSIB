// static/script.js

const socket = io.connect('http://127.0.0.1:5001');

socket.on('update_data', function(data) {
    document.getElementById('temperature').textContent = `Temperature: ${data.temperature} °C`;
    document.getElementById('humidity').textContent = `Humidity: ${data.humidity} %`;
    document.getElementById('timestamp').textContent = `Timestamp: ${data.timestamp}`;
});

function toggleTheme() {
    const isDarkMode = document.getElementById('toggle-theme').checked;

    document.body.classList.toggle('dark-mode', isDarkMode);
    document.querySelector('.container').classList.toggle('dark-mode', isDarkMode);
    document.querySelector('h1').classList.toggle('dark-mode', isDarkMode);
    document.querySelectorAll('.data').forEach(el => el.classList.toggle('dark-mode', isDarkMode));
}
