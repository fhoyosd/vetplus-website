const password = document.getElementById("password");
const confirm_password = document.getElementById("confirm_password");

function validarPassword() {
    if (password.value !== confirm_password.value) {
    confirm_password.setCustomValidity("Las contraseñas no coinciden");
    } 
    else {
    confirm_password.setCustomValidity("");
    }
}

password.oninput = validarPassword;
confirm_password.oninput = validarPassword;

// Validar captcha antes de enviar
document.getElementById("registerForm").addEventListener("submit", function(event) {
    const response = grecaptcha.getResponse();
    const errorMsg = document.getElementById("captchaError");

    if (response.length === 0) {
    event.preventDefault();
    errorMsg.style.display = "block";
    } 
    else {
    errorMsg.style.display = "none";
    }
});