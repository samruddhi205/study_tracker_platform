document.addEventListener('DOMContentLoaded', () => {
    // Theme toggle functionality
    const themeBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const htmlEl = document.documentElement;
    
    // Check saved theme or system preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    const setTheme = (isDark) => {
        if (isDark) {
            htmlEl.setAttribute('data-theme', 'dark');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            localStorage.setItem('theme', 'dark');
        } else {
            htmlEl.removeAttribute('data-theme');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            localStorage.setItem('theme', 'light');
        }
        
        // Dispatch custom event for charts to update
        window.dispatchEvent(new Event('themeChanged'));
    };
    
    // Initialize theme
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        setTheme(true);
    } else {
        setTheme(false);
    }
    
    // Toggle theme on click
    if(themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = htmlEl.hasAttribute('data-theme');
            setTheme(!isDark);
        });
    }
});
