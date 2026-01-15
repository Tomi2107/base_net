document.addEventListener("DOMContentLoaded", () => {
    const toggle = document.getElementById("theme-toggle");
    const circle = document.getElementById("theme-toggle-circle");
    const html = document.documentElement;

    if (!toggle || !circle) return;

    // estado inicial
    if (html.classList.contains("dark")) {
        circle.classList.add("translate-x-6");
    }

    toggle.addEventListener("click", () => {
        const isDark = html.classList.toggle("dark");

        if (isDark) {
            localStorage.setItem("theme", "dark");
            circle.classList.add("translate-x-6");
        } else {
            localStorage.setItem("theme", "light");
            circle.classList.remove("translate-x-6");
        }
    });
});
