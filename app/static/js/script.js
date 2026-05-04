/**
 * script.js — General UI helpers for My Blog
 * Theme management lives in theme.js (loaded first in base.html).
 */

document.addEventListener("DOMContentLoaded", function () {
    // Auto-close flash messages after 4 seconds.
    document.querySelectorAll(".error, .flash").forEach(function (el) {
        setTimeout(function () {
            el.style.transition = "opacity 0.4s";
            el.style.opacity = "0";
            setTimeout(function () { el.remove(); }, 400);
        }, 4000);
    });
});