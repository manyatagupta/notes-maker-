import os
import subprocess

DASHBOARD = 'study_app/templates/study_app/dashboard.html'
LOGIN = 'study_app/templates/study_app/login.html'
REGISTER = 'study_app/templates/study_app/register.html'
FILES = [DASHBOARD, LOGIN, REGISTER]

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def replace_in_files(replacements):
    for path in FILES:
        if path not in replacements:
            continue
        content = read_file(path)
        for old, new in replacements[path]:
            if old in content:
                content = content.replace(old, new)
            else:
                print(f"WARNING: Could not find '{old[:50]}...' in {path}")
        write_file(path, content)

def commit(message):
    run("git add " + " ".join(FILES))
    run(f'git commit -m "{message}"')

# Ensure we're in a clean state (the files are currently modified with all changes, so we revert)
# First stash any changes just in case.
run("git checkout -- study_app/templates/study_app/dashboard.html study_app/templates/study_app/login.html study_app/templates/study_app/register.html")

# STEP 1: Head config
head_old = """    <script src="https://cdn.tailwindcss.com"></script>
</head>"""
head_new = """    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
        }
    </script>
    <script>
        if (localStorage.getItem('color-theme') === 'dark' || (!('color-theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches)) {
            document.documentElement.classList.add('dark');
        } else {
            document.documentElement.classList.remove('dark');
        }
    </script>
</head>"""

replace_in_files({
    DASHBOARD: [(head_old, head_new)],
    LOGIN: [(head_old, head_new)],
    REGISTER: [(head_old, head_new)]
})
commit("feat(ui): add Tailwind dark mode configuration in head sections")

# STEP 2: Body tags
dashboard_body_old = '<body class="bg-gray-50 min-h-screen font-sans text-gray-800">'
dashboard_body_new = '<body class="bg-gray-50 dark:bg-gray-900 min-h-screen font-sans text-gray-800 dark:text-gray-100 transition-colors duration-200">'

login_body_old = '<body class="bg-gray-50 flex flex-col min-h-screen">'
login_body_new = '<body class="bg-gray-50 dark:bg-gray-900 flex flex-col min-h-screen text-gray-800 dark:text-gray-100 transition-colors duration-200">'

replace_in_files({
    DASHBOARD: [(dashboard_body_old, dashboard_body_new)],
    LOGIN: [(login_body_old, login_body_new)],
    REGISTER: [(login_body_old, login_body_new)]
})
commit("feat(ui): implement dark mode background and text colors on body")


# STEP 3: Toggle button
toggle_svg = """<button id="theme-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5">
                    <svg id="theme-toggle-dark-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M17.293 13.293A8 8 0 016.707 2.707a8.001 8.001 0 1010.586 10.586z"></path></svg>
                    <svg id="theme-toggle-light-icon" class="hidden w-5 h-5" fill="currentColor" viewBox="0 0 20 20"><path d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4.22 4.22a1 1 0 011.415 0l.708.708a1 1 0 01-1.414 1.414l-.708-.708a1 1 0 010-1.415zM12 10a2 2 0 11-4 0 2 2 0 014 0zM17 10a1 1 0 110 2h-1a1 1 0 110-2h1zm-4.22 4.22a1 1 0 010 1.415l-.708.708a1 1 0 01-1.414-1.414l.708.708a1 1 0 011.415 0zM10 17a1 1 0 11-2 0v-1a1 1 0 112 0v1zm-4.22-4.22a1 1 0 01-1.415 0l-.708-.708a1 1 0 011.414-1.414l.708.708a1 1 0 010 1.415zM3 10a1 1 0 110-2h1a1 1 0 110 2H3zm4.22-4.22a1 1 0 010-1.415l.708-.708a1 1 0 011.414 1.414l-.708.708a1 1 0 01-1.415 0z"></path></svg>
                </button>"""

dash_nav_old = """            <div class="flex gap-4 items-center">
                <a href="{% url 'index' %}" class="text-gray-600 hover:text-blue-600">Generate Notes</a>"""
dash_nav_new = f"""            <div class="flex gap-4 items-center">
                {toggle_svg}
                <a href="{{% url 'index' %}}" class="text-gray-600 hover:text-blue-600">Generate Notes</a>"""

login_nav_old = """            <div class="flex gap-4">
                <a href="{% url 'register' %}" class="text-blue-600 font-medium hover:underline">Register</a>
            </div>"""
login_nav_new = f"""            <div class="flex gap-4 items-center">
                {toggle_svg}
                <a href="{{% url 'register' %}}" class="text-blue-600 font-medium hover:underline">Register</a>
            </div>"""

reg_nav_old = """            <div class="flex gap-4">
                <a href="{% url 'login' %}" class="text-blue-600 font-medium hover:underline">Login</a>
            </div>"""
reg_nav_new = f"""            <div class="flex gap-4 items-center">
                {toggle_svg}
                <a href="{{% url 'login' %}}" class="text-blue-600 font-medium hover:underline">Login</a>
            </div>"""

