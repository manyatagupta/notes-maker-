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

print("Starting Batch 15 feature injection...")

# Feature 1: Focus Line Reader
index_content = read_file(INDEX)
focus_line_html = """
                                <button id="focus-line-btn" class="bg-blue-100 hover:bg-blue-200 dark:bg-blue-800 dark:hover:bg-blue-700 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    📏 Focus Line
                                </button>"""
target_hide_img = """<button id="hide-img-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2" title="Toggle Images">
                                    🖼️ Hide Images
                                </button>"""
index_content = index_content.replace(target_hide_img, target_hide_img + focus_line_html)

focus_line_js = """
            // Feature 1: Focus Line Reader
            const focusLineBtn = document.getElementById('focus-line-btn');
            if(focusLineBtn) {
                focusLineBtn.addEventListener('click', () => {
                    let line = document.getElementById('focus-line');
                    if(!line) {
                        line = document.createElement('div');
                        line.id = 'focus-line';
                        line.className = 'fixed left-0 w-full h-[2px] bg-red-500 shadow-sm z-50 pointer-events-none opacity-50';
                        document.body.appendChild(line);
                        
                        document.addEventListener('mousemove', (e) => {
                            if(document.getElementById('focus-line')) {
                                document.getElementById('focus-line').style.top = e.clientY + 'px';
                            }
                        });
                        focusLineBtn.classList.add('bg-blue-500', 'text-white');
                    } else {
                        line.remove();
                        focusLineBtn.classList.remove('bg-blue-500', 'text-white');
                    }
                });
            }
"""
target_tts = "document.getElementById('listen-notes-btn')?.addEventListener('click'"
index_content = index_content.replace(target_tts, focus_line_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(a11y): add mouse-tracking focus line reader")


# Feature 2: Deep Focus Binaural Beats
index_content = read_file(INDEX)
binaural_html = """
                <!-- Binaural Beats -->
                <button id="binaural-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Deep Focus Binaural Beats">
                    🎧
                </button>"""
target_rain = """<button id="rain-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Ambient Rain Sounds">
                    🌧️
                </button>"""
index_content = index_content.replace(target_rain, target_rain + binaural_html)

binaural_js = """
            // Feature 2: Deep Focus Binaural Beats
            const binauralBtn = document.getElementById('binaural-btn');
            let audioCtx;
            let osc1, osc2, gainNode;
            let isBinauralPlaying = false;
            
            if(binauralBtn) {
                binauralBtn.addEventListener('click', () => {
                    if(!isBinauralPlaying) {
                        if(!audioCtx) {
                            audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                            osc1 = audioCtx.createOscillator();
                            osc2 = audioCtx.createOscillator();
                            gainNode = audioCtx.createGain();
                            
                            osc1.type = 'sine';
                            osc2.type = 'sine';
                            // Focus frequency (e.g., 14Hz difference for Beta waves)
                            osc1.frequency.setValueAtTime(200, audioCtx.currentTime);
                            osc2.frequency.setValueAtTime(214, audioCtx.currentTime);
                            
                            gainNode.gain.setValueAtTime(0.1, audioCtx.currentTime); // very soft
                            
                            // Pan left and right
                            const panLeft = audioCtx.createStereoPanner();
                            const panRight = audioCtx.createStereoPanner();
                            panLeft.pan.value = -1;
                            panRight.pan.value = 1;
                            
                            osc1.connect(panLeft).connect(gainNode);
                            osc2.connect(panRight).connect(gainNode);
                            gainNode.connect(audioCtx.destination);
                            
                            osc1.start();
                            osc2.start();
                        } else {
                            audioCtx.resume();
                        }
                        isBinauralPlaying = true;
                        binauralBtn.classList.add('bg-blue-100', 'dark:bg-blue-900');
                    } else {
                        audioCtx.suspend();
                        isBinauralPlaying = false;
                        binauralBtn.classList.remove('bg-blue-100', 'dark:bg-blue-900');
                    }
                });
            }
"""
index_content = index_content.replace(target_tts, binaural_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(wellness): add synthesized binaural beats audio generator")


# Feature 3: Collapsible Header Accordions
index_content = read_file(INDEX)

accordian_js = """
                    const setupAccordions = () => {
                        const headers = notesContent.querySelectorAll('h2, h3');
                        headers.forEach(header => {
                            header.classList.add('cursor-pointer', 'hover:opacity-80', 'transition', 'select-none');
                            header.title = "Click to collapse/expand";
                            header.innerHTML = '<span class="text-xs mr-2 transition-transform inline-block">▼</span>' + header.innerHTML;
                            
                            header.addEventListener('click', () => {
                                const arrow = header.querySelector('span');
                                let sibling = header.nextElementSibling;
                                let isCollapsed = arrow.style.transform === 'rotate(-90deg)';
                                
                                arrow.style.transform = isCollapsed ? 'rotate(0deg)' : 'rotate(-90deg)';
                                
                                while(sibling && !['H2', 'H3'].includes(sibling.tagName)) {
                                    sibling.style.display = isCollapsed ? '' : 'none';
                                    sibling = sibling.nextElementSibling;
                                }
                            });
                        });
                    };
"""
target_def = "const convertChecklists = () => {"
index_content = index_content.replace(target_def, accordian_js + "\n                    " + target_def)
target_inv = "try { convertChecklists(); } catch(e) { console.error(\"Error in convertChecklists\", e); }"
index_content = index_content.replace(target_inv, target_inv + "\n                    try { setupAccordions(); } catch(e) { console.error(\"Error in setupAccordions\", e); }")
write_file(INDEX, index_content)
commit("feat(notes): implement collapsible header accordions for easier reading")


# Feature 4: Flashcard Star Tagging
index_content = read_file(INDEX)
target_flashcard = """<div class="flashcard-inner w-full h-full relative rounded-xl shadow-md border border-gray-100">"""
star_html = """<div class="flashcard-inner w-full h-full relative rounded-xl shadow-md border border-gray-100 transition-all duration-300">
                                <button class="star-btn absolute top-3 right-3 z-10 text-gray-300 hover:text-yellow-400 transition" onclick="event.stopPropagation(); this.closest('.flashcard-inner').classList.toggle('ring-4'); this.closest('.flashcard-inner').classList.toggle('ring-yellow-400'); this.classList.toggle('text-yellow-400'); this.classList.toggle('text-gray-300');" title="Mark as Hard">⭐</button>"""
index_content = index_content.replace(target_flashcard, star_html)
write_file(INDEX, index_content)
commit("feat(flashcards): add star toggle to mark difficult flashcards")


# Feature 5: Smart Dark Mode Images
index_content = read_file(INDEX)
smart_img_html = """
                                <button id="smart-img-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2" title="Invert Images for Dark Mode">
                                    🌙 Smart Images
                                </button>"""
index_content = index_content.replace(target_hide_img, target_hide_img + smart_img_html)

smart_img_js = """
            // Feature 5: Smart Dark Mode Images
            const smartImgBtn = document.getElementById('smart-img-btn');
            if(smartImgBtn) {
                smartImgBtn.addEventListener('click', () => {
                    const imgs = document.querySelectorAll('#notes-content img');
                    imgs.forEach(img => {
                        if(img.style.filter.includes('invert')) {
                            img.style.filter = '';
                        } else {
                            img.style.filter = 'invert(1) hue-rotate(180deg) brightness(95%)';
                        }
                    });
                    smartImgBtn.classList.toggle('bg-blue-500');
                    smartImgBtn.classList.toggle('text-white');
                });
            }
"""
index_content = index_content.replace(target_tts, smart_img_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(ui): add smart image inversion toggle for dark mode compatibility")


# Feature 6: Mindfulness Chime
index_content = read_file(INDEX)
chime_html = """
                <!-- Mindfulness Chime -->
                <button id="chime-btn" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="15-min Mindfulness Chime">
                    🔔
                </button>"""
index_content = index_content.replace(target_rain, target_rain + chime_html)

chime_js = """
            // Feature 6: Mindfulness Chime
            const chimeBtn = document.getElementById('chime-btn');
            let chimeInterval = null;
            if(chimeBtn) {
                const playChime = () => {
                    const ctx = new (window.AudioContext || window.webkitAudioContext)();
                    const osc = ctx.createOscillator();
                    const gain = ctx.createGain();
                    osc.type = 'sine';
                    osc.frequency.setValueAtTime(523.25, ctx.currentTime); // C5
                    osc.frequency.exponentialRampToValueAtTime(261.63, ctx.currentTime + 1.5);
                    gain.gain.setValueAtTime(0.5, ctx.currentTime);
                    gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 1.5);
                    osc.connect(gain).connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + 1.5);
                };
                
                chimeBtn.addEventListener('click', () => {
                    if(chimeInterval) {
                        clearInterval(chimeInterval);
                        chimeInterval = null;
                        chimeBtn.classList.remove('bg-yellow-100', 'dark:bg-yellow-900');
                    } else {
                        playChime(); // Play test sound immediately
                        chimeInterval = setInterval(playChime, 15 * 60 * 1000); // Every 15 mins
                        chimeBtn.classList.add('bg-yellow-100', 'dark:bg-yellow-900');
                    }
                });
            }
"""
index_content = index_content.replace(target_tts, chime_js + "\n            " + target_tts)
write_file(INDEX, index_content)
commit("feat(wellness): add 15-minute mindfulness interval chime")

run('git push')
print("Pushed Batch 15 to GitHub!")
