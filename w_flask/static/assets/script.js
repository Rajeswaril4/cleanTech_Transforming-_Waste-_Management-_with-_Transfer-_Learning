document.addEventListener('DOMContentLoaded', () => {

    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('header nav a');

    // Function to change active link
    const changeLinkState = () => {
        let index = sections.length;

        while(--index && window.scrollY + 100 < sections[index].offsetTop) {}
        
        navLinks.forEach((link) => link.classList.remove('active'));
        
        // Check if a corresponding nav link exists before adding the class
        if (navLinks[index]) {
            navLinks[index].classList.add('active');
        }
    };

    // Initial call to set the active link on page load
    changeLinkState();

    // Add scroll event listener
    window.addEventListener('scroll', changeLinkState);

});