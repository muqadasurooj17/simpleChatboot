from html import escape


def render_login_page(error: str | None = None) -> str:
    error_html = ""
    if error:
        error_html = f"""
        <div class="bg-red-900 text-red-200 border border-red-700 p-3 rounded mb-4">
            {escape(error)}
        </div>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Log In - ChatBot</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 flex flex-col items-center justify-center min-h-screen text-white">

<header class="text-center mb-6">
    <h1 class="text-3xl font-bold">🤖 ChatBot</h1>
    <p class="text-gray-400 mt-1">Welcome back</p>
</header>

<main class="bg-gray-800 border border-gray-700 rounded-lg p-8 w-full max-w-md">
    {error_html}
    <form method="post" action="/login" class="space-y-4">
        <input
            name="email"
            type="email"
            class="w-full p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Email"
            required
            autofocus
        />
        <input
        name="password"
        type="password"
        class="w-full p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
        placeholder="Password"
        required
        autofocus

        />
        <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white p-3 rounded font-semibold">
            Log In
        </button>
    </form>

    <p class="text-gray-400 text-sm text-center mt-4">
        Don't have an account?
        <a href="/signup" class="text-blue-400 hover:underline">Create one</a>
    </p>
</main>

</body>
</html>
"""