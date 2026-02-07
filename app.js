// CHANGED: Use relative path. This works on Localhost AND Render automatically.
const API_URL = "/chat"; 

const chatWindow = document.getElementById("chatWindow");
const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");

// Add event listener for the button
sendBtn.addEventListener("click", sendMessage);

// Add event listener for "Enter" key
userInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

function addMessage(text, role) {
    const msg = document.createElement("div");
    msg.className = `message ${role}`;
    msg.innerText = text;
    chatWindow.appendChild(msg);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function showTyping() {
    const typing = document.createElement("div");
    typing.className = "message bot";
    typing.id = "typing";
    typing.innerText = "Doctor AI is thinking...";
    chatWindow.appendChild(typing);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function removeTyping() {
    const typing = document.getElementById("typing");
    if (typing) typing.remove();
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    addMessage(text, "user");
    userInput.value = "";
    showTyping();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        removeTyping();
        addMessage(data.reply, "bot");

    } catch (error) {
        removeTyping();
        addMessage("Unable to connect to server.", "bot");
        console.error(error);
    }
}
