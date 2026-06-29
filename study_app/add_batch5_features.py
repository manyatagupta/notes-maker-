import os

index_path = r"c:\Users\manya\OneDrive\Desktop\notes maker\study_app\templates\study_app\index.html"
dashboard_path = r"c:\Users\manya\OneDrive\Desktop\notes maker\study_app\templates\study_app\dashboard.html"

with open(index_path, "r", encoding="utf-8") as f:
    index_content = f.read()

# Feature 5: Reading Progress Bar HTML
progress_bar_html = """
    <!-- Reading Progress Bar -->
    <div class="fixed top-0 left-0 w-full h-1.5 z-50 bg-transparent pointer-events-none">
        <div id="reading-progress" class="h-full bg-blue-500 w-0 transition-all duration-150"></div>
    </div>
"""
index_content = index_content.replace('<body class="', progress_bar_html + '\n<body class="')

# Feature 1: Ambient Lofi Player HTML
lofi_player_html = """
    <!-- Ambient Lofi Player -->
    <div id="lofi-widget" class="fixed bottom-6 left-6 bg-white dark:bg-gray-800 shadow-xl rounded-xl p-3 border border-gray-200 dark:border-gray-700 z-50 flex items-center gap-3 transform hover:scale-105 transition">
        <div class="w-12 h-12 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-500 overflow-hidden relative">
            <span class="absolute inset-0 animate-ping opacity-20 bg-indigo-400 rounded-full"></span>
            🎵
        </div>
        <div>
            <div class="text-xs font-bold text-gray-500 mb-1 flex justify-between w-32">
                <span>Focus Audio</span>
                <button id="lofi-toggle" class="hover:text-blue-500">▶️</button>
            </div>
            <audio id="lofi-audio" loop src="https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3?filename=lofi-study-112191.mp3"></audio>
        </div>
    </div>
"""
index_content = index_content.replace('<!-- Pomodoro Timer Widget -->', lofi_player_html + '\n    <!-- Pomodoro Timer Widget -->')

# Feature 2: Highlight Tool Button (Hidden by default)
highlight_btn_html = """
    <!-- Highlight Tool Popup -->
    <button id="highlight-btn" class="fixed hidden bg-yellow-400 hover:bg-yellow-500 text-gray-900 font-bold px-2 py-1 rounded shadow-lg text-xs z-50 cursor-pointer">
        🖍️ Highlight
    </button>
"""
index_content = index_content.replace('<!-- Dictionary Popup -->', highlight_btn_html + '\n    <!-- Dictionary Popup -->')

# Feature 4: Voice Dictation in Scratchpad
scratchpad_target = """<button id="scratchpad-close" class="hover:text-red-500 text-lg leading-none">&times;</button>"""
scratchpad_replace = """
            <div class="flex gap-2 items-center">
                <button id="scratchpad-mic" class="hover:text-blue-600 text-sm" title="Dictate">🎤</button>
                <button id="scratchpad-close" class="hover:text-red-500 text-lg leading-none">&times;</button>
            </div>
"""
index_content = index_content.replace(scratchpad_target, scratchpad_replace)

# Feature 3: Cheat Sheet Export Button
cheat_sheet_target = """<button id="export-pdf-btn" """
cheat_sheet_replace = """
                <button id="cheat-sheet-btn" class="bg-indigo-600 hover:bg-indigo-700 text-white font-medium px-4 py-2 rounded-lg flex items-center gap-2 text-sm shadow-sm transition mr-2">
                    🖨️ Cheat Sheet
                </button>
                <button id="export-pdf-btn" """
index_content = index_content.replace(cheat_sheet_target, cheat_sheet_replace)


