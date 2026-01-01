(function () {
    const html = document.documentElement;
    const theme = localStorage.getItem("theme");

    if (theme === "dark") {
        html.classList.add("dark");
    }
})();
