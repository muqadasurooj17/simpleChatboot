from html import escape


def user_bubble(text: str) -> str:
    safe = escape(text)
    return f"""
    <div class="flex justify-end items-start gap-2">
        <div class="bg-blue-600 p-3 rounded-lg max-w-2xl break-words">
            <span class="font-semibold">You:</span> {safe}
        </div>
        <div class="w-10 h-10 rounded-full bg-blue-500 flex items-center justify-center text-white text-lg">🙂</div>
    </div>
    """


def bot_bubble(text: str) -> str:
    safe = escape(text)
    return f"""
    <div class="flex justify-start items-start gap-2">
        <div class="w-10 h-10 rounded-full bg-gray-500 flex items-center justify-center text-white text-lg">🤖</div>
        <div class="bg-gray-700 p-3 rounded-lg max-w-2xl break-words">
            <span class="font-semibold">Bot:</span> {safe}
        </div>
    </div>
    """


def render_messages(messages: list[dict]) -> str:
    parts = []
    for msg in messages:
        if msg["role"] == "user":
            parts.append(user_bubble(msg["text"]))
        else:
            parts.append(bot_bubble(msg["text"]))
    return "\n".join(parts)


def render_page(messages: list[dict]) -> str:
    chat_html = render_messages(messages)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Chatbot</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 flex flex-col h-screen text-white">

<header class="bg-gray-800 p-4 text-center shadow">
    <h1 class="text-3xl font-bold">🤖 ChatBot</h1>
</header>

<main class="flex-1 flex flex-col p-4 overflow-hidden">
    <div id="chat" class="flex-1 overflow-y-auto p-4 space-y-4 rounded border border-gray-700 bg-gray-800">
        {chat_html}
    </div>

    <form method="post" action="/chat" class="flex gap-2 mt-4">
        <input
            name="message"
            class="flex-1 p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Type your message..."
            required
            autofocus
        />
        <button type="submit" class="bg-blue-500 hover:bg-blue-600 text-white px-6 rounded font-semibold">
            Send
        </button>
    </form>
</main>

</body>
</html>
"""
