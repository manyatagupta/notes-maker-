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

# Start clean
# run('git checkout -- "' + INDEX + '"')

print("Starting Batch 14 feature injection...")

# Feature 1: TTS Speed Controller Logic
index_content = read_file(INDEX)
speed_js = """
            // Feature 1: TTS Speed Controller Logic
            const speedToggleBtn = document.getElementById('speed-toggle-btn');
            const speeds = [0.75, 1.0, 1.5, 2.0];
            let currentSpeedIndex = 1;
            if(speedToggleBtn) {
                speedToggleBtn.addEventListener('click', () => {
                    currentSpeedIndex = (currentSpeedIndex + 1) % speeds.length;
                    const speed = speeds[currentSpeedIndex];
                    speedToggleBtn.innerText = speed + 'x';
                    if (currentUtterance) {
                        currentUtterance.rate = speed;
                    }
                });
            }
"""
target_tts = "document.getElementById('listen-notes-btn')?.addEventListener('click'"
index_content = index_content.replace(target_tts, speed_js + "\n            " + target_tts)
target_speak = "currentUtterance = new SpeechSynthesisUtterance(cleanText);"
index_content = index_content.replace(target_speak, target_speak + "\n                currentUtterance.rate = typeof currentSpeedIndex !== 'undefined' ? speeds[currentSpeedIndex] : 1.0;")
write_file(INDEX, index_content)
commit("feat(tts): implement cycling speed controller for text-to-speech")

# Feature 2: Active Recall Blur
index_content = read_file(INDEX)
blur_html = """
                                <button id="blur-toggle-btn" class="bg-indigo-200 hover:bg-indigo-300 dark:bg-indigo-700 dark:hover:bg-indigo-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    🌫️ Blur Mode
                                </button>"""
target_focus = """<button id="focus-mask-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    🔦 Focus Mask
                                </button>"""
index_content = index_content.replace(target_focus, target_focus + blur_html)

blur_css = """
        .blur-mode p, .blur-mode li { filter: blur(5px); transition: filter 0.3s; cursor: pointer; }
        .blur-mode p:hover, .blur-mode li:hover { filter: blur(0); }
"""
target_css = "/* Flashcard Animations */"
index_content = index_content.replace(target_css, blur_css + "\n        " + target_css)

