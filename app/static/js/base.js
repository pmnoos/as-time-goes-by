function updateThemeButtons(isDark) {
    const emoji = isDark ? "☀️" : "🌙";
    const desktopButton = document.getElementById("theme-btn");
    const mobileButton = document.getElementById("theme-btn-mobile");

    if (desktopButton) desktopButton.textContent = emoji;
    if (mobileButton) mobileButton.textContent = emoji;
}

function toggleTheme() {
    const isDark = document.documentElement.classList.toggle("dark");

    try {
        localStorage.setItem("theme", isDark ? "dark" : "light");
    } catch (error) {
        // The selected theme still applies for the current page.
    }

    updateThemeButtons(isDark);
}

const mobileMenu = document.getElementById("mobile-menu");
const navigationToggle = document.getElementById("nav-toggle");
const desktopThemeButton = document.getElementById("theme-btn");
const mobileThemeButton = document.getElementById("theme-btn-mobile");
const backToTop = document.getElementById("back-to-top");

if (navigationToggle && mobileMenu) {
    navigationToggle.addEventListener("click", function () {
        mobileMenu.classList.toggle("hidden");
    });

    mobileMenu.querySelectorAll("a").forEach(function (link) {
        link.addEventListener("click", function () {
            mobileMenu.classList.add("hidden");
        });
    });
}

if (desktopThemeButton) desktopThemeButton.addEventListener("click", toggleTheme);
if (mobileThemeButton) mobileThemeButton.addEventListener("click", toggleTheme);

updateThemeButtons(document.documentElement.classList.contains("dark"));

if (backToTop) {
    backToTop.addEventListener("click", function () {
        window.scrollTo({ top: 0, behavior: "smooth" });
    });

    window.addEventListener("scroll", function () {
        backToTop.style.display = window.scrollY > 400 ? "flex" : "none";
    });
}