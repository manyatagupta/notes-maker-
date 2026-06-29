import os
import subprocess

INDEX = r"c:\Users\manya\OneDrive\Desktop\notes maker\study_app\templates\study_app\index.html"

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
    run(f'git commit -m "{message}"')

# Ensure clean slate for INDEX
run('git checkout -- "' + INDEX + '"')

print("Applying Batch 11 Features and Committing...")

# --- Feature 1: Sticky Toolkit Navigation ---
index_content = read_file(INDEX)
index_content = index_content.replace('<nav class="bg-white dark:bg-gray-800 shadow-sm py-4 no-print transition-colors duration-200">', '<nav class="bg-white dark:bg-gray-800 shadow-sm py-4 no-print transition-colors duration-200 sticky top-0 z-50">')
write_file(INDEX, index_content)
commit("feat(ui): make toolkit navigation sticky for easier access")

# --- Feature 2: Floating Scratchpad ---
index_content = read_file(INDEX)
scratchpad_html = """
    <!-- Floating Scratchpad -->
    <div id="scratchpad-container" class="fixed bottom-4 left-4 z-50 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 w-64 transition-transform transform translate-y-[calc(100%-40px)] no-print">
        <div id="scratchpad-header" class="flex justify-between items-center p-2 bg-gray-100 dark:bg-gray-700 rounded-t-lg cursor-pointer">
            <span class="font-semibold text-sm">📝 Scratchpad</span>
            <span id="scratchpad-toggle-icon">▲</span>
        </div>
        <textarea id="scratchpad-text" class="w-full h-40 p-2 text-sm bg-transparent border-none focus:ring-0 resize-none dark:text-white" placeholder="Type quick notes here..."></textarea>
    </div>
"""
# inject right before </body>
index_content = index_content.replace('</body>', scratchpad_html + '\n</body>')

scratchpad_js = """
            // Feature 2: Floating Scratchpad
            const scratchpadContainer = document.getElementById('scratchpad-container');
            const scratchpadHeader = document.getElementById('scratchpad-header');
            const scratchpadIcon = document.getElementById('scratchpad-toggle-icon');
            const scratchpadText = document.getElementById('scratchpad-text');
            let isScratchpadOpen = false;

            if (scratchpadHeader && scratchpadText) {
                const savedNotes = localStorage.getItem('study_scratchpad');
                if(savedNotes) scratchpadText.value = savedNotes;

                scratchpadText.addEventListener('input', () => {
                    localStorage.setItem('study_scratchpad', scratchpadText.value);
                });

                scratchpadHeader.addEventListener('click', () => {
                    isScratchpadOpen = !isScratchpadOpen;
                    if(isScratchpadOpen) {
                        scratchpadContainer.classList.remove('translate-y-[calc(100%-40px)]');
                        scratchpadIcon.textContent = '▼';
                    } else {
                        scratchpadContainer.classList.add('translate-y-[calc(100%-40px)]');
                        scratchpadIcon.textContent = '▲';
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 6: Hydration Reminder", scratchpad_js + "\n            // Feature 6: Hydration Reminder")
write_file(INDEX, index_content)
commit("feat(notes): add floating scratchpad with local storage")

# --- Feature 3: Live Study Clock ---
index_content = read_file(INDEX)
clock_html = """\n                <span id="live-clock" class="ml-4 font-mono text-gray-500 dark:text-gray-400 font-bold hidden md:inline-block" title="Current Time">--:--</span>"""
index_content = index_content.replace('title="Hydration Reminder">\n                    💧\n                </button>', 'title="Hydration Reminder">\n                    💧\n                </button>' + clock_html)

clock_js = """
            // Feature 3: Live Study Clock
            const liveClock = document.getElementById('live-clock');
            if (liveClock) {
                setInterval(() => {
                    const now = new Date();
                    liveClock.textContent = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
                }, 1000);
            }
"""
index_content = index_content.replace("// Feature 2: Floating Scratchpad", clock_js + "\n            // Feature 2: Floating Scratchpad")
write_file(INDEX, index_content)
commit("feat(ui): add live digital clock to navigation bar")

# --- Feature 4: Color Tint Themes ---
index_content = read_file(INDEX)
theme_btn_html = """\n                <!-- Theme Cycler -->
                <button id="theme-cycler-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Cycle Theme Colors">
                    🎨
                </button>"""
index_content = index_content.replace('title="Ambient Rain Sounds">\n                    🌧️\n                </button>', 'title="Ambient Rain Sounds">\n                    🌧️\n                </button>' + theme_btn_html)

theme_js = """
            // Feature 4: Color Tint Themes
            const themeCyclerBtn = document.getElementById('theme-cycler-btn');
            const themes = ['bg-white dark:bg-gray-900', 'bg-green-50 dark:bg-green-900', 'bg-purple-50 dark:bg-purple-900', 'bg-orange-50 dark:bg-orange-900'];
            let currentThemeIndex = 0;
            if(themeCyclerBtn) {
                themeCyclerBtn.addEventListener('click', () => {
                    // document.body might not have these classes initially, so we just remove all possible
                    themes.forEach(t => t.split(' ').forEach(cls => document.body.classList.remove(cls)));
                    currentThemeIndex = (currentThemeIndex + 1) % themes.length;
                    themes[currentThemeIndex].split(' ').forEach(cls => document.body.classList.add(cls));
                });
            }
"""
index_content = index_content.replace("// Feature 3: Live Study Clock", theme_js + "\n            // Feature 3: Live Study Clock")
write_file(INDEX, index_content)
commit("feat(ui): add color tint theme cycler to personalize study area")

# --- Feature 5: Alt-Click Quick Highlight ---
index_content = read_file(INDEX)
alt_click_js = """
            // Feature 5: Alt-Click Quick Highlight
            document.addEventListener('dblclick', (e) => {
                if(e.altKey) {
                    const selection = window.getSelection();
                    if(selection.rangeCount > 0 && !selection.isCollapsed) {
                        const range = selection.getRangeAt(0);
                        const mark = document.createElement('mark');
                        mark.className = 'bg-green-200 dark:bg-green-800 text-inherit rounded px-1';
                        try {
                            range.surroundContents(mark);
                            selection.removeAllRanges();
                        } catch(err) {
                            console.log("Could not highlight selection across elements.");
                        }
                    }
                }
            });
"""
index_content = index_content.replace("// Feature 4: Color Tint Themes", alt_click_js + "\n            // Feature 4: Color Tint Themes")
write_file(INDEX, index_content)
commit("feat(notes): implement alt-double-click quick highlighting shortcut")

run('git push')
print("All 5 commits created and pushed to GitHub successfully!")
