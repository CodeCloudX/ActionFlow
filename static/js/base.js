document.addEventListener('DOMContentLoaded', () => {
    setTimeout(() => {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(message => {
            message.style.display = 'none';
        });
    }, 2000); // 2 seconds
});