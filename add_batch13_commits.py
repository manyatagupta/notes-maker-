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

print("Applying Batch 13 Features and Committing...")

# --- Feature 1: Image Lightbox Zoom ---
index_content = read_file(INDEX)
lightbox_html = """
    <!-- Lightbox Container -->
    <div id="lightbox-overlay" class="fixed inset-0 z-[100] bg-black bg-opacity-90 hidden flex justify-center items-center cursor-pointer">
        <img id="lightbox-img" class="max-w-full max-h-full object-contain p-4" src="" alt="Zoomed Image">
        <button id="lightbox-close" class="absolute top-4 right-4 text-white text-3xl font-bold">&times;</button>
    </div>
"""
index_content = index_content.replace('<!-- Floating Scratchpad -->', lightbox_html + '\n    <!-- Floating Scratchpad -->')

lightbox_js = """
            // Feature 1: Image Lightbox Zoom
            const lightboxOverlay = document.getElementById('lightbox-overlay');
            const lightboxImg = document.getElementById('lightbox-img');
            if(lightboxOverlay && lightboxImg && notesContent) {
                const images = notesContent.querySelectorAll('img');
                images.forEach(img => {
                    img.classList.add('cursor-pointer', 'transition-transform', 'hover:scale-105');
                    img.addEventListener('click', () => {
                        lightboxImg.src = img.src;
                        lightboxOverlay.classList.remove('hidden');
                    });
                });
                lightboxOverlay.addEventListener('click', (e) => {
                    lightboxOverlay.classList.add('hidden');
                });
            }
"""
index_content = index_content.replace("// Feature 5: Beautiful Blockquotes", lightbox_js + "\n            // Feature 5: Beautiful Blockquotes")
write_file(INDEX, index_content)
commit("feat(notes): add click-to-zoom image lightbox overlay")

# --- Feature 2: Reverse Flashcard Deck ---
index_content = read_file(INDEX)
reverse_html = """\n                            <button id="reverse-flashcards-btn" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg items-center gap-2 text-sm shadow-sm transition ml-2 hidden">
                                🔄 Reverse Deck
                            </button>"""
index_content = index_content.replace('🔀 Shuffle Cards\n                            </button>', '🔀 Shuffle Cards\n                            </button>' + reverse_html)

reverse_js = """
            // Feature 2: Reverse Flashcard Deck
            const reverseBtn = document.getElementById('reverse-flashcards-btn');
            if(reverseBtn) {
                reverseBtn.classList.remove('hidden');
                reverseBtn.addEventListener('click', () => {
                    const fronts = flashcardsContainer.querySelectorAll('.flashcard-front p');
                    const backs = flashcardsContainer.querySelectorAll('.flashcard-back p');
                    for(let i=0; i<fronts.length; i++) {
                        const temp = fronts[i].innerHTML;
                        fronts[i].innerHTML = backs[i].innerHTML;
                        backs[i].innerHTML = temp;
                    }
                });
            }
"""
index_content = index_content.replace("shuffleBtn.classList.remove('hidden');", "shuffleBtn.classList.remove('hidden');\n                " + reverse_js)

write_file(INDEX, index_content)
commit("feat(flashcards): add reverse deck functionality to swap q&a")

# --- Feature 3: Smart Scroll Memory ---
index_content = read_file(INDEX)
scroll_js = """
            // Feature 3: Smart Scroll Memory
            window.addEventListener('beforeunload', () => {
                if(typeof currentMaterialId !== 'undefined' && currentMaterialId) {
                    localStorage.setItem('scrollPos_' + currentMaterialId, window.scrollY);
                }
            });
"""
index_content = index_content.replace("// Feature 1: Image Lightbox Zoom", scroll_js + "\n            // Feature 1: Image Lightbox Zoom")
# and in populate results
scroll_restore_js = """
                // Restore scroll
                if(data.material_id) {
                    const savedScroll = localStorage.getItem('scrollPos_' + data.material_id);
                    if(savedScroll) {
                        setTimeout(() => window.scrollTo({top: parseInt(savedScroll), behavior: 'smooth'}), 300);
                    }
                }
"""
index_content = index_content.replace("function populateResults(data) {", "function populateResults(data) {\n" + scroll_restore_js)
write_file(INDEX, index_content)
commit("feat(ui): remember and restore reading scroll position per document")

# --- Feature 4: TTS Voice Selector Dropdown ---
index_content = read_file(INDEX)
voice_select_html = """\n                                <select id="tts-voice-select" class="ml-2 text-xs border border-gray-300 rounded max-w-[100px]"></select>"""
index_content = index_content.replace('title="Speech Speed">1.0x</button>', 'title="Speech Speed">1.0x</button>' + voice_select_html)

