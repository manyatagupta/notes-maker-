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

print("Applying Batch 8 Features and Committing...")

# --- Feature 1: Fullscreen Study Mode ---
index_content = read_file(INDEX)
zen_btn = """<!-- Zen Mode Toggle Button -->
                <button id="zen-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Zen Mode">
                    🌙
                </button>"""
fullscreen_btn = zen_btn + """\n                <!-- Fullscreen Toggle Button -->
                <button id="fullscreen-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Fullscreen Mode">
                    ⛶
                </button>"""
index_content = index_content.replace(zen_btn, fullscreen_btn)

fullscreen_js = """
            // Feature 1: Fullscreen Mode
            const fullscreenToggle = document.getElementById('fullscreen-toggle');
            if (fullscreenToggle) {
                fullscreenToggle.addEventListener('click', () => {
                    if (!document.fullscreenElement) {
                        document.documentElement.requestFullscreen().catch(err => {
                            console.log(`Error attempting to enable fullscreen: ${err.message}`);
                        });
                    } else {
                        document.exitFullscreen();
                    }
                });
            }
"""
index_content = index_content.replace("// Theme Toggle Logic", fullscreen_js + "\n                // Theme Toggle Logic")
write_file(INDEX, index_content)
commit("feat(ui): add fullscreen study mode toggle")

# --- Feature 2: Blue Light Filter (Sepia Mode) ---
index_content = read_file(INDEX)
sepia_btn = """\n                <!-- Sepia Toggle Button -->
                <button id="sepia-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Blue Light Filter">
                    ☕
                </button>"""
index_content = index_content.replace('title="Fullscreen Mode">\n                    ⛶\n                </button>', 'title="Fullscreen Mode">\n                    ⛶\n                </button>' + sepia_btn)

sepia_js = """
            // Feature 2: Blue Light Filter (Sepia)
            const sepiaToggle = document.getElementById('sepia-toggle');
            let isSepia = false;
            if (sepiaToggle) {
                sepiaToggle.addEventListener('click', () => {
                    isSepia = !isSepia;
                    if (isSepia) {
                        document.body.style.filter = 'sepia(0.5) hue-rotate(-30deg)';
                        sepiaToggle.classList.add('bg-orange-100', 'dark:bg-orange-900');
                    } else {
                        document.body.style.filter = '';
                        sepiaToggle.classList.remove('bg-orange-100', 'dark:bg-orange-900');
                    }
                });
            }
"""
index_content = index_content.replace("// Theme Toggle Logic", sepia_js + "\n                // Theme Toggle Logic")
write_file(INDEX, index_content)
commit("feat(ui): implement blue light filter (sepia mode) for night studying")

# --- Feature 3: Line Spacing Adjuster ---
index_content = read_file(INDEX)
font_adjuster = """<div class="flex items-center bg-gray-100 dark:bg-gray-800 rounded px-2 py-1 mr-2 border border-gray-200 dark:border-gray-700">
                                    <button id="font-decrease" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">A-</button>
                                    <button id="font-reset" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">A</button>
                                    <button id="font-increase" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">A+</button>
                                    <button id="dyslexic-btn" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-2 text-sm font-bold border-l border-gray-300 dark:border-gray-600 ml-1" title="Dyslexia Friendly Font">OpenDyslexic</button>
                                </div>"""
line_height_adjuster = font_adjuster + """\n                                <div class="flex items-center bg-gray-100 dark:bg-gray-800 rounded px-2 py-1 mr-2 border border-gray-200 dark:border-gray-700">
                                    <button id="line-height-decrease" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">↕-</button>
                                    <button id="line-height-increase" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">↕+</button>
                                </div>"""
index_content = index_content.replace(font_adjuster, line_height_adjuster)

line_height_js = """
            // Feature 3: Line Spacing Adjuster
            let currentLineHeight = 1.6;
            document.getElementById('line-height-decrease')?.addEventListener('click', () => {
                currentLineHeight = Math.max(1.0, currentLineHeight - 0.2);
                if(notesContent) notesContent.style.lineHeight = currentLineHeight;
            });
            document.getElementById('line-height-increase')?.addEventListener('click', () => {
                currentLineHeight = Math.min(3.0, currentLineHeight + 0.2);
                if(notesContent) notesContent.style.lineHeight = currentLineHeight;
            });
"""
index_content = index_content.replace("// Feature 3: Dyslexia-Friendly Font", line_height_js + "\n            // Feature 3: Dyslexia-Friendly Font")
write_file(INDEX, index_content)
commit("feat(notes): add line spacing adjustment controls")

# --- Feature 4: High Contrast Mode Toggle ---
index_content = read_file(INDEX)
contrast_btn = """\n                <!-- High Contrast Toggle Button -->
                <button id="contrast-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="High Contrast Mode">
                    🌗
                </button>"""
