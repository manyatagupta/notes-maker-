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

print("Applying Batch 10 Features and Committing...")

# --- Feature 1: Ambient Focus Sounds (Rain) ---
index_content = read_file(INDEX)
rain_btn = """\n                <!-- Ambient Rain Sounds -->
                <button id="rain-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Ambient Rain Sounds">
                    🌧️
                </button>
                <audio id="rain-audio" loop src="https://cdn.freesound.org/previews/346/346618_6002932-lq.mp3"></audio>"""
index_content = index_content.replace('title="20-20-20 Eye Strain Timer">\n                    👁️\n                </button>', 'title="20-20-20 Eye Strain Timer">\n                    👁️\n                </button>' + rain_btn)

rain_js = """
            // Feature 1: Ambient Rain Sounds
            const rainToggle = document.getElementById('rain-toggle');
            const rainAudio = document.getElementById('rain-audio');
            let isRainPlaying = false;
            if(rainToggle && rainAudio) {
                rainAudio.volume = 0.3;
                rainToggle.addEventListener('click', () => {
                    isRainPlaying = !isRainPlaying;
                    if(isRainPlaying) {
                        rainAudio.play().catch(e => console.log('Audio play failed', e));
                        rainToggle.classList.add('bg-blue-100', 'dark:bg-blue-900');
                    } else {
                        rainAudio.pause();
                        rainToggle.classList.remove('bg-blue-100', 'dark:bg-blue-900');
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 6: 20-20-20 Timer", rain_js + "\n            // Feature 6: 20-20-20 Timer")
write_file(INDEX, index_content)
commit("feat(ui): add ambient rain sounds toggle for study focus")

# --- Feature 2: Auto Table of Contents ---
index_content = read_file(INDEX)
toc_html = """
                        <!-- Auto Table of Contents -->
                        <div id="toc-container" class="mb-6 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg hidden">
                            <h3 class="font-bold text-lg mb-2">Table of Contents</h3>
                            <ul id="toc-list" class="list-disc pl-5 space-y-1"></ul>
                        </div>
"""
index_content = index_content.replace('<div id="notes-content"', toc_html + '\n                        <div id="notes-content"')

toc_js = """
            // Feature 2: Auto Table of Contents
            const tocContainer = document.getElementById('toc-container');
            const tocList = document.getElementById('toc-list');
            if(tocContainer && tocList && notesContent) {
                const headers = notesContent.querySelectorAll('h1, h2, h3');
                tocList.innerHTML = '';
                if(headers.length > 0) {
                    headers.forEach((h, i) => {
                        if(!h.id) h.id = 'heading-' + i;
                        const li = document.createElement('li');
                        const a = document.createElement('a');
                        a.href = '#' + h.id;
                        a.textContent = h.textContent;
                        a.className = 'text-blue-600 dark:text-blue-400 hover:underline cursor-pointer';
                        a.addEventListener('click', (e) => {
                            e.preventDefault();
                            h.scrollIntoView({behavior: 'smooth'});
                        });
                        li.appendChild(a);
                        if(h.tagName === 'H3') li.classList.add('ml-4');
                        tocList.appendChild(li);
                    });
                    tocContainer.classList.remove('hidden');
                }
            }
"""
index_content = index_content.replace("// Stop active stopwatch", toc_js + "\n            // Stop active stopwatch")
write_file(INDEX, index_content)
commit("feat(notes): implement auto-generating table of contents")

# --- Feature 3: Document Stats Tracker ---
index_content = read_file(INDEX)
stats_btn = """\n                                <button id="doc-stats-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2" title="Document Stats">
                                    📊 Stats
                                </button>"""
index_content = index_content.replace('🖼️ Hide Images\n                                </button>', '🖼️ Hide Images\n                                </button>' + stats_btn)

stats_js = """
            // Feature 3: Document Stats Tracker
            const docStatsBtn = document.getElementById('doc-stats-btn');
            if(docStatsBtn) {
                docStatsBtn.addEventListener('click', () => {
                    const text = notesContent?.innerText || "";
                    const words = text.trim().split(/\\s+/).length;
                    const chars = text.length;
                    const paras = text.split(/\\n\\n+/).length;
                    alert(`Document Stats:\\n\\nWords: ${words}\\nCharacters: ${chars}\\nParagraphs: ${paras}`);
                });
            }
