import os
import subprocess

def run(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error running: {cmd}\n{result.stderr}")
    return result.stdout

def commit(msg):
    run('git add study_app/templates/study_app/index.html')
    run(f'git commit -m "{msg}"')

INDEX = r"c:\Users\manya\OneDrive\Desktop\notes maker\study_app\templates\study_app\index.html"

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

print("Starting Batch 16 feature injection...")

# Feature 1: Magic Marker Highlighter
index_content = read_file(INDEX)
marker_html = """
                                <button id="highlighter-btn" class="bg-pink-100 hover:bg-pink-200 dark:bg-pink-800 dark:hover:bg-pink-700 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    🖍️ Highlighter
                                </button>"""
target_focus_line = """<button id="focus-line-btn" class="bg-blue-100 hover:bg-blue-200 dark:bg-blue-800 dark:hover:bg-blue-700 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    📏 Focus Line
                                </button>"""
index_content = index_content.replace(target_focus_line, target_focus_line + marker_html)

marker_js = """
            // Feature 1: Magic Marker Highlighter
            const highlighterBtn = document.getElementById('highlighter-btn');
            let isHighlighterActive = false;
            if(highlighterBtn) {
                highlighterBtn.addEventListener('click', () => {
                    isHighlighterActive = !isHighlighterActive;
                    highlighterBtn.classList.toggle('bg-pink-500');
                    highlighterBtn.classList.toggle('text-white');
                    notesContent.style.cursor = isHighlighterActive ? 'text' : 'default';
                });
                notesContent.addEventListener('mouseup', () => {
                    if(isHighlighterActive) {
                        const selection = window.getSelection();
                        if(!selection.isCollapsed) {
                            const range = selection.getRangeAt(0);
                            const mark = document.createElement('mark');
                            mark.className = 'bg-yellow-300 dark:bg-yellow-600 rounded px-1';
                            try {
                                range.surroundContents(mark);
                            } catch(e) { console.error("Highlight crossed elements"); }
                            selection.removeAllRanges();
                        }
                    }
                });
            }
"""
target_tts = "document.getElementById('listen-notes-btn')?.addEventListener('click'"
index_content = index_content.replace(target_tts, marker_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(notes): add interactive magic marker text highlighter")


# Feature 2: Flashcard Mastery Tracker
index_content = read_file(INDEX)
mastery_ui = """
                    <div class="flex justify-between items-center mb-4">
                        <h2 class="text-xl font-semibold text-gray-800 dark:text-white flex items-center">
                            <span class="mr-2">🧠</span> Flashcards
                        </h2>
                        <div id="mastery-score" class="text-sm font-medium bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200 px-3 py-1 rounded-full">
                            Mastery: 0/0
                        </div>
                    </div>
"""
target_fc_head = """<h2 class="text-xl font-semibold text-gray-800 dark:text-white flex items-center mb-4">
                            <span class="mr-2">🧠</span> Flashcards
                        </h2>"""
index_content = index_content.replace(target_fc_head, mastery_ui)

flashcard_js_target = """<div class="absolute w-full h-full backface-hidden rotate-y-180 flex items-center justify-center p-6 bg-blue-50 dark:bg-blue-900 rounded-xl overflow-y-auto">
                                    <p class="text-lg text-center text-gray-700 dark:text-gray-200">${card.back}</p>
                                </div>"""
flashcard_js_replace = """<div class="absolute w-full h-full backface-hidden rotate-y-180 flex flex-col items-center justify-center p-6 bg-blue-50 dark:bg-blue-900 rounded-xl overflow-y-auto">
                                    <p class="text-lg text-center text-gray-700 dark:text-gray-200 mb-4">${card.back}</p>
                                    <div class="flex space-x-4 mt-auto">
                                        <button class="bg-red-100 hover:bg-red-200 text-red-800 px-3 py-1 rounded-full text-sm transition" onclick="event.stopPropagation(); updateMastery(false, this)">❌ Missed</button>
                                        <button class="bg-green-100 hover:bg-green-200 text-green-800 px-3 py-1 rounded-full text-sm transition" onclick="event.stopPropagation(); updateMastery(true, this)">✅ Knew It</button>
                                    </div>
                                </div>"""
index_content = index_content.replace(flashcard_js_target, flashcard_js_replace)

mastery_logic = """
            // Feature 2: Flashcard Mastery Tracker
            let correctCards = 0;
            let totalAttempted = 0;
            window.updateMastery = (isCorrect, btn) => {
                const buttons = btn.parentElement.querySelectorAll('button');
                buttons.forEach(b => { b.disabled = true; b.classList.add('opacity-50', 'cursor-not-allowed'); });
                totalAttempted++;
                if(isCorrect) correctCards++;
                const scoreBadge = document.getElementById('mastery-score');
                if(scoreBadge) {
                    scoreBadge.innerText = `Mastery: ${correctCards}/${totalAttempted}`;
                }
            };
"""
index_content = index_content.replace(target_tts, mastery_logic + "\n            " + target_tts)

reset_score = "flashcardsContainer.innerHTML = '';"
index_content = index_content.replace(reset_score, "correctCards = 0; totalAttempted = 0; if(document.getElementById('mastery-score')) document.getElementById('mastery-score').innerText = 'Mastery: 0/0';\n                    " + reset_score)
write_file(INDEX, index_content)
commit("feat(flashcards): implement mastery score tracking and feedback buttons")


# Feature 3: Code Snippet Copy Buttons
index_content = read_file(INDEX)

target_inv = "try { setupAccordions(); } catch(e) { console.error(\"Error in setupAccordions\", e); }"
code_copy_js = """
                    // Feature 3: Code Snippet Copy Buttons
                    const pres = notesContent.querySelectorAll('pre');
                    pres.forEach(pre => {
                        pre.style.position = 'relative';
                        const copyBtn = document.createElement('button');
                        copyBtn.className = 'absolute top-2 right-2 bg-gray-700 text-white text-xs px-2 py-1 rounded hover:bg-gray-600 transition opacity-0 group-hover:opacity-100';
                        copyBtn.innerText = '📋 Copy';
                        pre.classList.add('group');
                        copyBtn.addEventListener('click', () => {
                            navigator.clipboard.writeText(pre.innerText.replace('📋 Copy', '').trim());
                            copyBtn.innerText = '✅ Copied';
                            setTimeout(() => copyBtn.innerText = '📋 Copy', 2000);
                        });
                        pre.appendChild(copyBtn);
                    });
"""
index_content = index_content.replace(target_inv, target_inv + "\n                    try { \n" + code_copy_js + " } catch(e) { console.error(e); }")
write_file(INDEX, index_content)
commit("feat(notes): auto-inject copy to clipboard buttons on code blocks")


# Feature 4: Local Browser Draft Save
index_content = read_file(INDEX)
draft_html = """
                                <button id="save-draft-btn" class="bg-indigo-100 hover:bg-indigo-200 dark:bg-indigo-800 dark:hover:bg-indigo-700 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    💾 Save Draft
                                </button>
                                <button id="load-draft-btn" class="bg-teal-100 hover:bg-teal-200 dark:bg-teal-800 dark:hover:bg-teal-700 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2 hidden">
                                    📂 Load Draft
                                </button>"""
index_content = index_content.replace(target_focus_line, target_focus_line + draft_html)

draft_js = """
            // Feature 4: Local Browser Draft Save
            const saveDraftBtn = document.getElementById('save-draft-btn');
            const loadDraftBtn = document.getElementById('load-draft-btn');
            if(saveDraftBtn && loadDraftBtn) {
                if(localStorage.getItem('notes_draft')) {
                    loadDraftBtn.classList.remove('hidden');
                }
                saveDraftBtn.addEventListener('click', () => {
                    localStorage.setItem('notes_draft', notesContent.innerHTML);
                    saveDraftBtn.innerText = '✅ Saved';
                    loadDraftBtn.classList.remove('hidden');
                    setTimeout(() => saveDraftBtn.innerText = '💾 Save Draft', 2000);
                });
                loadDraftBtn.addEventListener('click', () => {
                    notesContent.innerHTML = localStorage.getItem('notes_draft');
                    document.getElementById('result-area').classList.remove('hidden');
                });
            }
"""
index_content = index_content.replace(target_tts, draft_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(data): add localstorage draft save and restore functionality")


# Feature 5: Dictionary Look-up on Double Click
index_content = read_file(INDEX)

dict_js = """
            // Feature 5: Dictionary Look-up on Double Click
            notesContent.addEventListener('dblclick', async (e) => {
                const selection = window.getSelection().toString().trim();
                if(selection && selection.length > 2 && selection.split(' ').length === 1) { // Single word
                    try {
                        const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${selection}`);
                        if(res.ok) {
                            const data = await res.json();
                            const def = data[0]?.meanings[0]?.definitions[0]?.definition;
                            if(def) {
                                // Create tooltip
                                const tooltip = document.createElement('div');
                                tooltip.className = 'absolute bg-gray-900 text-white text-sm p-3 rounded-lg shadow-lg z-50 max-w-xs';
                                tooltip.style.left = e.pageX + 'px';
                                tooltip.style.top = (e.pageY + 20) + 'px';
                                tooltip.innerHTML = `<strong>${selection}:</strong> ${def}`;
                                document.body.appendChild(tooltip);
                                
                                // Remove on next click
                                setTimeout(() => {
                                    document.addEventListener('click', () => tooltip.remove(), {once: true});
                                }, 100);
                            }
                        }
                    } catch(err) { console.error("Dict error", err); }
                }
            });
"""
index_content = index_content.replace(target_tts, dict_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(notes): integrate double-click dictionary definition lookups")


# Feature 6: Deep Focus Brown Noise
index_content = read_file(INDEX)
brown_html = """
                <!-- Brown Noise -->
                <button id="brown-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Deep Focus Brown Noise">
                    🟫
                </button>"""
target_chime = """<button id="chime-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="15-min Mindfulness Chime">
                    🔔
                </button>"""
index_content = index_content.replace(target_chime, target_chime + brown_html)

brown_js = """
            // Feature 6: Deep Focus Brown Noise
            const brownBtn = document.getElementById('brown-btn');
            let brownCtx, brownNoiseNode;
            let isBrownPlaying = false;
            if(brownBtn) {
                brownBtn.addEventListener('click', () => {
                    if(!isBrownPlaying) {
                        if(!brownCtx) {
                            brownCtx = new (window.AudioContext || window.webkitAudioContext)();
                            const bufferSize = 2 * brownCtx.sampleRate;
                            const noiseBuffer = brownCtx.createBuffer(1, bufferSize, brownCtx.sampleRate);
                            const output = noiseBuffer.getChannelData(0);
                            let lastOut = 0;
                            for (let i = 0; i < bufferSize; i++) {
                                const white = Math.random() * 2 - 1;
                                output[i] = (lastOut + (0.02 * white)) / 1.02;
                                lastOut = output[i];
                                output[i] *= 3.5; // Compensate for gain
                            }
                            brownNoiseNode = brownCtx.createBufferSource();
                            brownNoiseNode.buffer = noiseBuffer;
                            brownNoiseNode.loop = true;
                            
                            const gain = brownCtx.createGain();
                            gain.gain.value = 0.2;
                            brownNoiseNode.connect(gain).connect(brownCtx.destination);
                            brownNoiseNode.start(0);
                        } else {
                            brownCtx.resume();
                        }
                        isBrownPlaying = true;
                        brownBtn.classList.add('bg-orange-100', 'dark:bg-orange-900');
                    } else {
                        brownCtx.suspend();
                        isBrownPlaying = false;
                        brownBtn.classList.remove('bg-orange-100', 'dark:bg-orange-900');
                    }
                });
            }
"""
index_content = index_content.replace(target_tts, brown_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(wellness): add synthesized brown noise generator for ADHD focus")

run('git push')
print("Pushed Batch 16 to GitHub!")
