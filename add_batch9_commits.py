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

print("Applying Batch 9 Features and Committing...")

# --- Feature 1: Highlighter Pen Tool ---
index_content = read_file(INDEX)
highlight_btn = """\n                                <button id="highlight-btn" class="bg-yellow-200 hover:bg-yellow-300 dark:bg-yellow-700 dark:hover:bg-yellow-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    🖍️ Highlight
                                </button>"""
index_content = index_content.replace('📋 Copy\n                                </button>', '📋 Copy\n                                </button>' + highlight_btn)

highlight_js = """
            // Feature 1: Highlighter Tool
            const highlightBtn = document.getElementById('highlight-btn');
            if(highlightBtn) {
                highlightBtn.addEventListener('click', () => {
                    const selection = window.getSelection();
                    if(!selection.rangeCount || selection.toString().length === 0) return;
                    const range = selection.getRangeAt(0);
                    const mark = document.createElement('mark');
                    mark.className = 'bg-yellow-300 dark:bg-yellow-600';
                    range.surroundContents(mark);
                    selection.removeAllRanges();
                });
            }
"""
index_content = index_content.replace("// Feature 3: Keyboard Shortcuts", highlight_js + "\n            // Feature 3: Keyboard Shortcuts")
write_file(INDEX, index_content)
commit("feat(notes): add interactive highlighter pen tool")

# --- Feature 2: Flashcard Shuffle Button ---
index_content = read_file(INDEX)
shuffle_btn = """\n                            <button id="shuffle-flashcards-btn" class="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg items-center gap-2 text-sm shadow-sm transition ml-2 hidden">
                                🔀 Shuffle Cards
                            </button>"""
index_content = index_content.replace('🖨️ Print Flashcards\n                            </button>', '🖨️ Print Flashcards\n                            </button>' + shuffle_btn)

shuffle_js = """
            // Feature 2: Flashcard Shuffle
            const shuffleBtn = document.getElementById('shuffle-flashcards-btn');
            if(shuffleBtn) {
                shuffleBtn.addEventListener('click', () => {
                    const container = document.getElementById('flashcards-container');
                    if(!container) return;
                    const cards = Array.from(container.children);
                    cards.sort(() => Math.random() - 0.5);
                    cards.forEach(card => container.appendChild(card));
                });
            }
"""
index_content = index_content.replace("// Feature 3: Keyboard Shortcuts", shuffle_js + "\n            // Feature 3: Keyboard Shortcuts")
index_content = index_content.replace("document.getElementById('print-flashcards-btn')?.classList.remove('hidden');", "document.getElementById('print-flashcards-btn')?.classList.remove('hidden');\n                    document.getElementById('shuffle-flashcards-btn')?.classList.remove('hidden');")
write_file(INDEX, index_content)
commit("feat(flashcards): add shuffle flashcards functionality for varied testing")

# --- Feature 3: Text-to-Speech Speed Control ---
index_content = read_file(INDEX)
speed_btn = """\n                                <button id="speed-toggle-btn" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-2 py-1 text-sm font-bold border border-gray-300 dark:border-gray-600 rounded ml-1 bg-white dark:bg-gray-800" title="Speech Speed">1.0x</button>"""
index_content = index_content.replace('🔊 Listen\n                                </button>', '🔊 Listen\n                                </button>' + speed_btn)

speed_js = """
            // Feature 3: TTS Speed Control
            const speedToggle = document.getElementById('speed-toggle-btn');
            let ttsSpeed = 1.0;
            if(speedToggle) {
                speedToggle.addEventListener('click', () => {
                    if(ttsSpeed === 1.0) ttsSpeed = 1.5;
                    else if(ttsSpeed === 1.5) ttsSpeed = 2.0;
                    else ttsSpeed = 1.0;
                    speedToggle.textContent = ttsSpeed.toFixed(1) + 'x';
                    if (window.speechSynthesis.speaking) {
                        window.speechSynthesis.cancel();
                        document.getElementById('listen-notes-btn')?.click(); 
                    }
                });
            }
"""
index_content = index_content.replace("// Text to Speech Logic", speed_js + "\n            // Text to Speech Logic")
# We need to inject ttsSpeed into the actual Text to Speech Logic
index_content = index_content.replace("utterance = new SpeechSynthesisUtterance(textToRead);", "utterance = new SpeechSynthesisUtterance(textToRead);\n                    utterance.rate = ttsSpeed;")
write_file(INDEX, index_content)
commit("feat(ui): add playback speed control for text-to-speech")

# --- Feature 4: Hide/Show Images Toggle ---
index_content = read_file(INDEX)
hide_img_btn = """\n                                <button id="hide-img-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2" title="Toggle Images">
                                    🖼️ Hide Images
                                </button>"""
