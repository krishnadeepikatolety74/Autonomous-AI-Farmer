/**
 * Farm Quick Notes JavaScript Controller
 * Handles checklist interaction dynamically.
 */

document.addEventListener("DOMContentLoaded", () => {
    const notesList = document.getElementById("quick-notes-list");
    const inputField = document.getElementById("quick-note-input");
    const addBtn = document.getElementById("quick-note-add-btn");
    const clearBtn = document.getElementById("quick-notes-clear-btn");
    const countSpan = document.getElementById("quick-notes-count");

    if (!notesList) return; // Exit if component is not loaded on page

    // Fetch initial notes on load
    loadNotes();

    // Bind event listeners
    if (addBtn) {
        addBtn.addEventListener("click", handleAddNote);
    }
    if (inputField) {
        inputField.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                handleAddNote();
            }
        });
    }
    if (clearBtn) {
        clearBtn.addEventListener("click", handleClearCompleted);
    }

    // ── Function Implementations ──

    async function loadNotes() {
        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/quick-notes`);
            const data = await resp.json();

            if (data.success) {
                renderNotes(data.notes);
            } else {
                notesList.innerHTML = `<div style="color: var(--red-alert); font-size: 13px; text-align: center; padding: 12px;">Failed to load notes.</div>`;
            }
        } catch (err) {
            console.error("Error loading quick notes:", err);
            notesList.innerHTML = `<div style="color: var(--red-alert); font-size: 13px; text-align: center; padding: 12px;">Connection error loading notes.</div>`;
        }
    }

    function renderNotes(notes) {
        notesList.innerHTML = "";
        
        if (!notes || notes.length === 0) {
            notesList.innerHTML = `<div style="text-align: center; color: var(--text-secondary); font-size: 13px; padding: 24px 0;">No active notes. Try adding one above!</div>`;
            if (countSpan) countSpan.textContent = "0 items";
            return;
        }

        let incompleteCount = 0;

        notes.forEach(note => {
            if (!note.completed) incompleteCount++;

            const itemDiv = document.createElement("div");
            itemDiv.className = `quick-note-item ${note.completed ? 'completed' : ''}`;
            itemDiv.dataset.id = note.id;

            // Note checkmark + label left pane
            const leftPane = document.createElement("div");
            leftPane.className = "quick-note-item-left";
            
            const checkbox = document.createElement("span");
            checkbox.className = "quick-note-checkbox";
            checkbox.innerHTML = "✓";
            
            const textSpan = document.createElement("span");
            textSpan.className = "quick-note-text";
            textSpan.textContent = note.note;

            leftPane.appendChild(checkbox);
            leftPane.appendChild(textSpan);

            // Bind complete click event
            leftPane.addEventListener("click", () => handleToggleComplete(note.id, note.completed));

            // Delete button right pane
            const deleteBtn = document.createElement("button");
            deleteBtn.className = "quick-note-delete-btn";
            deleteBtn.innerHTML = "&times;";
            deleteBtn.title = "Delete Note";
            deleteBtn.addEventListener("click", (e) => {
                e.stopPropagation(); // prevent triggering complete
                handleDeleteNote(note.id);
            });

            itemDiv.appendChild(leftPane);
            itemDiv.appendChild(deleteBtn);
            notesList.appendChild(itemDiv);
        });

        if (countSpan) {
            countSpan.textContent = `${incompleteCount} active items`;
        }
    }

    async function handleAddNote() {
        const val = inputField.value.trim();
        if (!val) return;

        if (val.length > 200) {
            alert("Note content cannot exceed 200 characters.");
            return;
        }

        // Disable input during post
        inputField.disabled = true;
        if (addBtn) addBtn.disabled = true;

        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/quick-notes`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({ note: val })
            });
            const data = await resp.json();

            if (data.success) {
                inputField.value = "";
                loadNotes();
            } else {
                alert(data.error || "Failed to create note.");
            }
        } catch (err) {
            console.error("Error creating note:", err);
            alert("Connection error creating note.");
        } finally {
            inputField.disabled = false;
            if (addBtn) addBtn.disabled = false;
            inputField.focus();
        }
    }

    async function handleToggleComplete(id, currentCompleted) {
        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/quick-notes/${id}/complete`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({ completed: !currentCompleted })
            });
            const data = await resp.json();

            if (data.success) {
                loadNotes();
            }
        } catch (err) {
            console.error("Error completing note:", err);
        }
    }

    async function handleDeleteNote(id) {
        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/quick-notes/${id}`, {
                method: "DELETE",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });
            const data = await resp.json();

            if (data.success) {
                loadNotes();
            }
        } catch (err) {
            console.error("Error deleting note:", err);
        }
    }

    async function handleClearCompleted() {
        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/quick-notes/clear-completed`, {
                method: "POST",
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            });
            const data = await resp.json();

            if (data.success) {
                loadNotes();
            }
        } catch (err) {
            console.error("Error clearing completed:", err);
        }
    }
});
