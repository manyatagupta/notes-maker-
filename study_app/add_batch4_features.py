import os

index_path = r"c:\Users\manya\OneDrive\Desktop\notes maker\study_app\templates\study_app\index.html"

with open(index_path, "r", encoding="utf-8") as f:
    content = f.read()

# Feature 1: ELI5 Button for Notes tab
notes_buttons_target = """<button id="translate-notes-btn" class="bg-indigo-100 hover:bg-indigo-200 text-indigo-700 dark:bg-indigo-900 dark:text-indigo-300 px-3 py-1.5 rounded text-sm font-medium transition">
                                    🌍 Translate
                                </button>"""
notes_buttons_replacement = notes_buttons_target + """
                                <button id="eli5-notes-btn" class="bg-pink-100 hover:bg-pink-200 text-pink-700 dark:bg-pink-900 dark:text-pink-300 px-3 py-1.5 rounded text-sm font-medium transition ml-2">
                                    🧒 ELI5
                                </button>"""
content = content.replace(notes_buttons_target, notes_buttons_replacement)

# Feature 1: ELI5 Button for Summary tab
summary_buttons_target = """<button id="listen-summary-btn" class="bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-white px-3 py-1 rounded text-sm transition">
                                🔊 Listen
                            </button>"""
summary_buttons_replacement = """<button id="eli5-summary-btn" class="bg-pink-100 hover:bg-pink-200 text-pink-700 dark:bg-pink-900 dark:text-pink-300 px-3 py-1 rounded text-sm transition mr-2">
                                🧒 ELI5
                            </button>""" + summary_buttons_target
content = content.replace(summary_buttons_target, summary_buttons_replacement)

# Feature 4: Floating Scratchpad HTML
scratchpad_html = """
    <!-- Floating Scratchpad Widget -->
    <div id="scratchpad-widget" class="fixed top-24 left-6 bg-yellow-100 dark:bg-yellow-900/40 shadow-xl rounded-sm border border-yellow-300 dark:border-yellow-700 z-40 hidden flex-col w-64 h-64 transform rotate-1 cursor-move">
        <div class="bg-yellow-200 dark:bg-yellow-800 px-2 py-1 flex justify-between items-center text-xs text-yellow-800 dark:text-yellow-200 font-bold border-b border-yellow-300 dark:border-yellow-700">
            <span>📝 Scratchpad</span>
            <button id="scratchpad-close" class="hover:text-red-500 text-lg leading-none">&times;</button>
        </div>
        <textarea id="scratchpad-input" class="flex-1 w-full p-2 bg-transparent outline-none resize-none text-gray-800 dark:text-yellow-100 placeholder-yellow-600/50" placeholder="Jot down notes here... Auto-saves!"></textarea>
    </div>
"""
# Insert scratchpad before Dictionary Popup
dict_popup_target = '<!-- Dictionary Popup -->'
content = content.replace(dict_popup_target, scratchpad_html + "\n    " + dict_popup_target)

# Add scratchpad toggle button to Navbar
navbar_target = """<!-- Zen Mode Toggle Button -->"""
scratchpad_btn = """<button id="scratchpad-toggle" type="button" class="text-gray-500 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 focus:outline-none rounded-lg text-sm p-2.5 mr-2" title="Toggle Scratchpad">
                    📝
                </button>
                """
content = content.replace(navbar_target, scratchpad_btn + navbar_target)


