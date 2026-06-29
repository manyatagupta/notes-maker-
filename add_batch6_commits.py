import os
import subprocess

INDEX = r"c:\Users\manya\OneDrive\Desktop\notes maker\study_app\templates\study_app\index.html"
DASHBOARD = r"c:\Users\manya\OneDrive\Desktop\notes maker\study_app\templates\study_app\dashboard.html"

def run(cmd):
    print(f"Running: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def commit(message):
    run('git add "' + INDEX + '"')
    run('git add "' + DASHBOARD + '"')
    run(f'git commit -m "{message}"')

# Ensure clean slate for these files
run('git checkout -- "' + INDEX + '" "' + DASHBOARD + '"')

print("Applying Batch 6 Features and Committing...")

# --- Feature 1: Bionic Reading ---
index_content = read_file(INDEX)
eli5_btn = """<button id="eli5-notes-btn" class="bg-pink-100 hover:bg-pink-200 text-pink-700 dark:bg-pink-900 dark:text-pink-300 px-3 py-1.5 rounded text-sm font-medium transition ml-2">
                                    🧒 ELI5
                                </button>"""
bionic_btn = """<button id="eli5-notes-btn" class="bg-pink-100 hover:bg-pink-200 text-pink-700 dark:bg-pink-900 dark:text-pink-300 px-3 py-1.5 rounded text-sm font-medium transition ml-2">
                                    🧒 ELI5
                                </button>
                                <button id="bionic-btn" class="bg-indigo-100 hover:bg-indigo-200 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300 px-3 py-1.5 rounded text-sm font-medium transition ml-2" title="Bionic Reading Mode">
                                    👁️ Bionic
                                </button>"""
index_content = index_content.replace(eli5_btn, bionic_btn)

bionic_js = """
            // Feature 1: Bionic Reading
            const bionicBtn = document.getElementById('bionic-btn');
            let isBionic = false;
            let originalNotesHtml = '';
            
            function applyBionic(html) {
                const div = document.createElement('div');
                div.innerHTML = html;
                function processNode(node) {
                    if (node.nodeType === Node.TEXT_NODE) {
                        const words = node.textContent.split(/(\s+)/);
                        const span = document.createElement('span');
                        words.forEach(word => {
                            if (word.trim().length > 0) {
                                const mid = Math.ceil(word.length / 2);
                                const b = document.createElement('b');
                                b.textContent = word.slice(0, mid);
                                const rest = document.createTextNode(word.slice(mid));
                                span.appendChild(b);
                                span.appendChild(rest);
                            } else {
                                span.appendChild(document.createTextNode(word));
                            }
                        });
                        node.parentNode.replaceChild(span, node);
                    } else if (node.nodeType === Node.ELEMENT_NODE) {
                        Array.from(node.childNodes).forEach(processNode);
                    }
                }
                Array.from(div.childNodes).forEach(processNode);
                return div.innerHTML;
            }

            if (bionicBtn && notesContent) {
                bionicBtn.addEventListener('click', () => {
                    if (!originalNotesHtml) originalNotesHtml = notesContent.innerHTML;
                    if (!isBionic) {
                        notesContent.innerHTML = applyBionic(originalNotesHtml);
                        bionicBtn.classList.add('bg-indigo-300', 'dark:bg-indigo-700');
                        isBionic = true;
                    } else {
                        notesContent.innerHTML = originalNotesHtml;
                        bionicBtn.classList.remove('bg-indigo-300', 'dark:bg-indigo-700');
                        isBionic = false;
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 5: Reading Progress Bar", bionic_js + "\n            // Feature 5: Reading Progress Bar")
write_file(INDEX, index_content)
commit("feat(notes): implement bionic reading mode toggle")

# --- Feature 2: Estimated Reading Time ---
index_content = read_file(INDEX)
listen_notes_btn = """<button id="listen-notes-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition">
                                    🔊 Listen
                                </button>"""
reading_badge = """<span id="reading-time-badge" class="mr-2 text-xs font-semibold bg-gray-200 dark:bg-gray-700 text-gray-700 dark:text-gray-300 px-2 py-1.5 rounded hidden">
                                    ⏱️ 0 min read
                                </span>
                                <button id="listen-notes-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition">
                                    🔊 Listen
                                </button>"""
index_content = index_content.replace(listen_notes_btn, reading_badge)

populate_results_str = """function populateResults(data) {"""
reading_time_js = """function populateResults(data) {
                // Feature 2: Estimated Reading Time
                const wordCount = (data.notes || "").split(/\s+/).length + (data.summary || "").split(/\s+/).length;
                const readTime = Math.max(1, Math.ceil(wordCount / 200));
                const readBadge = document.getElementById('reading-time-badge');
                if(readBadge) {
                    readBadge.textContent = `⏱️ ${readTime} min read`;
                    readBadge.classList.remove('hidden');
                }
"""
index_content = index_content.replace(populate_results_str, reading_time_js)
write_file(INDEX, index_content)
commit("feat(notes): display estimated reading time based on word count")

# --- Feature 3: Font Size Adjuster ---
index_content = read_file(INDEX)
font_btns = """<div class="flex items-center bg-gray-100 dark:bg-gray-800 rounded px-2 py-1 mr-2 border border-gray-200 dark:border-gray-700">
                                    <button id="font-decrease" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">A-</button>
                                    <button id="font-reset" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">A</button>
                                    <button id="font-increase" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">A+</button>
                                </div>"""
index_content = index_content.replace('<button id="listen-notes-btn"', font_btns + '\n                                <button id="listen-notes-btn"')

font_js = """
            // Feature 3: Font Size Adjuster
            let currentFontSize = 16;
            document.getElementById('font-decrease')?.addEventListener('click', () => {
                currentFontSize = Math.max(12, currentFontSize - 2);
                if(notesContent) notesContent.style.fontSize = currentFontSize + 'px';
            });
            document.getElementById('font-increase')?.addEventListener('click', () => {
                currentFontSize = Math.min(24, currentFontSize + 2);
                if(notesContent) notesContent.style.fontSize = currentFontSize + 'px';
            });
            document.getElementById('font-reset')?.addEventListener('click', () => {
                currentFontSize = 16;
                if(notesContent) notesContent.style.fontSize = currentFontSize + 'px';
            });
"""
index_content = index_content.replace("// Feature 5: Reading Progress Bar", font_js + "\n            // Feature 5: Reading Progress Bar")
write_file(INDEX, index_content)
commit("feat(ui): add font size adjustment controls for notes")

# --- Feature 4: Teleprompter Auto-Scroll ---
index_content = read_file(INDEX)
scroll_btn = """<button id="autoscroll-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    📜 Auto-Scroll
                                </button>"""
index_content = index_content.replace('✏️ Edit Notes\n                                </button>', '✏️ Edit Notes\n                                </button>\n                                ' + scroll_btn)

scroll_js = """
            // Feature 4: Teleprompter Auto-Scroll
            let scrollInterval;
            let isScrolling = false;
            const scrollBtn = document.getElementById('autoscroll-btn');
            if(scrollBtn) {
                scrollBtn.addEventListener('click', () => {
                    if(isScrolling) {
                        clearInterval(scrollInterval);
                        isScrolling = false;
                        scrollBtn.classList.remove('bg-blue-200', 'dark:bg-blue-800');
                    } else {
                        scrollInterval = setInterval(() => { window.scrollBy(0, 1); }, 30);
                        isScrolling = true;
                        scrollBtn.classList.add('bg-blue-200', 'dark:bg-blue-800');
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 5: Reading Progress Bar", scroll_js + "\n            // Feature 5: Reading Progress Bar")
write_file(INDEX, index_content)
commit("feat(notes): implement teleprompter auto-scroll functionality")

# --- Feature 5: Confetti on Mastery ---
dashboard_content = read_file(DASHBOARD)
confetti_script = """    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>"""
dashboard_content = dashboard_content.replace('<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>', confetti_script)

mastered_js_old = """if (data.is_mastered) {
                            btn.textContent = '✅';
                        } else {"""
mastered_js_new = """if (data.is_mastered) {
                            btn.textContent = '✅';
                            confetti({ particleCount: 100, spread: 70, origin: { y: 0.6 } });
                        } else {"""
dashboard_content = dashboard_content.replace(mastered_js_old, mastered_js_new)
write_file(DASHBOARD, dashboard_content)
commit("feat(dashboard): trigger confetti animation on marking notes as mastered")

# --- Feature 6: Active Study Stopwatch ---
index_content = read_file(INDEX)
stopwatch_html = """
    <!-- Feature 6: Active Study Stopwatch -->
    <div id="stopwatch-widget" class="fixed top-24 right-6 bg-white dark:bg-gray-800 shadow-lg rounded-full px-4 py-2 border border-gray-200 dark:border-gray-700 z-50 flex items-center gap-3">
        <span class="text-sm font-bold text-gray-500">⏱️ Study Time</span>
        <span id="stopwatch-display" class="font-mono font-bold text-blue-600 dark:text-blue-400">00:00:00</span>
        <button id="stopwatch-toggle" class="hover:text-green-500 text-sm">▶️</button>
        <button id="stopwatch-reset" class="hover:text-red-500 text-sm">🔄</button>
    </div>
"""
index_content = index_content.replace('<!-- Reading Progress Bar -->', stopwatch_html + '\n    <!-- Reading Progress Bar -->')

stopwatch_js = """
            // Feature 6: Stopwatch
            let swSeconds = 0;
            let swInterval = null;
            const swDisplay = document.getElementById('stopwatch-display');
            const swToggle = document.getElementById('stopwatch-toggle');
            const swReset = document.getElementById('stopwatch-reset');
            
            function updateSwDisplay() {
                const h = String(Math.floor(swSeconds / 3600)).padStart(2, '0');
                const m = String(Math.floor((swSeconds % 3600) / 60)).padStart(2, '0');
                const s = String(swSeconds % 60).padStart(2, '0');
                if(swDisplay) swDisplay.textContent = `${h}:${m}:${s}`;
            }
            if(swToggle && swReset) {
                swToggle.addEventListener('click', () => {
                    if(swInterval) {
                        clearInterval(swInterval);
                        swInterval = null;
                        swToggle.textContent = '▶️';
                    } else {
                        swInterval = setInterval(() => { swSeconds++; updateSwDisplay(); }, 1000);
                        swToggle.textContent = '⏸️';
                    }
                });
                swReset.addEventListener('click', () => {
                    clearInterval(swInterval);
                    swInterval = null;
                    swSeconds = 0;
                    updateSwDisplay();
                    swToggle.textContent = '▶️';
                });
            }
"""
index_content = index_content.replace("// Feature 5: Reading Progress Bar", stopwatch_js + "\n            // Feature 5: Reading Progress Bar")
write_file(INDEX, index_content)
commit("feat(ui): add active study stopwatch widget")

print("All 6 commits created successfully!")
