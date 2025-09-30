// static/js/script.js

document.addEventListener('DOMContentLoaded', () => {
    // --- 1. Element References ---
    // Get all the HTML elements we will need to interact with.
    const analyzerForm = document.getElementById('analyzer-form');
    const extractBtn = document.getElementById('extract-btn');
    const skillConfirmationSection = document.getElementById('skill-confirmation-section');
    const skillCheckboxesContainer = document.getElementById('skill-checkboxes');
    const analyzeBtn = document.getElementById('analyze-btn');
    const resultsSection = document.getElementById('results-section');
    const feedbackSection = document.getElementById('feedback-section');
    const feedbackText = document.getElementById('feedback-text');
    const suggestionsSection = document.getElementById('suggestions-section');
    const courseListContainer = document.getElementById('course-list');
    const generalTipsList = document.getElementById('general-tips-list');
    const courseSuggestionsContainer = document.getElementById('course-suggestions');
    const generalTipsSuggestionsContainer = document.getElementById('general-tips-suggestions');

    // --- 2. Tab Switching & File Input Logic ---
    // This handles the "Upload File" / "Paste Text" tabs.
    document.querySelectorAll('.tab-btn').forEach(button => {
        button.addEventListener('click', () => {
            const group = button.dataset.for; // 'resume' or 'jd'
            const type = button.dataset.type; // 'file' or 'text'
            // Deactivate all buttons in the group, then activate the clicked one.
            document.querySelectorAll(`.tab-btn[data-for="${group}"]`).forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');
            // Hide all content blocks in the group, then show the relevant one.
            document.querySelectorAll(`.card:has(.tab-btn[data-for="${group}"]) .input-content`).forEach(content => content.classList.add('hidden'));
            document.getElementById(`${group}-${type}-content`).classList.remove('hidden');
        });
    });
    // This updates the file input label to show the selected filename.
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', () => {
            const labelSpan = document.querySelector(`span[data-for="${input.name}"]`);
            if (input.files.length > 0) labelSpan.textContent = `📄 ${input.files[0].name}`;
            else labelSpan.textContent = '📄 Choose a file...';
        });
    });

    // --- 3. Step 1: Handle Skill Extraction ---
    // This function is triggered when the "Extract Skills" button is clicked.
    analyzerForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent the page from reloading
        const formData = new FormData(analyzerForm);
        
        // Update UI to show loading state
        extractBtn.textContent = 'Extracting...';
        extractBtn.disabled = true;
        [skillConfirmationSection, resultsSection, feedbackSection, suggestionsSection].forEach(el => el.classList.add('hidden'));

        try {
            // Send resume data to the /extract endpoint
            const response = await fetch('/extract', { method: 'POST', body: formData });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Failed to extract skills.');
            
            // If successful, show the checkboxes for confirmation
            displaySkillCheckboxes(data.extracted_skills);
        } catch (error) {
            console.error('Extraction Error:', error);
            alert(`Could not extract skills: ${error.message}`);
        } finally {
            // Reset the button state
            extractBtn.textContent = 'Extract Skills';
            extractBtn.disabled = false;
        }
    });

    // --- 4. Display Skill Checkboxes ---
    // This function dynamically creates the checkbox list from the skills the backend found.
    function displaySkillCheckboxes(skills) {
        skillCheckboxesContainer.innerHTML = '';
        if (skills.length === 0) {
            skillCheckboxesContainer.innerHTML = '<p class="empty-state">No skills found in a dedicated section. Please check your resume format.</p>';
            analyzeBtn.classList.add('hidden');
        } else {
            skills.forEach(skill => {
                const label = document.createElement('label');
                label.className = 'checkbox-label';
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.value = skill;
                checkbox.checked = true;
                checkbox.name = 'confirmed_skills[]'; // Important for form submission
                label.appendChild(checkbox);
                label.appendChild(document.createTextNode(` ${skill}`));
                skillCheckboxesContainer.appendChild(label);
            });
            analyzeBtn.classList.remove('hidden');
        }
        skillConfirmationSection.classList.remove('hidden');
        skillConfirmationSection.scrollIntoView({ behavior: 'smooth' });
    }

    // --- 5. Step 2: Handle Final Analysis ---
    // This function is triggered when the "Analyze Match" button is clicked.
    analyzeBtn.addEventListener('click', async () => {
        analyzeBtn.textContent = 'Analyzing...';
        analyzeBtn.disabled = true;

        // Create a new FormData object to send to the backend.
        // It will contain all the original resume/JD data PLUS the confirmed skills.
        const finalFormData = new FormData(analyzerForm);
        finalFormData.delete('confirmed_skills[]'); // Clear any previous skill data
        const confirmedSkills = skillCheckboxesContainer.querySelectorAll('input:checked');
        if (confirmedSkills.length === 0) {
            alert('Please select at least one skill to analyze.');
            analyzeBtn.textContent = 'Analyze Match';
            analyzeBtn.disabled = false;
            return;
        }
        // Add only the skills the user has checked.
        confirmedSkills.forEach(skill => finalFormData.append('confirmed_skills[]', skill.value));

        try {
            // Send all data to the /analyze endpoint
            const response = await fetch('/analyze', { method: 'POST', body: finalFormData });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'Analysis failed.');

            // If successful, display the full report
            displayFinalResults(data);
        } catch (error) {
            console.error('Analysis Error:', error);
            alert(`Analysis failed: ${error.message}`);
        } finally {
            // Reset button state
            analyzeBtn.textContent = 'Analyze Match';
            analyzeBtn.disabled = false;
        }
    });

    // --- 6. Display Final Results ---
    // This function takes the final analysis object and populates the entire results UI.
    function displayFinalResults(data) {
        resultsSection.classList.remove('hidden');

        const createTags = (container, skills, type) => {
            container.innerHTML = '';
            if (skills.length > 0) {
                skills.forEach(skill => {
                    const tag = document.createElement('div');
                    tag.className = `tag ${type}-tag`;
                    tag.textContent = skill;
                    container.appendChild(tag);
                });
            } else {
                container.innerHTML = `<p class="empty-state" style="font-size: 0.8rem;">None</p>`;
            }
        };

        // Populate Box 1: JD Analysis
        document.getElementById('jd-score-value').textContent = `${data.jd_analysis.score}%`;
        document.getElementById('jd-score-circle').style.background = `conic-gradient(var(--primary-color) ${data.jd_analysis.score}%, var(--border-color) 0%)`;
        createTags(document.getElementById('jd-matched-skills'), data.jd_analysis.matched_skills, 'matched');
        createTags(document.getElementById('jd-missing-skills'), data.jd_analysis.missing_skills, 'missing');

        // Populate Box 2: Field Analysis
        document.getElementById('field-name-title').textContent = data.field_analysis.field_name;
        document.getElementById('field-score-value').textContent = `${data.field_analysis.score}%`;
        document.getElementById('field-score-circle').style.background = `conic-gradient(var(--primary-color) ${data.field_analysis.score}%, var(--border-color) 0%)`;
        createTags(document.getElementById('field-matched-skills'), data.field_analysis.matched_skills, 'matched');
        createTags(document.getElementById('field-missing-skills'), data.field_analysis.missing_skills, 'missing');

        // Populate Box 3: Best Match Analysis
        document.getElementById('best-match-field-name').textContent = data.best_match_analysis.field_name;
        document.getElementById('best-match-score-value').textContent = `${data.best_match_analysis.score}%`;
        document.getElementById('best-match-score-circle').style.background = `conic-gradient(var(--primary-color) ${data.best_match_analysis.score}%, var(--border-color) 0%)`;

        // Populate Quick Feedback Section
        feedbackText.innerHTML = '';
        if (data.feedback && data.feedback.points) {
            const list = document.createElement('ul');
            list.className = 'feedback-list';
            data.feedback.points.forEach(point => {
                const item = document.createElement('li');
                item.innerHTML = point; // Use innerHTML to render bold tags
                list.appendChild(item);
            });
            feedbackText.appendChild(list);
            feedbackSection.classList.remove('hidden');
        }

        // Populate Suggestions Section
        courseListContainer.innerHTML = '';
        if (data.suggestions.courses && data.suggestions.courses.length > 0) {
            data.suggestions.courses.forEach(course => {
                const courseEl = document.createElement('div');
                courseEl.className = 'suggestion-item';
                courseEl.innerHTML = `
                    <div class="suggestion-header">
                        <strong>${course.skill}</strong>
                        <a href="${course.course_link}" target="_blank" class="course-link">View Course ➔</a>
                    </div>
                    <p class="suggestion-body">${course.importance}</p>
                `;
                courseListContainer.appendChild(courseEl);
            });
            courseSuggestionsContainer.classList.remove('hidden');
        } else {
            courseSuggestionsContainer.classList.add('hidden');
        }

        generalTipsList.innerHTML = '';
        if (data.suggestions.general && data.suggestions.general.length > 0) {
            data.suggestions.general.forEach(tip => {
                const tipEl = document.createElement('li');
                tipEl.innerHTML = tip.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
                generalTipsList.appendChild(tipEl);
            });
            generalTipsSuggestionsContainer.classList.remove('hidden');
        } else {
            generalTipsSuggestionsContainer.classList.add('hidden');
        }
        
        // Only show the suggestions card if it has content
        if ((data.suggestions.courses && data.suggestions.courses.length > 0) || (data.suggestions.general && data.suggestions.general.length > 0)) {
            suggestionsSection.classList.remove('hidden');
        }

        // Scroll to the top of the report
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }
});