"""
index_content = index_content.replace("// Feature 4: Hide Images", stats_js + "\n            // Feature 4: Hide Images")
write_file(INDEX, index_content)
commit("feat(ui): add document stats (word/char count) tracker")

# --- Feature 4: Tactile Flashcard Sounds ---
index_content = read_file(INDEX)
flashcard_sound_js = """
            // Feature 4: Tactile Flashcard Sounds
            const cardFlipSound = new Audio("https://cdn.freesound.org/previews/240/240776_4107740-lq.mp3");
            document.addEventListener('click', (e) => {
                if(e.target.closest('.flashcard-inner')) {
                    cardFlipSound.currentTime = 0;
                    cardFlipSound.play().catch(e=>e);
                }
            });
"""
index_content = index_content.replace("// Feature 4: Hide Images", flashcard_sound_js + "\n            // Feature 4: Hide Images")
write_file(INDEX, index_content)
commit("feat(flashcards): add tactile audio feedback on card flip")

# --- Feature 5: Smart Hashtag Badges ---
index_content = read_file(INDEX)
hashtag_js = """
            // Feature 5: Smart Hashtag Badges
            function highlightHashtags() {
                if(!notesContent) return;
                const walker = document.createTreeWalker(notesContent, NodeFilter.SHOW_TEXT, null, false);
                const nodesToReplace = [];
                let node;
                while(node = walker.nextNode()) {
                    if(node.nodeValue.match(/#[a-zA-Z0-9_]+/)) {
                        nodesToReplace.push(node);
                    }
                }
                nodesToReplace.forEach(n => {
                    const span = document.createElement('span');
                    span.innerHTML = n.nodeValue.replace(/(#[a-zA-Z0-9_]+)/g, '<span class="bg-indigo-100 text-indigo-800 text-xs font-semibold mr-1 px-2.5 py-0.5 rounded dark:bg-indigo-900 dark:text-indigo-300">$1</span>');
                    n.parentNode.replaceChild(span, n);
                });
            }
"""
index_content = index_content.replace("// Feature 2: Auto Table of Contents", hashtag_js + "\n            // Feature 2: Auto Table of Contents")
# inject call
index_content = index_content.replace("notesContent.innerHTML = notesHtml;", "notesContent.innerHTML = notesHtml;\n                    highlightHashtags();")
write_file(INDEX, index_content)
commit("feat(notes): implement auto-formatting for hashtag badges")

# --- Feature 6: Hydration Reminder ---
index_content = read_file(INDEX)
water_timer_btn = """\n                <!-- Hydration Reminder Toggle Button -->
                <button id="water-timer-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Hydration Reminder">
                    💧
                </button>"""
index_content = index_content.replace('title="Ambient Rain Sounds">\n                    🌧️\n                </button>', 'title="Ambient Rain Sounds">\n                    🌧️\n                </button>' + water_timer_btn)

water_timer_js = """
            // Feature 6: Hydration Reminder
            const waterTimerToggle = document.getElementById('water-timer-toggle');
            let waterTimerInterval;
            let isWaterTimerActive = false;
            if(waterTimerToggle) {
                waterTimerToggle.addEventListener('click', () => {
                    isWaterTimerActive = !isWaterTimerActive;
                    if(isWaterTimerActive) {
                        waterTimerToggle.classList.add('bg-blue-100', 'dark:bg-blue-900');
                        waterTimerInterval = setInterval(() => {
                            alert("💧 Hydration Reminder! Take a moment to drink some water and stretch.");
                        }, 45 * 60 * 1000); // 45 minutes
                    } else {
                        waterTimerToggle.classList.remove('bg-blue-100', 'dark:bg-blue-900');
                        clearInterval(waterTimerInterval);
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 1: Ambient Rain Sounds", water_timer_js + "\n            // Feature 1: Ambient Rain Sounds")
write_file(INDEX, index_content)
commit("feat(ui): implement 45-minute hydration reminder timer")

run('git push')
print("All 6 commits created and pushed to GitHub successfully!")