index_content = index_content.replace('🔦 Focus Mask\n                                </button>', '🔦 Focus Mask\n                                </button>' + hide_img_btn)

hide_img_js = """
            // Feature 4: Hide Images
            const hideImgBtn = document.getElementById('hide-img-btn');
            let imagesHidden = false;
            if(hideImgBtn) {
                hideImgBtn.addEventListener('click', () => {
                    imagesHidden = !imagesHidden;
                    const styleId = 'hide-img-style';
                    if(imagesHidden) {
                        const style = document.createElement('style');
                        style.id = styleId;
                        style.innerHTML = '#notes-content img, #summary-content img { display: none !important; }';
                        document.head.appendChild(style);
                        hideImgBtn.textContent = '🖼️ Show Images';
                        hideImgBtn.classList.add('bg-blue-200', 'dark:bg-blue-800');
                    } else {
                        document.getElementById(styleId)?.remove();
                        hideImgBtn.textContent = '🖼️ Hide Images';
                        hideImgBtn.classList.remove('bg-blue-200', 'dark:bg-blue-800');
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 3: Keyboard Shortcuts", hide_img_js + "\n            // Feature 3: Keyboard Shortcuts")
write_file(INDEX, index_content)
commit("feat(notes): implement toggle to hide/show images for distraction-free reading")

# --- Feature 5: Spaced Repetition Counter (Read Tracker) ---
index_content = read_file(INDEX)
read_tracker_html = """
                            <div class="mt-6 pt-4 border-t border-gray-200 dark:border-gray-700 flex justify-between items-center text-sm text-gray-500">
                                <div class="flex items-center gap-2">
                                    <span>Times Read: <span id="read-count">0</span></span>
                                    <button id="add-read-btn" class="bg-green-100 dark:bg-green-900 hover:bg-green-200 dark:hover:bg-green-800 text-green-700 dark:text-green-300 px-2 rounded transition">+</button>
                                </div>
                            </div>
"""
index_content = index_content.replace('</div>\n                        </div>\n\n                        <!-- Flashcards Tab -->', read_tracker_html + '                        </div>\n                        </div>\n\n                        <!-- Flashcards Tab -->')

read_tracker_js = """
            // Feature 5: Read Tracker
            const addReadBtn = document.getElementById('add-read-btn');
            const readCountSpan = document.getElementById('read-count');
            let readCount = 0;
            if(addReadBtn && readCountSpan) {
                addReadBtn.addEventListener('click', () => {
                    readCount++;
                    readCountSpan.textContent = readCount;
                });
            }
"""
index_content = index_content.replace("// Feature 3: Keyboard Shortcuts", read_tracker_js + "\n            // Feature 3: Keyboard Shortcuts")
write_file(INDEX, index_content)
commit("feat(ui): add manual read counter to track spaced repetition")

# --- Feature 6: 20-20-20 Eye Strain Timer ---
index_content = read_file(INDEX)
eye_timer_btn = """\n                <!-- 20-20-20 Timer Toggle Button -->
                <button id="eye-timer-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="20-20-20 Eye Strain Timer">
                    👁️
                </button>"""
index_content = index_content.replace('title="High Contrast Mode">\n                    🌗\n                </button>', 'title="High Contrast Mode">\n                    🌗\n                </button>' + eye_timer_btn)

eye_timer_js = """
            // Feature 6: 20-20-20 Timer
            const eyeTimerToggle = document.getElementById('eye-timer-toggle');
            let eyeTimerInterval;
            let isEyeTimerActive = false;
            if(eyeTimerToggle) {
                eyeTimerToggle.addEventListener('click', () => {
                    isEyeTimerActive = !isEyeTimerActive;
                    if(isEyeTimerActive) {
                        eyeTimerToggle.classList.add('bg-green-100', 'dark:bg-green-900');
                        eyeTimerInterval = setInterval(() => {
                            alert("👁️ 20-20-20 Rule! Look at something 20 feet away for 20 seconds to rest your eyes.");
                        }, 20 * 60 * 1000); // 20 minutes
                    } else {
                        eyeTimerToggle.classList.remove('bg-green-100', 'dark:bg-green-900');
                        clearInterval(eyeTimerInterval);
                    }
                });
            }
"""
index_content = index_content.replace("// Theme Toggle Logic", eye_timer_js + "\n                // Theme Toggle Logic")
write_file(INDEX, index_content)
commit("feat(ui): implement 20-20-20 eye strain prevention timer")

run('git push')
print("All 6 commits created and pushed to GitHub successfully!")