replace_in_files({
    DASHBOARD: [(dash_nav_old, dash_nav_new)],
    LOGIN: [(login_nav_old, login_nav_new)],
    REGISTER: [(reg_nav_old, reg_nav_new)]
})
commit("feat(ui): add dark mode theme toggle button in navigation bars")


# STEP 4: Components & Layout styles
dash_replacements = [
    ('<nav class="bg-white shadow-sm py-4">', '<nav class="bg-white dark:bg-gray-800 shadow-sm py-4 transition-colors duration-200">'),
    ('<a href="{% url \'index\' %}" class="text-xl font-bold text-gray-800 flex items-center gap-2">', '<a href="{% url \'index\' %}" class="text-xl font-bold text-gray-800 dark:text-white flex items-center gap-2">'),
    ('<a href="{% url \'index\' %}" class="text-gray-600 hover:text-blue-600">Generate Notes</a>', '<a href="{% url \'index\' %}" class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400">Generate Notes</a>'),
    ('<button type="submit" class="text-blue-600 font-medium hover:underline">Logout</button>', '<button type="submit" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Logout</button>'),
    ('<h2 class="text-3xl font-bold text-gray-800 mb-6">Your Saved Notes</h2>', '<h2 class="text-3xl font-bold text-gray-800 dark:text-white mb-6">Your Saved Notes</h2>'),
    ('<div class="bg-white rounded-xl shadow-md p-6 hover:shadow-lg transition">', '<div class="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 hover:shadow-lg transition">'),
    ('<h3 class="font-bold text-lg text-gray-800 mb-2 truncate">{{ mat.title }}</h3>', '<h3 class="font-bold text-lg text-gray-800 dark:text-white mb-2 truncate">{{ mat.title }}</h3>'),
    ('<p class="text-sm text-gray-500 mb-4">{{ mat.created_at|date:"M d, Y" }}</p>', '<p class="text-sm text-gray-500 dark:text-gray-400 mb-4">{{ mat.created_at|date:"M d, Y" }}</p>'),
    ('<a href="{% url \'index\' %}?video_id={{ mat.video_id }}" class="bg-blue-50 text-blue-600 px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-blue-100 transition">View Details</a>', '<a href="{% url \'index\' %}?video_id={{ mat.video_id }}" class="bg-blue-50 dark:bg-blue-900/50 text-blue-600 dark:text-blue-400 px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-blue-100 dark:hover:bg-blue-900 transition">View Details</a>'),
    ('<a href="https://youtube.com/watch?v={{ mat.video_id }}" target="_blank" class="bg-gray-50 text-gray-600 px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-gray-100 transition">Watch</a>', '<a href="https://youtube.com/watch?v={{ mat.video_id }}" target="_blank" class="bg-gray-50 dark:bg-gray-700 text-gray-600 dark:text-gray-300 px-3 py-1.5 rounded-lg text-sm font-medium hover:bg-gray-100 dark:hover:bg-gray-600 transition">Watch</a>'),
    ('<div class="bg-white rounded-xl shadow-sm p-12 text-center border border-gray-200">', '<div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm p-12 text-center border border-gray-200 dark:border-gray-700">'),
    ('<svg class="w-16 h-16 text-gray-300 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>', '<svg class="w-16 h-16 text-gray-300 dark:text-gray-600 mx-auto mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path></svg>'),
    ('<h3 class="text-lg font-medium text-gray-800 mb-2">No notes yet</h3>', '<h3 class="text-lg font-medium text-gray-800 dark:text-white mb-2">No notes yet</h3>'),
    ('<p class="text-gray-500 mb-6">You haven\'t generated any study materials yet.</p>', '<p class="text-gray-500 dark:text-gray-400 mb-6">You haven\'t generated any study materials yet.</p>')
]

login_replacements = [
    ('<nav class="bg-white shadow-sm py-4">', '<nav class="bg-white dark:bg-gray-800 shadow-sm py-4 transition-colors duration-200">'),
    ('<a href="{% url \'index\' %}" class="text-xl font-bold text-gray-800 flex items-center gap-2">', '<a href="{% url \'index\' %}" class="text-xl font-bold text-gray-800 dark:text-white flex items-center gap-2">'),
    ('<a href="{% url \'register\' %}" class="text-blue-600 font-medium hover:underline">Register</a>', '<a href="{% url \'register\' %}" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Register</a>'),
    ('<div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8">', '<div class="max-w-md w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8">'),
    ('<h2 class="text-2xl font-bold text-center text-gray-900 mb-6">Login to your account</h2>', '<h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white mb-6">Login to your account</h2>'),
    ('<label class="block text-sm font-medium text-gray-700 mb-1" for="{{ field.id_for_label }}">{{ field.label }}</label>', '<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" for="{{ field.id_for_label }}">{{ field.label }}</label>'),
    ('<p class="mt-4 text-center text-sm text-gray-600">Don\'t have an account? <a href="{% url \'register\' %}" class="text-blue-600 font-medium hover:underline">Register</a></p>', '<p class="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">Don\'t have an account? <a href="{% url \'register\' %}" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Register</a></p>')
]

