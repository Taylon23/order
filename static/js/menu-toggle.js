$(document).ready(function () {
    var menuAberto = false;

    $(".content-icon-menu-mobile").click(function (event) {
        event.stopPropagation();
        menuAberto = !menuAberto; // Inverte o estado do menu
        if (menuAberto) {
            $(".menu-ul-topo").slideDown();
        } else {
            $(".menu-ul-topo").slideUp();
        }
    });

    $(document).click(function (event) {
        var target = $(event.target);
        if (!target.closest(".menu-ul-topo").length && !target.hasClass("content-icon-menu-mobile")) {
            if (menuAberto) {
                $(".menu-ul-topo").slideUp();
                menuAberto = false;
            }
        }
    });
});