# JS Additions for Index
js_additions = """
            // Feature 5: Reading Progress Bar
            window.addEventListener('scroll', () => {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = (winScroll / height) * 100;
                const progress = document.getElementById('reading-progress');
                if (progress) progress.style.width = scrolled + "%";
            });

            // Feature 1: Lofi Player
            const lofiAudio = document.getElementById('lofi-audio');
            const lofiToggle = document.getElementById('lofi-toggle');
            if (lofiAudio && lofiToggle) {
                lofiToggle.addEventListener('click', () => {
                    if (lofiAudio.paused) {
                        lofiAudio.play();
                        lofiToggle.textContent = '⏸️';
                    } else {
                        lofiAudio.pause();
                        lofiToggle.textContent = '▶️';
                    }
                });
            }

            // Feature 4: Scratchpad Dictation
            const spMic = document.getElementById('scratchpad-mic');
            const spInput = document.getElementById('scratchpad-input');
            if (spMic && spInput) {
                const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
                if (SpeechRecognition) {
                    const spRec = new SpeechRecognition();
                    spRec.continuous = false;
                    spRec.interimResults = false;
                    spRec.onresult = (e) => {
                        spInput.value += (spInput.value ? ' ' : '') + e.results[0][0].transcript;
                        spMic.classList.remove('text-red-500', 'animate-pulse');
                        localStorage.setItem('study_scratchpad', spInput.value);
                    };
                    spRec.onend = () => spMic.classList.remove('text-red-500', 'animate-pulse');
                    spMic.addEventListener('click', () => {
                        spRec.start();
                        spMic.classList.add('text-red-500', 'animate-pulse');
                    });
                } else {
                    spMic.style.display = 'none';
                }
            }

            // Feature 2: Custom Text Highlighter
            const hlBtn = document.getElementById('highlight-btn');
            const nContent = document.getElementById('notes-content');
            if (nContent && hlBtn) {
                nContent.addEventListener('mouseup', (e) => {
                    const selection = window.getSelection();
                    if (selection.toString().length > 0 && nContent.contains(selection.anchorNode)) {
                        const rect = selection.getRangeAt(0).getBoundingClientRect();
                        hlBtn.style.top = (rect.top - 30) + 'px';
                        hlBtn.style.left = (rect.left + rect.width / 2 - 35) + 'px';
                        hlBtn.classList.remove('hidden');
                    } else {
                        hlBtn.classList.add('hidden');
                    }
                });
                hlBtn.addEventListener('click', () => {
                    const selection = window.getSelection();
                    if (selection.rangeCount && selection.toString().length > 0) {
                        const range = selection.getRangeAt(0);
                        const span = document.createElement('span');
                        span.className = 'bg-yellow-200 dark:bg-yellow-700 text-black dark:text-white rounded px-1';
                        range.surroundContents(span);
                        hlBtn.classList.add('hidden');
                        selection.removeAllRanges();
                    }
                });
                document.addEventListener('mousedown', (e) => {
                    if (e.target !== hlBtn) hlBtn.classList.add('hidden');
                });
            }

            // Feature 3: Cheat Sheet Generator
            const cheatBtn = document.getElementById('cheat-sheet-btn');
            if (cheatBtn) {
                cheatBtn.addEventListener('click', () => {
                    document.body.classList.add('cheat-sheet-mode');
                    
                    // Inject temporary styles for print
                    const style = document.createElement('style');
                    style.id = 'cheat-sheet-style';
                    style.innerHTML = `
                        @media print {
                            body * { visibility: hidden; }
                            #results-area, #results-container, #notes-tab, #summary-tab, #notes-content, #summary-content, #notes-content *, #summary-content * { visibility: visible; }
                            
                            #results-container { position: absolute; left: 0; top: 0; width: 100%; margin: 0; padding: 0; }
                            .tab-content { display: block !important; page-break-inside: avoid; }
                            .no-print, nav, #video-player, iframe, .tab-btn { display: none !important; }
                            
                            /* Multi-column layout for density */
                            #notes-content, #summary-content {
                                column-count: 2;
                                column-gap: 20px;
                                font-size: 10pt !important;
                                line-height: 1.2 !important;
                                text-align: left;
                            }
                            h1, h2, h3 { font-size: 12pt !important; margin: 5px 0 !important; }
                            p, li { margin-bottom: 3px !important; }
                        }
                    `;
                    document.head.appendChild(style);
                    
                    window.print();
                    
                    setTimeout(() => {
                        document.body.classList.remove('cheat-sheet-mode');
                        const s = document.getElementById('cheat-sheet-style');
                        if (s) s.remove();
                    }, 1000);
                });
            }
"""
index_content = index_content.replace("// Feature 3: Keyboard Shortcuts", js_additions + "\n            // Feature 3: Keyboard Shortcuts")

with open(index_path, "w", encoding="utf-8") as f:
    f.write(index_content)


# Dashboard modifications
with open(dashboard_path, "r", encoding="utf-8") as f:
    dash_content = f.read()

# Feature 6: Daily Motivational Quote
quote_html = """
        <!-- Feature 6: Daily Quote -->
        <div class="bg-gradient-to-r from-purple-500 to-indigo-600 rounded-xl shadow-lg p-6 mb-8 text-white relative overflow-hidden">
            <div class="absolute -right-4 -top-4 opacity-10 text-9xl">"</div>
            <h3 class="text-sm font-bold uppercase tracking-wider mb-2 opacity-80">Daily Study Motivation</h3>
            <p id="daily-quote-text" class="text-xl font-medium italic mb-2">"Loading inspiration..."</p>
            <p id="daily-quote-author" class="text-sm font-semibold opacity-90"></p>
        </div>
"""
dash_content = dash_content.replace('<!-- Analytics Chart -->', quote_html + '\n        <!-- Analytics Chart -->')

dash_js = """
<script>
document.addEventListener('DOMContentLoaded', () => {
    // Feature 6: Fetch Quote
    const quotes = [
        {"q": "The secret of getting ahead is getting started.", "a": "Mark Twain"},
        {"q": "It always seems impossible until it is done.", "a": "Nelson Mandela"},
        {"q": "Don't watch the clock; do what it does. Keep going.", "a": "Sam Levenson"},
        {"q": "Success is not final, failure is not fatal: it is the courage to continue that counts.", "a": "Winston Churchill"},
        {"q": "The future belongs to those who believe in the beauty of their dreams.", "a": "Eleanor Roosevelt"}
    ];
    
    // Try to fetch from API, fallback to array
    fetch('https://dummyjson.com/quotes/random')
        .then(res => res.json())
        .then(data => {
            document.getElementById('daily-quote-text').textContent = `"${data.quote}"`;
            document.getElementById('daily-quote-author').textContent = `- ${data.author}`;
        })
        .catch(() => {
            const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];
            document.getElementById('daily-quote-text').textContent = `"${randomQuote.q}"`;
            document.getElementById('daily-quote-author').textContent = `- ${randomQuote.a}`;
        });
});
</script>
"""
dash_content = dash_content.replace('{% endblock %}', dash_js + '\n{% endblock %}')

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(dash_content)

print("Batch 5 applied successfully!")
