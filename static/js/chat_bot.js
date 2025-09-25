// chat_bot.js

const toggleBtn = document.getElementById("chatbotToggle");
const chatWindow = document.getElementById("chatbotContainer");
const chatInput = document.getElementById("chatInput");
const chatSend = document.getElementById("sendBtn");

let awaitingInvoiceId = false;
const loggedIn = Boolean(window.loggedIn);

// Mostrar mensaje inicial cuando se carga la página
document.addEventListener("DOMContentLoaded", () => {
    showMenu();
});

toggleBtn.addEventListener("click", () => {
    chatWindow.style.display = chatWindow.style.display === "flex" ? "none" : "flex";
});

chatSend.addEventListener("click", () => {
    handleUserInput();
});

chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleUserInput();
});

function handleUserInput() {
    const userText = chatInput.value.trim();
    if (!userText) return;

    addMessage(userText, "user");

    if (awaitingInvoiceId) {
        if (!/^\d+$/.test(userText)) {
            addMessage("⚠️ El ID de la factura debe ser un número válido.", "bot");
            chatInput.value = "";
            return;
        }

        const invoiceId = userText;
        checkInvoice(invoiceId);
        awaitingInvoiceId = false;
        chatInput.value = "";
        return;
    }

    const choice = parseInt(userText);

    switch (choice) {
        case 1: 
            if (loggedIn) {
                addMessage('🔗 Haz clic aquí para registrar tu mascota: <a href="http://localhost:5000/pets" target="_blank">Registrar mascota</a>', "bot");
            } else {
                addMessage('🔑 Debes iniciar sesión primero: <a href="http://localhost:5000/login" target="_blank">Iniciar sesión</a>', "bot");
            }
            break;

        case 2:
            if (loggedIn) {
                addMessage('📋 Consulta el historial clínico aquí: <a href="http://localhost:5000/pets" target="_blank">Historial clínico</a>', "bot");
            } else {
                addMessage('🔑 Debes iniciar sesión primero: <a href="http://localhost:5000/login" target="_blank">Iniciar sesión</a>', "bot");
            }
            break;

        case 3:
            addMessage("✍️ Por favor, ingresa el ID de la factura:", "bot");
            awaitingInvoiceId = true;
            break;

        case 4:
            addMessage('📞 Aquí tienes la página de contacto: <a href="http://localhost:5000/contacto" target="_blank">Contacto</a>', "bot");
            break;

        case 5:
            addMessage("🔄 Saliendo...", "bot");
            showMenu();
            break;

        default:
            addMessage("⚠️ Opción no válida. Intenta de nuevo.", "bot");
            showMenu();
            break;
    }

    chatInput.value = "";
}

function checkInvoice(invoiceId) {
    fetch(`/orders/check/${invoiceId}`)
        .then(res => res.json())
        .then(data => {
            if (data.exists) {
                addMessage(`✅ Factura encontrada. <a href="http://localhost:5000/invoice/${invoiceId}" target="_blank">Ver factura #${invoiceId}</a>`, "bot");
            } else {
                addMessage("❌ No se encontró ninguna factura con ese ID.", "bot");
            }
        })
        .catch(() => {
            addMessage("⚠️ Error al verificar la factura. Intenta más tarde.", "bot");
        });
}

function addMessage(content, sender = "bot") {
    const messages = document.getElementById("chatbotMessages");
    const msg = document.createElement("div");
    msg.classList.add("message");
    msg.classList.add(sender === "bot" ? "bot-message" : "user-message");
    msg.innerHTML = content;
    messages.appendChild(msg);
    messages.scrollTop = messages.scrollHeight;
}

function showMenu() {
    addMessage(
        "👋 ¡Hola! Soy tu asistente virtual de VetPlus.<br><br>" +
        "Elige una opción del menú:<br>" +
        "1️⃣ Registrar nueva mascota<br>" +
        "2️⃣ Consultar historial clínico<br>" +
        "3️⃣ Ver detalles de una factura<br>" +
        "4️⃣ Información de contacto<br>" +
        "5️⃣ Salir / Volver al menú principal<br><br>" +
        "Selecciona un número del índice.",
        "bot"
    );
}
