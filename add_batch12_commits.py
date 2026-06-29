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

print("Applying Batch 12 Features and Committing...")

# --- Feature 1: Pomodoro Focus Timer ---
index_content = read_file(INDEX)
pomodoro_btn = """\n                <button id="pomodoro-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2 font-mono font-bold" title="Pomodoro Timer">
                    🍅 25:00
                </button>"""
index_content = index_content.replace('title="Current Time">--:--</span>', 'title="Current Time">--:--</span>' + pomodoro_btn)

pomodoro_js = """
            // Feature 1: Pomodoro Timer
            const pomodoroBtn = document.getElementById('pomodoro-btn');
            let pomodoroInterval;
            let pomodoroTime = 25 * 60;
            let isPomodoroRunning = false;
            if(pomodoroBtn) {
                pomodoroBtn.addEventListener('click', () => {
                    if(isPomodoroRunning) {
                        clearInterval(pomodoroInterval);
                        isPomodoroRunning = false;
                        pomodoroTime = 25 * 60;
                        pomodoroBtn.textContent = '🍅 25:00';
                        pomodoroBtn.classList.remove('text-red-500', 'bg-red-50');
                    } else {
                        isPomodoroRunning = true;
                        pomodoroBtn.classList.add('text-red-500', 'bg-red-50');
                        pomodoroInterval = setInterval(() => {
                            pomodoroTime--;
                            let m = Math.floor(pomodoroTime / 60).toString().padStart(2, '0');
                            let s = (pomodoroTime % 60).toString().padStart(2, '0');
                            pomodoroBtn.textContent = `🍅 ${m}:${s}`;
                            if(pomodoroTime <= 0) {
                                clearInterval(pomodoroInterval);
                                alert("🍅 Pomodoro finished! Take a 5 minute break.");
                                isPomodoroRunning = false;
                                pomodoroTime = 25 * 60;
                                pomodoroBtn.textContent = '🍅 25:00';
                                pomodoroBtn.classList.remove('text-red-500', 'bg-red-50');
                            }
                        }, 1000);
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 5: Alt-Click Quick Highlight", pomodoro_js + "\n            // Feature 5: Alt-Click Quick Highlight")
write_file(INDEX, index_content)
commit("feat(ui): implement pomodoro productivity timer in navbar")

# --- Feature 2: Scroll Progress Bar ---
index_content = read_file(INDEX)
progress_html = """\n    <div id="scroll-progress" class="fixed top-0 left-0 h-1 bg-blue-500 z-[60] w-0 transition-all duration-150"></div>"""
index_content = index_content.replace('<body class="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen font-sans transition-colors duration-200">', '<body class="bg-gray-50 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen font-sans transition-colors duration-200">' + progress_html)

progress_js = """
            // Feature 2: Scroll Progress Bar
            const scrollProgress = document.getElementById('scroll-progress');
            if(scrollProgress) {
                window.addEventListener('scroll', () => {
                    const scrollTop = window.scrollY;
                    const docHeight = document.body.scrollHeight - window.innerHeight;
                    const scrollPercent = scrollTop / docHeight;
                    scrollProgress.style.width = Math.min(100, Math.max(0, scrollPercent * 100)) + '%';
                });
            }
"""
index_content = index_content.replace("// Feature 1: Pomodoro Timer", progress_js + "\n            // Feature 1: Pomodoro Timer")
write_file(INDEX, index_content)
commit("feat(ui): add reading scroll progress bar to top of window")

# --- Feature 3: Clickable Task Checklists ---
index_content = read_file(INDEX)
checklist_js = """
            // Feature 3: Clickable Task Checklists
            function convertChecklists() {
                if(!notesContent) return;
                const walker = document.createTreeWalker(notesContent, NodeFilter.SHOW_TEXT, null, false);
                const nodesToReplace = [];
                let node;
                while(node = walker.nextNode()) {
                    if(node.nodeValue.match(/- \\[( |x)\\]/i)) {
                        nodesToReplace.push(node);
                    }
                }
                nodesToReplace.forEach(n => {
                    const span = document.createElement('span');
                    span.innerHTML = n.nodeValue
                        .replace(/- \\[ \\]/g, '<input type="checkbox" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600 cursor-pointer mr-2">')
                        .replace(/- \\[x\\]/gi, '<input type="checkbox" checked class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600 cursor-pointer mr-2">');
                    n.parentNode.replaceChild(span, n);
                });
            }
"""
index_content = index_content.replace("function highlightHashtags() {", checklist_js + "\n            function highlightHashtags() {")
index_content = index_content.replace("highlightHashtags();", "highlightHashtags();\n                    convertChecklists();")
write_file(INDEX, index_content)
commit("feat(notes): convert markdown checkboxes to interactive html inputs")

# --- Feature 4: Floating Quick Search ---
index_content = read_file(INDEX)
search_html = """
    <!-- Floating Quick Search -->
    <button id="quick-search-btn" class="fixed hidden z-50 bg-white dark:bg-gray-800 shadow-lg rounded-full p-2 border border-gray-200 dark:border-gray-700 hover:bg-gray-50 transition-transform transform hover:scale-110 text-xl" title="Search Google">
        🔍
    </button>