# Feature 2 & 5 & JS logic additions
js_additions = """
            // Feature 1: ELI5 Logic
            async function triggerELI5(materialId, type, contentEl, btnEl) {
                const originalText = btnEl.innerHTML;
                btnEl.innerHTML = "Processing...";
                btnEl.disabled = true;
                
                try {
                    const res = await fetch(`/eli5_content/${materialId}/`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        body: JSON.stringify({ type: type })
                    });
                    const data = await res.json();
                    if (data.eli5_text) {
                        contentEl.innerHTML = data.eli5_text.split('\\n').filter(p => p.trim()).map(p => `<p class="mb-4">${p}</p>`).join('');
                    } else {
                        alert(data.error);
                    }
                } catch (e) {
                    alert('Error applying ELI5');
                } finally {
                    btnEl.innerHTML = originalText;
                    btnEl.disabled = false;
                }
            }
            
            document.getElementById('eli5-notes-btn')?.addEventListener('click', function() {
                if (currentMaterialId) triggerELI5(currentMaterialId, 'notes', notesContent, this);
            });
            document.getElementById('eli5-summary-btn')?.addEventListener('click', function() {
                if (currentMaterialId) triggerELI5(currentMaterialId, 'summary', summaryContent, this);
            });

            // Feature 3: Keyboard Shortcuts
            document.addEventListener('keydown', (e) => {
                // Esc to close widgets
                if (e.key === 'Escape') {
                    document.getElementById('ask-ai-body')?.classList.add('hidden');
                    document.getElementById('dict-popup')?.classList.add('hidden');
                }
                
                // Alt shortcuts
                if (e.altKey) {
                    if (e.key.toLowerCase() === 'n') { e.preventDefault(); document.querySelector('[data-target="notes-tab"]')?.click(); }
                    if (e.key.toLowerCase() === 's') { e.preventDefault(); document.querySelector('[data-target="summary-tab"]')?.click(); }
                    if (e.key.toLowerCase() === 'f') { e.preventDefault(); document.querySelector('[data-target="flashcards-tab"]')?.click(); }
                    if (e.key.toLowerCase() === 'q') { e.preventDefault(); document.querySelector('[data-target="quiz-tab"]')?.click(); }
                }

                // Ctrl + / for Ask AI
                if (e.ctrlKey && e.key === '/') {
                    e.preventDefault();
                    document.getElementById('ask-ai-body')?.classList.remove('hidden');
                    document.getElementById('ask-ai-input')?.focus();
                }
            });

            // Feature 4: Scratchpad Logic
            const scratchpad = document.getElementById('scratchpad-widget');
            const scratchpadToggle = document.getElementById('scratchpad-toggle');
            const scratchpadClose = document.getElementById('scratchpad-close');
            const scratchpadInput = document.getElementById('scratchpad-input');
            
            if (scratchpadToggle) {
                scratchpadToggle.addEventListener('click', () => scratchpad.classList.toggle('hidden'));
                scratchpadClose.addEventListener('click', () => scratchpad.classList.add('hidden'));
                
                // Load saved notes
                scratchpadInput.value = localStorage.getItem('study_scratchpad') || '';
                scratchpadInput.addEventListener('input', () => {
                    localStorage.setItem('study_scratchpad', scratchpadInput.value);
                });

                // Draggable logic
                let isDragging = false;
                let currentX;
                let currentY;
                let initialX;
                let initialY;
                let xOffset = 0;
                let yOffset = 0;

                scratchpad.addEventListener("mousedown", dragStart);
                document.addEventListener("mouseup", dragEnd);
                document.addEventListener("mousemove", drag);

                function dragStart(e) {
                    if (e.target.tagName.toLowerCase() === 'textarea' || e.target.tagName.toLowerCase() === 'button') return;
                    initialX = e.clientX - xOffset;
                    initialY = e.clientY - yOffset;
                    if (e.target.closest('#scratchpad-widget')) {
                        isDragging = true;
                    }
                }
                function dragEnd(e) {
                    initialX = currentX;
                    initialY = currentY;
                    isDragging = false;
                }
                function drag(e) {
                    if (isDragging) {
                        e.preventDefault();
                        currentX = e.clientX - initialX;
                        currentY = e.clientY - initialY;
                        xOffset = currentX;
                        yOffset = currentY;
                        scratchpad.style.transform = `translate3d(${currentX}px, ${currentY}px, 0) rotate(1deg)`;
                    }
                }
            }
"""

js_target = "let currentMaterialId = null;"
content = content.replace(js_target, js_target + "\n" + js_additions)


# Feature 2: Quiz Timer & Score HTML insertion in JS `populateResults`
quiz_populate_target = """
                // Quiz
                if (data.quiz && Array.isArray(data.quiz)) {
                    quizContainer.innerHTML = '';
"""
quiz_populate_replacement = """
                // Quiz
                if (data.quiz && Array.isArray(data.quiz)) {
                    quizContainer.innerHTML = `
                        <div class="flex justify-between items-center mb-6 bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm">
                            <div class="text-xl font-bold font-mono text-blue-600 dark:text-blue-400" id="quiz-timer">00:00</div>
                            <button id="start-quiz-btn" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium">Start Timed Quiz</button>
                        </div>
                        <div id="quiz-questions" class="space-y-8 hidden"></div>
                        <div class="mt-8 hidden" id="quiz-submit-container">
                            <button id="submit-quiz-btn" class="w-full bg-green-600 hover:bg-green-700 text-white font-bold py-3 rounded-xl text-lg shadow-lg">Submit & Get Score</button>
                        </div>
                        <div id="quiz-score-display" class="hidden mt-8 text-center bg-gray-50 dark:bg-gray-800 p-8 rounded-xl border border-gray-200 dark:border-gray-700">
                            <h3 class="text-3xl font-bold text-gray-800 dark:text-white mb-2">Quiz Complete!</h3>
                            <div class="text-5xl font-extrabold text-blue-600 dark:text-blue-400 mb-4" id="quiz-final-score"></div>
                            <p class="text-gray-500 dark:text-gray-400" id="quiz-feedback-msg"></p>
                        </div>
                    `;
                    const questionsContainer = document.getElementById('quiz-questions');
"""
content = content.replace(quiz_populate_target, quiz_populate_replacement)

