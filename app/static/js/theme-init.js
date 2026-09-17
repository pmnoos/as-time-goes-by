(function () {
    try {
        if (localStorage.getItem("theme") === "dark") {
            document.documentElement.classList.add("dark");
        }
    } catch (error) {
        // Theme selection remains optional when storage is unavailable.
    }
})();