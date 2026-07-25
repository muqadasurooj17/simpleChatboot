from html import escape

def render_create_user_page(error: str | None = None) -> str:
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
    <title>Create Account - ChatBot</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-900 flex flex-col items-center justify-center min-h-screen text-white">

<header class="text-center mb-6">
    <h1 class="text-3xl font-bold">🤖 ChatBot</h1>
    <p class="text-gray-400 mt-1">Create your account</p>
</header>

<main class="bg-gray-800 border border-gray-700 rounded-lg p-4 w-full max-w-lg">
    {error_html}
    <form method="post" action="/signup" class="space-y-4">
        <div class="flex gap-2">
            <input
                name="first_name"
                class="flex-1 p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="First name"
                required
            />
            <input
                name="last_name"
                class="flex-1 p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Last name"
                required
            />
        </div>
<div class="flex gap-2">
        <input
            name="email"
            type="email"
            class="w-full p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Email"
            required
        />

        <input
            name="password"
            type="password"
            class="w-full p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Password"
            required
        />
        </div>
        
        <input
            name="phone"
            class="w-full p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            placeholder="Phone number"
            required
        />
        <div class="flex gap-2">
            <input
                name="age"
                type="number"
                min="1"
                class="flex-1 p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Age"
                required
            />
            <input
                name="country"
                class="flex-1 p-3 rounded bg-gray-900 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Country"
                required
            />
        </div>
        <button type="submit" class="w-full bg-blue-500 hover:bg-blue-600 text-white p-3 rounded font-semibold">
            Create Account
        </button>
    </form>

    <p class="text-gray-400 text-sm text-center mt-4">
        Already have an account?
        <a href="/login" class="text-blue-400 hover:underline">Log in</a>
    </p>
</main>
</body>
</html>
"""