# Update quiz appending logic
quiz_append_target = """quizContainer.appendChild(questionDiv);"""
quiz_append_replacement = """questionsContainer.appendChild(questionDiv);"""
content = content.replace(quiz_append_target, quiz_append_replacement)

# Update quiz timer logic inside populateResults
quiz_timer_logic = """
                    // Quiz Timer Logic
                    let qTimerInterval;
                    let qTimeLeft = data.quiz.length * 60; // 1 minute per question
                    let qScore = 0;
                    
                    document.getElementById('start-quiz-btn').addEventListener('click', function() {
                        this.classList.add('hidden');
                        document.getElementById('quiz-questions').classList.remove('hidden');
                        document.getElementById('quiz-submit-container').classList.remove('hidden');
                        
                        const display = document.getElementById('quiz-timer');
                        qTimerInterval = setInterval(() => {
                            if (qTimeLeft > 0) {
                                qTimeLeft--;
                                const m = Math.floor(qTimeLeft / 60).toString().padStart(2, '0');
                                const s = (qTimeLeft % 60).toString().padStart(2, '0');
                                display.textContent = `${m}:${s}`;
                            } else {
                                clearInterval(qTimerInterval);
                                document.getElementById('submit-quiz-btn').click(); // auto submit
                            }
                        }, 1000);
                    });

                    document.getElementById('submit-quiz-btn').addEventListener('click', function() {
                        clearInterval(qTimerInterval);
                        this.closest('#quiz-submit-container').classList.add('hidden');
                        document.getElementById('start-quiz-btn').classList.add('hidden'); // hide start button
                        
                        // Calculate score
                        let correctAnswers = 0;
                        document.querySelectorAll('.check-answer-btn').forEach(btn => {
                            btn.click(); // auto check all
                            if (btn.nextElementSibling.classList.contains('text-green-600')) {
                                correctAnswers++;
                            }
                            btn.classList.add('hidden'); // hide show answer buttons
                        });
                        
                        const scoreDisplay = document.getElementById('quiz-score-display');
                        const scoreText = document.getElementById('quiz-final-score');
                        const msgText = document.getElementById('quiz-feedback-msg');
                        
                        scoreDisplay.classList.remove('hidden');
                        scoreText.textContent = `${correctAnswers} / ${data.quiz.length}`;
                        
                        const percentage = (correctAnswers / data.quiz.length) * 100;
                        if (percentage === 100) msgText.textContent = "Perfect! You're a master!";
                        else if (percentage >= 70) msgText.textContent = "Great job! Keep it up!";
                        else msgText.textContent = "Good effort. Review the notes and try again!";
                    });
"""
# Insert after quiz event listeners
quiz_listeners_target = """feedback.classList.remove('hidden');
                        });
                    });"""
content = content.replace(quiz_listeners_target, quiz_listeners_target + "\n" + quiz_timer_logic)

# Feature 5: Explore More Wikipedia Links
wiki_logic_target = """
                // Summary
                if (data.summary) {
                    summaryContent.innerHTML = data.summary.split('\\n').filter(p => p.trim()).map(p => `<p class="mb-4">${p}</p>`).join('');
                }
"""
wiki_logic_replacement = """
                // Summary & Explore More
                if (data.summary) {
                    summaryContent.innerHTML = data.summary.split('\\n').filter(p => p.trim()).map(p => `<p class="mb-4">${p}</p>`).join('');
                    
                    // Extract some random capitalized words (naive keyword extraction for Explore More)
                    const words = data.summary.match(/[A-Z][a-z]+/g) || [];
                    const uniqueWords = [...new Set(words)].filter(w => w.length > 4).slice(0, 3);
                    
                    if (uniqueWords.length > 0) {
                        const wikiLinks = uniqueWords.map(w => 
                            `<a href="https://en.wikipedia.org/wiki/${w}" target="_blank" class="inline-block bg-white dark:bg-gray-800 px-4 py-2 rounded-full shadow-sm text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-gray-700 transition font-medium border border-gray-100 dark:border-gray-700">🔍 ${w}</a>`
                        ).join('');
                        
                        const exploreHtml = `
                            <div class="mt-8 pt-6 border-t border-gray-200 dark:border-gray-700">
                                <h4 class="text-lg font-bold mb-4 text-gray-800 dark:text-white flex items-center gap-2">🔗 Explore More (Wikipedia)</h4>
                                <div class="flex flex-wrap gap-2">
                                    ${wikiLinks}
                                </div>
                            </div>
                        `;
                        summaryContent.innerHTML += exploreHtml;
                    }
                }
"""
content = content.replace(wiki_logic_target, wiki_logic_replacement)


with open(index_path, "w", encoding="utf-8") as f:
    f.write(content)

print("index.html updated successfully!")
