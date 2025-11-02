document.addEventListener('DOMContentLoaded', () => {
    // THEME - Read persisted theme and apply
    const preferred = localStorage.getItem('theme');
    const root = document.documentElement;
    const themeToggle = document.getElementById('theme-toggle');

    const applyTheme = (theme) => {
        if (theme === 'dark') {
            root.setAttribute('data-theme', 'dark');
            if (themeToggle) themeToggle.textContent = '☀️';
        } else {
            root.setAttribute('data-theme', 'light');
            if (themeToggle) themeToggle.textContent = '🌙';
        }
    };

    // If user has a saved preference, use it. Else detect system preference.
    if (preferred) {
        applyTheme(preferred);
    } else {
        const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
        applyTheme(prefersDark ? 'dark' : 'light');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const current = root.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            applyTheme(next);
            localStorage.setItem('theme', next);
        });
    }

    // NAV ACTIVE LINK FOR IN-PAGE SECTIONS ONLY
    // Only consider nav links that are anchors (href starts with '#')
    const navLinksAll = Array.from(document.querySelectorAll('header nav a'));
    const navLinks = navLinksAll.filter(a => {
        const href = a.getAttribute('href') || '';
        return href.startsWith('#');
    });

    const sections = document.querySelectorAll('section[id]');

    const changeLinkState = () => {
        if (sections.length === 0 || navLinks.length === 0) return;
        let index = sections.length;
        while (--index && window.scrollY + 120 < sections[index].offsetTop) {}
        navLinks.forEach((link) => link.classList.remove('active'));
        if (navLinks[index]) {
            navLinks[index].classList.add('active');
        }
    };

    // Run once on load and on scroll (for pages with in-page anchors)
    changeLinkState();
    window.addEventListener('scroll', changeLinkState);
});
