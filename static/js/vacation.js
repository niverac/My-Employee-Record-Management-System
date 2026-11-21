
document.addEventListener("DOMContentLoaded", function () {

    const employeeSelect = document.getElementById("employee_id");
    const firstNameInput = document.getElementById("first_name");
    const lastNameInput = document.getElementById("last_name");

    employeeSelect.addEventListener("change", function () {

        const selectedOption =
            employeeSelect.options[employeeSelect.selectedIndex];

        const firstName = selectedOption.dataset.firstName || "";
        const lastName = selectedOption.dataset.lastName || "";

        firstNameInput.value = firstName;
        lastNameInput.value = lastName;

    });

});
