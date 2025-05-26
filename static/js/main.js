document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", function (e) {
        const inputs = form.querySelectorAll("input[type='number']");
        let valid = true;

        inputs.forEach(input => {
            if (input.value === "") {
                input.style.border = "1px solid red";
                valid = false;
            } else {
                input.style.border = "1px solid #ccc";
            }
        });

        if (!valid) {
            e.preventDefault();
            alert("Please fill all fields before submitting.");
        }
    });
});
