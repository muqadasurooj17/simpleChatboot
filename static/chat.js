async function sendMessage() {
    const input = document.getElementById("message");
    const chat = document.getElementById("chat");
    const userText = input.value.trim();
    if (!userText) return;

    // Add user message with avatar
    chat.innerHTML += `
    <div class="flex justify-end items-start gap-2">
        <div class="bg-blue-600 p-3 rounded-lg max-w-2xl break-words">
            <span class="font-semibold">You:</span> ${userText}
        </div>
        <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white text-lg">🙂</div>
    </div>
    `;

    input.value = "";
    chat.scrollTop = chat.scrollHeight;

    // Fetch bot response
    const response = await fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: userText})
    });

    const data = await response.json();
    const botText = data.reply;

    // Add bot response with avatar
    chat.innerHTML += `
    <div class="flex justify-start items-start gap-2">
        <div class="w-10 h-10 rounded-full bg-gray-500 flex items-center justify-center text-white text-lg">🤖</div>
        <div class="bg-gray-700 p-3 rounded-lg max-w-2xl break-words">
            <span class="font-semibold">Bot:</span> ${botText}
        </div>
    </div>
    `;
    chat.scrollTop = chat.scrollHeight;
}

// Send on Enter key
document.getElementById("message").addEventListener("keydown", function(e) {
    if (e.key === "Enter") sendMessage();
});

// Send on button click
document.getElementById("sendBtn").addEventListener("click", sendMessage);