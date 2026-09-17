tailwind.config = {
    darkMode: "class",
    theme: {
        extend: {
            colors: {
                brand: {
                    50: "#f0fdf9",
                    100: "#ccfbef",
                    200: "#99f6e0",
                    500: "#2ea87a",
                    600: "#25916a",
                    700: "#1a6b4f",
                    900: "#0f3d2e",
                },
            },
            fontFamily: {
                sans: ["Inter", "system-ui", "sans-serif"],
                serif: ["Merriweather", "Georgia", "serif"],
            },
            typography: {
                DEFAULT: {
                    css: {
                        maxWidth: "72ch",
                    },
                },
            },
        },
    },
};