voice_js = """
            // Feature 4: TTS Voice Selector
            const voiceSelect = document.getElementById('tts-voice-select');
            let systemVoices = [];
            function populateVoices() {
                systemVoices = speechSynthesis.getVoices();
                if(voiceSelect) {
                    voiceSelect.innerHTML = systemVoices.map((v, i) => `<option value="${i}">${v.name.substring(0,10)}...</option>`).join('');
                }
            }
            populateVoices();
            if (speechSynthesis.onvoiceschanged !== undefined) {
                speechSynthesis.onvoiceschanged = populateVoices;
            }
            const originalSpeak = speechSynthesis.speak;
            speechSynthesis.speak = function(utterance) {
                if(voiceSelect && systemVoices.length > 0) {
                    utterance.voice = systemVoices[voiceSelect.value];
                }
                originalSpeak.call(speechSynthesis, utterance);
            };
"""
index_content = index_content.replace("// Feature 3: Smart Scroll Memory", voice_js + "\n            // Feature 3: Smart Scroll Memory")
write_file(INDEX, index_content)
commit("feat(ui): add voice selector dropdown for text-to-speech")

# --- Feature 5: Shortcuts Cheat Sheet Modal ---
index_content = read_file(INDEX)
cheat_btn = """\n                <button id="cheat-sheet-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Keyboard Shortcuts">
                    ⌨️
                </button>"""
index_content = index_content.replace('title="Celebrate!">', 'title="Celebrate!">\n                </button>' + cheat_btn)

cheat_modal = """
    <!-- Cheat Sheet Modal -->
    <div id="cheat-sheet-modal" class="fixed inset-0 z-[110] bg-black bg-opacity-50 hidden flex justify-center items-center">
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-md w-full shadow-2xl">
            <h2 class="text-2xl font-bold mb-4">Keyboard Shortcuts</h2>
            <ul class="space-y-3">
                <li class="flex justify-between"><span>Quick Highlight</span> <kbd class="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded text-sm">Alt + Double Click</kbd></li>
                <li class="flex justify-between"><span>Dictionary Tooltip</span> <kbd class="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded text-sm">Double Click</kbd></li>
                <li class="flex justify-between"><span>Google Search</span> <kbd class="px-2 py-1 bg-gray-100 dark:bg-gray-700 rounded text-sm">Select Text</kbd></li>
            </ul>
            <button id="close-cheat-sheet" class="mt-6 w-full bg-blue-600 text-white rounded py-2 font-semibold hover:bg-blue-700">Got it!</button>
        </div>
    </div>
"""
index_content = index_content.replace('<!-- Lightbox Container -->', cheat_modal + '\n    <!-- Lightbox Container -->')

cheat_js = """
            // Feature 5: Cheat Sheet Modal
            const cheatBtn = document.getElementById('cheat-sheet-btn');
            const cheatModal = document.getElementById('cheat-sheet-modal');
            const closeCheat = document.getElementById('close-cheat-sheet');
            if(cheatBtn && cheatModal) {
                cheatBtn.addEventListener('click', () => cheatModal.classList.remove('hidden'));
                closeCheat.addEventListener('click', () => cheatModal.classList.add('hidden'));
            }
"""
index_content = index_content.replace("// Feature 4: TTS Voice Selector", cheat_js + "\n            // Feature 4: TTS Voice Selector")
write_file(INDEX, index_content)
commit("feat(ui): add keyboard shortcuts cheat sheet modal")

# --- Feature 6: Zen Focus Mode ---
index_content = read_file(INDEX)
zen_btn = """\n                <button id="zen-mode-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Zen Focus Mode">
                    🧘
                </button>"""
index_content = index_content.replace('title="Keyboard Shortcuts">\n                    ⌨️\n                </button>', 'title="Keyboard Shortcuts">\n                    ⌨️\n                </button>' + zen_btn)

zen_js = """
            // Feature 6: Zen Focus Mode
            const zenBtn = document.getElementById('zen-mode-btn');
            let isZen = false;
            if(zenBtn) {
                zenBtn.addEventListener('click', () => {
                    isZen = !isZen;
                    const nav = document.querySelector('nav');
                    const sidebar = document.getElementById('sidebar');
                    const floatingEls = document.querySelectorAll('.fixed:not(#lightbox-overlay)');
                    
                    if(isZen) {
                        if(nav) nav.classList.add('hidden');
                        if(sidebar) sidebar.classList.add('hidden');
                        floatingEls.forEach(el => el.classList.add('hidden'));
                        
                        const exitZen = document.createElement('button');
                        exitZen.id = 'exit-zen-btn';
                        exitZen.innerHTML = 'Exit Zen 🧘';
                        exitZen.className = 'fixed top-4 right-4 z-[200] bg-gray-800 text-white px-4 py-2 rounded-full opacity-50 hover:opacity-100';
                        exitZen.onclick = () => zenBtn.click();
                        document.body.appendChild(exitZen);
                    } else {
                        if(nav) nav.classList.remove('hidden');
                        if(sidebar) sidebar.classList.remove('hidden');
                        floatingEls.forEach(el => el.classList.remove('hidden'));
                        const exitZen = document.getElementById('exit-zen-btn');
                        if(exitZen) exitZen.remove();
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 5: Cheat Sheet Modal", zen_js + "\n            // Feature 5: Cheat Sheet Modal")
write_file(INDEX, index_content)
commit("feat(ui): implement zen mode for distraction-free reading")

run('git push')
print("All 6 commits created and pushed to GitHub successfully!")