blur_js = """
            // Feature 2: Active Recall Blur Mode
            const blurToggleBtn = document.getElementById('blur-toggle-btn');
            if(blurToggleBtn) {
                blurToggleBtn.addEventListener('click', () => {
                    notesContent.classList.toggle('blur-mode');
                    blurToggleBtn.classList.toggle('bg-indigo-500');
                    blurToggleBtn.classList.toggle('text-white');
                });
            }
"""
index_content = index_content.replace(target_tts, blur_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(notes): add active recall blur toggle for self-testing")


# Feature 3: Auto-Keyword Scanner
index_content = read_file(INDEX)
keyword_html = """
                                <button id="keyword-scanner-btn" class="bg-yellow-100 hover:bg-yellow-200 dark:bg-yellow-800 dark:hover:bg-yellow-700 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    🔍 Scan Keywords
                                </button>"""
index_content = index_content.replace(target_focus, target_focus + keyword_html)

keyword_js = """
            // Feature 3: Auto-Keyword Scanner
            const keywordScannerBtn = document.getElementById('keyword-scanner-btn');
            if(keywordScannerBtn) {
                keywordScannerBtn.addEventListener('click', () => {
                    if(!notesContent) return;
                    const walker = document.createTreeWalker(notesContent, NodeFilter.SHOW_TEXT, null, false);
                    const nodes = [];
                    let node;
                    while(node = walker.nextNode()) nodes.push(node);
                    
                    nodes.forEach(n => {
                        if (n.parentNode.nodeName === 'SPAN' && n.parentNode.classList.contains('bg-yellow-200')) return; // Already highlighted
                        if (n.nodeValue.trim() === '') return;
                        
                        const regex = /\\b([A-Z][a-z]{3,}|\\d{2,4})\\b/g;
                        if(n.nodeValue.match(regex)) {
                            const span = document.createElement('span');
                            span.innerHTML = n.nodeValue.replace(regex, '<span class="bg-yellow-200 dark:bg-yellow-700 font-medium px-1 rounded">$1</span>');
                            n.parentNode.replaceChild(span, n);
                        }
                    });
                });
            }
"""
index_content = index_content.replace(target_tts, keyword_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(notes): auto-highlight dates and proper nouns with keyword scanner")


# Feature 4: Clean Print Notes Mode
index_content = read_file(INDEX)
print_html = """
                                <button id="print-notes-btn" class="bg-green-100 hover:bg-green-200 dark:bg-green-800 dark:hover:bg-green-700 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    🖨️ Print PDF
                                </button>"""
index_content = index_content.replace(target_focus, target_focus + print_html)

print_js = """
            // Feature 4: Clean Print Notes Mode
            const printNotesBtn = document.getElementById('print-notes-btn');
            if(printNotesBtn) {
                printNotesBtn.addEventListener('click', () => {
                    document.getElementById('sidebar')?.classList.add('no-print');
                    window.print();
                });
            }
"""
index_content = index_content.replace(target_tts, print_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(ui): add clean print export button for generated notes")


# Feature 5: Breathing Exercise Widget
index_content = read_file(INDEX)
breathe_html = """
                <button id="breathe-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Breathing Exercise">
                    🫁
                </button>"""
target_zen = """<button id="zen-mode-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Zen Focus Mode">"""
index_content = index_content.replace(target_zen, breathe_html + "\n                " + target_zen)

breathe_css = """
        @keyframes pulse-breathe {
            0% { transform: scale(1); opacity: 0.8; }
            40% { transform: scale(2); opacity: 0.4; }
            100% { transform: scale(1); opacity: 0.8; }
        }
        .breathe-animate { animation: pulse-breathe 19s infinite ease-in-out; }
"""
index_content = index_content.replace(target_css, breathe_css + "\n        " + target_css)

breathe_js = """
            // Feature 5: Breathing Exercise Widget
            const breatheBtn = document.getElementById('breathe-btn');
            if(breatheBtn) {
                breatheBtn.addEventListener('click', () => {
                    let widget = document.getElementById('breathe-widget');
                    if(!widget) {
                        widget = document.createElement('div');
                        widget.id = 'breathe-widget';
                        widget.className = 'fixed inset-0 z-[100] flex items-center justify-center bg-black bg-opacity-70 backdrop-blur-sm cursor-pointer';
                        widget.innerHTML = `<div class="relative flex items-center justify-center">
                            <div class="absolute w-32 h-32 bg-blue-400 rounded-full breathe-animate"></div>
                            <div class="relative z-10 text-white font-bold text-xl text-center">
                                <span id="breathe-text">Inhale (4s)</span>
                            </div>
                        </div>`;
                        document.body.appendChild(widget);
                        
                        let step = 0;
                        const steps = [
                            { text: "Inhale (4s)", time: 4000 },
                            { text: "Hold (7s)", time: 7000 },
                            { text: "Exhale (8s)", time: 8000 }
                        ];
                        const updateBreathe = () => {
                            if(!document.getElementById('breathe-widget')) return;
                            step = (step + 1) % steps.length;
                            document.getElementById('breathe-text').innerText = steps[step].text;
                            setTimeout(updateBreathe, steps[step].time);
                        };
                        setTimeout(updateBreathe, steps[0].time);
                        
                        widget.addEventListener('click', () => widget.remove());
                    }
                });
            }
"""
index_content = index_content.replace(target_tts, breathe_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(wellness): add 4-7-8 breathing exercise widget overlay")


# Feature 6: Floating Sticky Notes (Alt+Click)
index_content = read_file(INDEX)

sticky_js = """
            // Feature 6: Floating Sticky Notes
            if(notesContent) {
                notesContent.addEventListener('click', (e) => {
                    if (e.altKey) {
                        const sticky = document.createElement('div');
                        sticky.className = 'absolute bg-yellow-200 text-gray-800 p-2 shadow-md border border-yellow-300 rounded text-sm z-50 min-w-[100px] min-h-[100px] outline-none';
                        sticky.contentEditable = true;
                        sticky.style.left = e.pageX + 'px';
                        sticky.style.top = e.pageY + 'px';
                        sticky.innerHTML = 'Note...';
                        document.body.appendChild(sticky);
                        
                        // Drag logic
                        let isDown = false, startX, startY;
                        sticky.addEventListener('mousedown', (e2) => {
                            if (e2.target !== sticky) return;
                            isDown = true;
                            startX = e2.clientX - sticky.offsetLeft;
                            startY = e2.clientY - sticky.offsetTop;
                        });
                        document.addEventListener('mouseup', () => isDown = false);
                        document.addEventListener('mousemove', (e2) => {
                            if (!isDown) return;
                            sticky.style.left = (e2.clientX - startX) + 'px';
                            sticky.style.top = (e2.clientY - startY) + 'px';
                        });
                        
                        // Double click to remove
                        sticky.addEventListener('dblclick', () => sticky.remove());
                    }
                });
            }
"""
index_content = index_content.replace(target_tts, sticky_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(notes): drop draggable sticky notes using alt-click")


# Push all
run('git push')
print("Pushed all 6 commits for Batch 14.")
