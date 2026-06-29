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

print("Applying Batch 7 Features and Committing...")

# --- Feature 1: Dictionary Tooltip on Double-Click ---
index_content = read_file(INDEX)
dict_js = """
            // Feature 1: Dictionary Tooltip on Double-Click
            const dictPopup = document.getElementById('dict-popup');
            const dictWord = document.getElementById('dict-word');
            const dictDef = document.getElementById('dict-def');
            const dictClose = document.getElementById('dict-close');
            
            if (dictPopup && dictClose) {
                dictClose.addEventListener('click', () => dictPopup.classList.add('hidden'));
                
                document.addEventListener('dblclick', async (e) => {
                    const selection = window.getSelection().toString().trim();
                    if (!selection || selection.split(' ').length > 1) return;
                    
                    const rect = window.getSelection().getRangeAt(0).getBoundingClientRect();
                    dictPopup.style.top = (rect.bottom + window.scrollY + 10) + 'px';
                    dictPopup.style.left = (rect.left + window.scrollX) + 'px';
                    
                    dictWord.textContent = selection;
                    dictDef.textContent = "Loading...";
                    dictPopup.classList.remove('hidden');
                    
                    try {
                        const res = await fetch(`https://api.dictionaryapi.dev/api/v2/entries/en/${selection}`);
                        const data = await res.json();
                        if(Array.isArray(data) && data[0].meanings.length > 0) {
                            dictDef.textContent = data[0].meanings[0].definitions[0].definition;
                        } else {
                            dictDef.textContent = "Definition not found.";
                        }
                    } catch(err) {
                        dictDef.textContent = "Error fetching definition.";
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 3: Keyboard Shortcuts", dict_js + "\n            // Feature 3: Keyboard Shortcuts")
write_file(INDEX, index_content)
commit("feat(notes): add double-click dictionary tooltip API integration")

# --- Feature 2: Download as Markdown (.md) ---
index_content = read_file(INDEX)
pdf_btn = """<button id="export-pdf-btn" class="bg-gray-800 hover:bg-gray-900 text-white font-medium px-4 py-2 rounded-lg flex items-center gap-2 text-sm shadow-sm transition">
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"></path></svg>
                    Save as PDF
                </button>"""
md_btn = """<button id="export-md-btn" class="bg-gray-700 hover:bg-gray-800 text-white font-medium px-4 py-2 rounded-lg flex items-center gap-2 text-sm shadow-sm transition mr-2">
                    ⬇️ Save as Markdown
                </button>\n                """ + pdf_btn
index_content = index_content.replace(pdf_btn, md_btn)

md_js = """
            // Feature 2: Download as Markdown
            const exportMdBtn = document.getElementById('export-md-btn');
            if(exportMdBtn) {
                exportMdBtn.addEventListener('click', () => {
                    let mdContent = "# Study Notes\\n\\n";
                    mdContent += "## Notes\\n\\n" + (notesContent?.innerText || "") + "\\n\\n";
                    mdContent += "## Summary\\n\\n" + (summaryContent?.innerText || "") + "\\n";
                    
                    const blob = new Blob([mdContent], { type: 'text/markdown' });
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'study_materials.md';
                    a.click();
                    URL.revokeObjectURL(url);
                });
            }
"""
index_content = index_content.replace("// PDF Export Logic", md_js + "\n            // PDF Export Logic")
write_file(INDEX, index_content)
commit("feat(export): add download as markdown functionality")

# --- Feature 3: Dyslexia-Friendly Font Toggle ---
index_content = read_file(INDEX)
font_btns = """<button id="font-increase" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-1 text-sm font-bold">A+</button>"""
dyslexic_btn = font_btns + """\n                                    <button id="dyslexic-btn" class="text-gray-600 dark:text-gray-300 hover:text-blue-500 px-2 text-sm font-bold border-l border-gray-300 dark:border-gray-600 ml-1" title="Dyslexia Friendly Font">OpenDyslexic</button>"""
index_content = index_content.replace(font_btns, dyslexic_btn)

dyslexic_js = """
            // Feature 3: Dyslexia-Friendly Font
            let isDyslexic = false;
            const dyslexicBtn = document.getElementById('dyslexic-btn');
            if(dyslexicBtn) {
                dyslexicBtn.addEventListener('click', () => {
                    isDyslexic = !isDyslexic;
                    const val = isDyslexic ? "'Comic Sans MS', 'OpenDyslexic', sans-serif" : "";
                    const spacing = isDyslexic ? "1px" : "";
                    if(notesContent) {
                        notesContent.style.fontFamily = val;
                        notesContent.style.letterSpacing = spacing;
                    }
                    if(summaryContent) {
                        summaryContent.style.fontFamily = val;
                        summaryContent.style.letterSpacing = spacing;
                    }
                    dyslexicBtn.classList.toggle('text-blue-600', isDyslexic);
                });
            }
"""
index_content = index_content.replace("// Feature 3: Font Size Adjuster", dyslexic_js + "\n            // Feature 3: Font Size Adjuster")
write_file(INDEX, index_content)
commit("feat(ui): add dyslexia-friendly font toggle for accessibility")

# --- Feature 4: Focus Mask (Reading Ruler) ---
index_content = read_file(INDEX)
autoscroll_btn = """<button id="autoscroll-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    📜 Auto-Scroll
                                </button>"""
mask_btn = autoscroll_btn + """\n                                <button id="focus-mask-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    🔦 Focus Mask
                                </button>"""
index_content = index_content.replace(autoscroll_btn, mask_btn)