index_content = index_content.replace('title="Blue Light Filter">\n                    ☕\n                </button>', 'title="Blue Light Filter">\n                    ☕\n                </button>' + contrast_btn)

contrast_js = """
            // Feature 4: High Contrast Mode
            const contrastToggle = document.getElementById('contrast-toggle');
            let isHighContrast = false;
            if (contrastToggle) {
                contrastToggle.addEventListener('click', () => {
                    isHighContrast = !isHighContrast;
                    if (isHighContrast) {
                        document.documentElement.style.filter = 'contrast(1.5) grayscale(1)';
                        contrastToggle.classList.add('bg-gray-300', 'dark:bg-gray-600');
                    } else {
                        document.documentElement.style.filter = '';
                        contrastToggle.classList.remove('bg-gray-300', 'dark:bg-gray-600');
                    }
                });
            }
"""
index_content = index_content.replace("// Theme Toggle Logic", contrast_js + "\n                // Theme Toggle Logic")
write_file(INDEX, index_content)
commit("feat(ui): add high contrast mode toggle for accessibility")

# --- Feature 5: Floating Scroll-to-Top/Bottom Buttons ---
index_content = read_file(INDEX)
scroll_html = """
    <!-- Feature 5: Scroll Buttons -->
    <div class="fixed right-6 bottom-32 flex flex-col gap-2 z-40">
        <button id="scroll-top-btn" class="bg-gray-800 text-white p-3 rounded-full shadow-lg hover:bg-gray-700 transition opacity-0 invisible" title="Scroll to Top">
            ↑
        </button>
        <button id="scroll-bottom-btn" class="bg-gray-800 text-white p-3 rounded-full shadow-lg hover:bg-gray-700 transition opacity-0 invisible" title="Scroll to Bottom">
            ↓
        </button>
    </div>
"""
index_content = index_content.replace('<!-- Pomodoro Timer Widget -->', scroll_html + '\n    <!-- Pomodoro Timer Widget -->')

scroll_js = """
            // Feature 5: Scroll Buttons
            const scrollTopBtn = document.getElementById('scroll-top-btn');
            const scrollBottomBtn = document.getElementById('scroll-bottom-btn');
            
            window.addEventListener('scroll', () => {
                if (window.scrollY > 300) {
                    scrollTopBtn?.classList.remove('opacity-0', 'invisible');
                } else {
                    scrollTopBtn?.classList.add('opacity-0', 'invisible');
                }
                
                if (window.scrollY + window.innerHeight < document.body.scrollHeight - 300) {
                    scrollBottomBtn?.classList.remove('opacity-0', 'invisible');
                } else {
                    scrollBottomBtn?.classList.add('opacity-0', 'invisible');
                }
            });
            
            scrollTopBtn?.addEventListener('click', () => window.scrollTo({top: 0, behavior: 'smooth'}));
            scrollBottomBtn?.addEventListener('click', () => window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'}));
"""
index_content = index_content.replace("// Feature 3: Keyboard Shortcuts", scroll_js + "\n            // Feature 3: Keyboard Shortcuts")
write_file(INDEX, index_content)
commit("feat(ui): implement floating scroll-to-top and scroll-to-bottom buttons")

# --- Feature 6: Text Alignment Toggle ---
index_content = read_file(INDEX)
align_btn = """<button id="align-toggle" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition mr-2" title="Toggle Justify">
                                    ⫶⫶ Justify
                                </button>"""
index_content = index_content.replace('<div class="flex items-center bg-gray-100 dark:bg-gray-800 rounded px-2 py-1 mr-2 border border-gray-200 dark:border-gray-700">\n                                    <button id="line-height-decrease"', align_btn + '\n                                <div class="flex items-center bg-gray-100 dark:bg-gray-800 rounded px-2 py-1 mr-2 border border-gray-200 dark:border-gray-700">\n                                    <button id="line-height-decrease"')

align_js = """
            // Feature 6: Text Alignment
            let isJustified = false;
            const alignToggle = document.getElementById('align-toggle');
            if(alignToggle) {
                alignToggle.addEventListener('click', () => {
                    isJustified = !isJustified;
                    if(notesContent) {
                        notesContent.style.textAlign = isJustified ? 'justify' : 'left';
                    }
                    if(summaryContent) {
                        summaryContent.style.textAlign = isJustified ? 'justify' : 'left';
                    }
                    alignToggle.classList.toggle('bg-blue-200', isJustified);
                    alignToggle.classList.toggle('dark:bg-blue-800', isJustified);
                });
            }
"""
index_content = index_content.replace("// Feature 3: Line Spacing Adjuster", align_js + "\n            // Feature 3: Line Spacing Adjuster")
write_file(INDEX, index_content)
commit("feat(notes): add text alignment toggle for readability")

print("All 6 commits created successfully!")
