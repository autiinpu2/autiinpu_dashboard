document.addEventListener("DOMContentLoaded", function() {
    var checkbox = document.getElementById("cbx-51");
    if (checkbox) {
        checkbox.addEventListener("change", function() {
            document.body.classList.toggle("dark-mode", this.checked);
            document.querySelector('.content').classList.toggle("dark-mode", this.checked);
            document.querySelector('.sidebar').classList.toggle("dark-mode", this.checked);
            document.querySelectorAll('.stat-button, .settings_button').forEach(function(button) {
                button.classList.toggle("dark-mode", this.checked);
            });
        });
    } else {
        console.error("L'élément avec l'ID cbx-51 n'existe pas.");
    }
});
