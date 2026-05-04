/**
 * theme.js — Theme management for My Blog
 *
 * Priority order:
 *   1. User's explicit saved preference (localStorage)
 *   2. OS / browser prefers-color-scheme
 *   3. Default: light
 */

(function () {
    // ── Helpers ────────────────────────────────────────────────────────────────

    function getSystemTheme() {
        if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
            return "dark";
        }
        return "light";
    }

    function getSavedTheme() {
        try {
            const stored = window.localStorage.getItem("theme");
            if (stored === "light" || stored === "dark") {
                return stored;
            }
        } catch (e) {
            // Storage blocked — fall through to system preference.
        }
        return null;
    }

    function saveTheme(theme) {
        try {
            window.localStorage.setItem("theme", theme);
        } catch (e) {
            // Ignore — toggle still works for this session.
        }
    }

    function resolveTheme() {
        return getSavedTheme() || getSystemTheme();
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        updateButton(theme);
    }

    function updateButton(theme) {
        const btn = document.getElementById("theme-btn");
        if (!btn) return;
        btn.textContent = theme === "dark" ? "☀ Light" : "🌙 Dark";
        btn.setAttribute("aria-label", theme === "dark" ? "Switch to light mode" : "Switch to dark mode");
    }

    // ── Apply theme immediately (before DOMContentLoaded) to avoid flash ───────
    applyTheme(resolveTheme());

    // ── Wire up button and system-change listener after DOM is ready ───────────
    document.addEventListener("DOMContentLoaded", function () {
        // Re-apply in case DOMContentLoaded fired before our IIFE ran.
        applyTheme(resolveTheme());

        // Button click — explicit user toggle.
        const btn = document.getElementById("theme-btn");
        if (btn) {
            btn.addEventListener("click", function () {
                const current = document.documentElement.getAttribute("data-theme") || "light";
                const next = current === "light" ? "dark" : "light";
                applyTheme(next);
                saveTheme(next);
            });
        }

        // System theme change — only auto-update if user has no saved preference.
        if (window.matchMedia) {
            window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function (e) {
                if (!getSavedTheme()) {
                    applyTheme(e.matches ? "dark" : "light");
                }
            });
        }
    });
})();