mask_js = """
            // Feature 4: Focus Mask (Reading Ruler)
            const maskBtn = document.getElementById('focus-mask-btn');
            let isMaskActive = false;
            let maskTop, maskBottom;
            
            function focusMaskMove(e) {
                const slitHeight = 100;
                if(maskTop) maskTop.style.height = (e.clientY - slitHeight/2) + 'px';
                if(maskBottom) maskBottom.style.height = (window.innerHeight - e.clientY - slitHeight/2) + 'px';
            }

            if(maskBtn) {
                maskBtn.addEventListener('click', () => {
                    isMaskActive = !isMaskActive;
                    if(isMaskActive) {
                        maskTop = document.createElement('div');
                        maskBottom = document.createElement('div');
                        const style = 'position:fixed; left:0; width:100%; background:rgba(0,0,0,0.8); z-index:9998; pointer-events:none;';
                        maskTop.style.cssText = style + 'top:0; height:50%;';
                        maskBottom.style.cssText = style + 'bottom:0; height:50%;';
                        document.body.appendChild(maskTop);
                        document.body.appendChild(maskBottom);
                        document.addEventListener('mousemove', focusMaskMove);
                        maskBtn.classList.add('bg-blue-200', 'dark:bg-blue-800');
                    } else {
                        if(maskTop) maskTop.remove();
                        if(maskBottom) maskBottom.remove();
                        document.removeEventListener('mousemove', focusMaskMove);
                        maskBtn.classList.remove('bg-blue-200', 'dark:bg-blue-800');
                    }
                });
            }
"""
index_content = index_content.replace("// Feature 4: Teleprompter Auto-Scroll", mask_js + "\n            // Feature 4: Teleprompter Auto-Scroll")
write_file(INDEX, index_content)
commit("feat(notes): implement focus mask reading ruler")

# --- Feature 5: Quick Copy to Clipboard ---
index_content = read_file(INDEX)
copy_btn = """\n                                <button id="copy-notes-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1.5 rounded text-sm transition ml-2">
                                    📋 Copy
                                </button>"""
index_content = index_content.replace('✏️ Edit Notes\n                                </button>', '✏️ Edit Notes\n                                </button>' + copy_btn)

copy_js = """
            // Feature 5: Quick Copy
            const copyNotesBtn = document.getElementById('copy-notes-btn');
            if(copyNotesBtn) {
                copyNotesBtn.addEventListener('click', () => {
                    navigator.clipboard.writeText(notesContent?.innerText || "");
                    const oldText = copyNotesBtn.innerHTML;
                    copyNotesBtn.innerHTML = "✅ Copied!";
                    setTimeout(() => copyNotesBtn.innerHTML = oldText, 2000);
                });
            }
"""
index_content = index_content.replace("// Feature 5: Reading Progress Bar", copy_js + "\n            // Feature 5: Reading Progress Bar")
write_file(INDEX, index_content)
commit("feat(notes): add quick copy to clipboard button")

# --- Feature 6: Print-Ready Flashcards ---
index_content = read_file(INDEX)
export_csv_btn = """<button id="export-csv-btn" class="hidden bg-green-600 hover:bg-green-700 text-white px-4 py-2 rounded-lg items-center gap-2 text-sm shadow-sm transition">
                                ⬇️ Download Anki CSV
                            </button>"""
print_flash_btn = export_csv_btn + """\n                            <button id="print-flashcards-btn" class="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded-lg items-center gap-2 text-sm shadow-sm transition ml-2 hidden">
                                🖨️ Print Flashcards
                            </button>"""
index_content = index_content.replace(export_csv_btn, print_flash_btn)

print_flash_js = """
            // Feature 6: Print-Ready Flashcards
            const printFlashBtn = document.getElementById('print-flashcards-btn');
            if(printFlashBtn) {
                printFlashBtn.addEventListener('click', () => {
                    document.body.classList.add('cheat-sheet-mode');
                    const style = document.createElement('style');
                    style.id = 'print-flash-style';
                    style.innerHTML = `
                        @media print {
                            body * { visibility: hidden; }
                            #results-container, #flashcards-tab, #flashcards-container, #flashcards-container * { visibility: visible; }
                            #results-container { position: absolute; left: 0; top: 0; width: 100%; margin: 0; padding: 0; }
                            .tab-content { display: block !important; }
                            .no-print, nav, #video-player, iframe, .tab-btn { display: none !important; }
                            #flashcards-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
                            .flashcard { border: 1px dashed #ccc; padding: 20px; page-break-inside: avoid; min-height: 150px; }
                            .flashcard-inner { transform: none !important; }
                            .rotate-y-180 { transform: none !important; display: block; margin-top: 20px; border-top: 1px solid #eee; padding-top: 10px; }
                            .backface-hidden { backface-visibility: visible; position: static; }
                        }
                    `;
                    document.head.appendChild(style);
                    window.print();
                    setTimeout(() => {
                        document.body.classList.remove('cheat-sheet-mode');
                        const s = document.getElementById('print-flash-style');
                        if (s) s.remove();
                    }, 1000);
                });
            }
"""
index_content = index_content.replace("// Feature 3: Keyboard Shortcuts", print_flash_js + "\n            // Feature 3: Keyboard Shortcuts")

# We also need to unhide the button when flashcards are populated
populate_str = "if (data.flashcards && data.flashcards.length > 0) {"
populate_with_print = populate_str + "\n                    document.getElementById('print-flashcards-btn')?.classList.remove('hidden');"
index_content = index_content.replace(populate_str, populate_with_print)

write_file(INDEX, index_content)
commit("feat(flashcards): add print-ready flashcard layout generator")

print("All 6 commits created successfully!")