register_replacements = [
    ('<nav class="bg-white shadow-sm py-4">', '<nav class="bg-white dark:bg-gray-800 shadow-sm py-4 transition-colors duration-200">'),
    ('<a href="{% url \'index\' %}" class="text-xl font-bold text-gray-800 flex items-center gap-2">', '<a href="{% url \'index\' %}" class="text-xl font-bold text-gray-800 dark:text-white flex items-center gap-2">'),
    ('<a href="{% url \'login\' %}" class="text-blue-600 font-medium hover:underline">Login</a>', '<a href="{% url \'login\' %}" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Login</a>'),
    ('<div class="max-w-md w-full bg-white rounded-xl shadow-lg p-8 mt-10 mb-10">', '<div class="max-w-md w-full bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 mt-10 mb-10">'),
    ('<h2 class="text-2xl font-bold text-center text-gray-900 mb-6">Create an account</h2>', '<h2 class="text-2xl font-bold text-center text-gray-900 dark:text-white mb-6">Create an account</h2>'),
    ('<label class="block text-sm font-medium text-gray-700 mb-1" for="{{ field.id_for_label }}">{{ field.label }}</label>', '<label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1" for="{{ field.id_for_label }}">{{ field.label }}</label>'),
    ('<p class="mt-4 text-center text-sm text-gray-600">Already have an account? <a href="{% url \'login\' %}" class="text-blue-600 font-medium hover:underline">Login</a></p>', '<p class="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">Already have an account? <a href="{% url \'login\' %}" class="text-blue-600 dark:text-blue-400 font-medium hover:underline">Login</a></p>')
]

replace_in_files({
    DASHBOARD: dash_replacements,
    LOGIN: login_replacements,
    REGISTER: register_replacements
})
commit("feat(ui): style navigation bars and layout components for dark mode")


# STEP 5: Form inputs
login_css_old = """        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            border: 1px solid #d1d5db;
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 1px #3b82f6;
        }"""
login_css_new = """        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            border: 1px solid #d1d5db;
            outline: none;
            transition: border-color 0.2s;
            background-color: transparent;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 1px #3b82f6;
        }
        .dark input[type="text"], .dark input[type="password"] {
            border-color: #4b5563; /* gray-600 */
            color: #f3f4f6; /* gray-100 */
        }"""

reg_css_old = """        input[type="text"], input[type="password"] {
            width: 100%;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            border: 1px solid #d1d5db;
            outline: none;
            transition: border-color 0.2s;
        }
        input[type="text"]:focus, input[type="password"]:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 1px #3b82f6;
        }"""
reg_css_new = """        input[type="text"], input[type="password"], input[type="email"] {
            width: 100%;
            padding: 0.5rem 0.75rem;
            border-radius: 0.375rem;
            border: 1px solid #d1d5db;
            outline: none;
            transition: border-color 0.2s;
            background-color: transparent;
        }
        input[type="text"]:focus, input[type="password"]:focus, input[type="email"]:focus {
            border-color: #3b82f6;
            box-shadow: 0 0 0 1px #3b82f6;
        }
        .dark input[type="text"], .dark input[type="password"], .dark input[type="email"] {
            border-color: #4b5563; /* gray-600 */
            color: #f3f4f6; /* gray-100 */
        }"""

replace_in_files({
    LOGIN: [(login_css_old, login_css_new)],
    REGISTER: [(reg_css_old, reg_css_new)]
})
commit("feat(ui): apply dark mode styling to form inputs and error messages")


# STEP 6: JS logic
js_logic = """    <script>
        document.addEventListener('DOMContentLoaded', () => {
            const themeToggleDarkIcon = document.getElementById('theme-toggle-dark-icon');
            const themeToggleLightIcon = document.getElementById('theme-toggle-light-icon');
            const themeToggleBtn = document.getElementById('theme-toggle');

            if (document.documentElement.classList.contains('dark')) {
                themeToggleLightIcon.classList.remove('hidden');
            } else {
                themeToggleDarkIcon.classList.remove('hidden');
            }

            themeToggleBtn.addEventListener('click', function() {
                themeToggleDarkIcon.classList.toggle('hidden');
                themeToggleLightIcon.classList.toggle('hidden');
                document.documentElement.classList.toggle('dark');
                if (document.documentElement.classList.contains('dark')) {
                    localStorage.setItem('color-theme', 'dark');
                } else {
                    localStorage.setItem('color-theme', 'light');
                }
            });
        });
    </script>
</body>"""

replace_in_files({
    DASHBOARD: [("</body>", js_logic)],
    LOGIN: [("</body>", js_logic)],
    REGISTER: [("</body>", js_logic)]
})
commit("feat(ui): add javascript logic for theme toggling across templates")

run("git push")