"""
index_content = index_content.replace('<!-- Floating Scratchpad -->', search_html + '\n    <!-- Floating Scratchpad -->')

search_js = """
            // Feature 4: Floating Quick Search
            const quickSearchBtn = document.getElementById('quick-search-btn');
            if(quickSearchBtn) {
                document.addEventListener('selectionchange', () => {
                    const selection = window.getSelection();
                    if(selection.rangeCount > 0 && !selection.isCollapsed && selection.toString().trim().length > 0) {
                        const range = selection.getRangeAt(0).getBoundingClientRect();
                        quickSearchBtn.style.left = `${range.left + (range.width / 2) - 20}px`;
                        quickSearchBtn.style.top = `${range.top + window.scrollY - 55}px`;
                        quickSearchBtn.classList.remove('hidden');
                        
                        quickSearchBtn.onclick = () => {
                            window.open(`https://www.google.com/search?q=${encodeURIComponent(selection.toString().trim())}`, '_blank');
                        };
                    } else {
                        quickSearchBtn.classList.add('hidden');
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 2: Scroll Progress Bar", search_js + "\n            // Feature 2: Scroll Progress Bar")
write_file(INDEX, index_content)
commit("feat(notes): add floating quick search button for selected text")

# --- Feature 5: Beautiful Blockquotes ---
index_content = read_file(INDEX)
blockquote_js = """
            // Feature 5: Beautiful Blockquotes
            function styleBlockquotes() {
                if(!notesContent) return;
                const bqs = notesContent.querySelectorAll('blockquote');
                bqs.forEach(bq => {
                    bq.className = 'p-4 my-4 border-s-4 border-blue-500 bg-blue-50 dark:bg-gray-800 dark:border-blue-600 italic text-gray-700 dark:text-gray-300 rounded-r-lg';
                });
                
                const walker = document.createTreeWalker(notesContent, NodeFilter.SHOW_TEXT, null, false);
                const nodesToReplace = [];
                let node;
                while(node = walker.nextNode()) {
                    if(node.nodeValue.trim().startsWith('> ')) {
                        nodesToReplace.push(node);
                    }
                }
                nodesToReplace.forEach(n => {
                    const div = document.createElement('div');
                    div.className = 'p-4 my-4 border-s-4 border-blue-500 bg-blue-50 dark:bg-gray-800 dark:border-blue-600 italic text-gray-700 dark:text-gray-300 rounded-r-lg';
                    div.textContent = n.nodeValue.replace(/^>\\s*/, '');
                    n.parentNode.replaceChild(div, n);
                });
            }
"""
index_content = index_content.replace("function highlightHashtags() {", blockquote_js + "\n            function highlightHashtags() {")
index_content = index_content.replace("convertChecklists();", "convertChecklists();\n                    styleBlockquotes();")
write_file(INDEX, index_content)
commit("feat(notes): style blockquotes with modern distinctive ui")

# --- Feature 6: Motivation Confetti Burst ---
index_content = read_file(INDEX)
confetti_btn = """\n                <button id="confetti-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Celebrate!">
                    🎉
                </button>"""
index_content = index_content.replace('title="Cycle Theme Colors">\n                    🎨\n                </button>', 'title="Cycle Theme Colors">\n                    🎨\n                </button>' + confetti_btn)

confetti_js = """
            // Feature 6: Motivation Confetti Burst
            const confettiBtn = document.getElementById('confetti-btn');
            if(confettiBtn) {
                confettiBtn.addEventListener('click', () => {
                    for(let i=0; i<50; i++) {
                        const conf = document.createElement('div');
                        conf.style.position = 'fixed';
                        conf.style.width = '10px';
                        conf.style.height = '10px';
                        conf.style.backgroundColor = ['#ef4444', '#3b82f6', '#10b981', '#f59e0b', '#8b5cf6'][Math.floor(Math.random()*5)];
                        conf.style.left = Math.random() * 100 + 'vw';
                        conf.style.top = '-10px';
                        conf.style.zIndex = '9999';
                        conf.style.transition = 'transform 3s linear, top 3s linear';
                        document.body.appendChild(conf);
                        
                        setTimeout(() => {
                            conf.style.top = '100vh';
                            conf.style.transform = `rotate(${Math.random() * 360 * 3}deg)`;
                        }, 50);
                        
                        setTimeout(() => conf.remove(), 3000);
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 4: Floating Quick Search", confetti_js + "\n            // Feature 4: Floating Quick Search")
write_file(INDEX, index_content)
commit("feat(ui): add motivation confetti burst effect on button click")

run('git push')
print("All 6 commits created and pushed to GitHub successfully!")
