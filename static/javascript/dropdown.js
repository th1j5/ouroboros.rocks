var span = document.querySelector('span#about_chevron');
var menu = document.querySelector('ul.sub-menu');
    span.addEventListener('click', function (event) {
        if (menu.classList.contains('dn')) {
            menu.classList.remove('dn');
        } else {
            menu.classList.add('dn');
        }
    }
);
