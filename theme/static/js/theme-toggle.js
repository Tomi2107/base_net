document.addEventListener("DOMContentLoaded", () => {
    const toggleBtn = document.getElementById("theme-toggle");
    const toggleCircle = document.getElementById("theme-toggle-circle");
    const html = document.documentElement;

    if (!toggleBtn || !toggleCircle) return;

    if (html.classList.contains("dark")) {
        toggleCircle.classList.add("translate-x-6");
    }

    toggleBtn.addEventListener("click", () => {
        const isDark = html.classList.toggle("dark");

        if (isDark) {
            localStorage.setItem("theme", "dark");
            toggleCircle.classList.add("translate-x-6");
        } else {
            localStorage.setItem("theme", "light");
            toggleCircle.classList.remove("translate-x-6");
        }
    });
});
