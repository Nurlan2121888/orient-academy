document.addEventListener("DOMContentLoaded", () => {

    const sidebar = document.getElementById("sidebar");
    const menuButton = document.getElementById("menuButton");
    const sidebarClose = document.getElementById("sidebarClose");
    const sidebarOverlay = document.getElementById("sidebarOverlay");


    function openSidebar() {

        if (!sidebar) return;

        sidebar.classList.add("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.add("show");
        }

        document.body.style.overflow = "hidden";
    }


    function closeSidebar() {

        if (!sidebar) return;

        sidebar.classList.remove("open");

        if (sidebarOverlay) {
            sidebarOverlay.classList.remove("show");
        }

        document.body.style.overflow = "";
    }


    if (menuButton) {
        menuButton.addEventListener(
            "click",
            openSidebar
        );
    }


    if (sidebarClose) {
        sidebarClose.addEventListener(
            "click",
            closeSidebar
        );
    }


    if (sidebarOverlay) {
        sidebarOverlay.addEventListener(
            "click",
            closeSidebar
        );
    }


    document.addEventListener(
        "keydown",
        (event) => {

            if (event.key === "Escape") {
                closeSidebar();
            }

        }
    );


    /*
     * Mobil cihazda menyudan linkə klik edildikdə
     * sidebar bağlansın.
     */

    if (sidebar) {

        const links = sidebar.querySelectorAll(
            ".nav-link"
        );

        links.forEach((link) => {

            link.addEventListener(
                "click",
                closeSidebar
            );

        });

    }

});