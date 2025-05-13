document.addEventListener('DOMContentLoaded', function () {
    const tabLinks = document.querySelectorAll('.tab-link');

    tabLinks.forEach(link => {
        link.addEventListener('click', function () {
            const href = this.getAttribute('data-href');
            window.location.href = href;
        });
    });
});