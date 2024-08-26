// This function ensures that the pathname ends with a slash
function normalizePathname(pathname) {
    return pathname.endsWith('/') ? pathname : `${pathname}/`;
}
function isCurrentPage(href, windowLocation) {
    const fullUrl = new URL(href, windowLocation.origin);
    const normalizedHref = normalizePathname(fullUrl.pathname);
    const normalizedWindowLocation = normalizePathname(windowLocation.pathname);

    return normalizedHref === normalizedWindowLocation;
}
// Get all the nav links
const navLinks = document.querySelectorAll('.nav-link');
// Iterate over each nav link and update the 'active' class
navLinks.forEach(link => {
    // Remove the 'active' class initially
    link.classList.remove('active');
    // Check if the link's href attribute matches the current window location
    if (isCurrentPage(link.getAttribute('href'), window.location)) {
        // Add the 'active' class if it's the current page
        link.classList.add('active');
    }
});
