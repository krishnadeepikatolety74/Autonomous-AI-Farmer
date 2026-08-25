async function deleteTask(taskId) {
    if (!confirm("Are you sure you want to delete this scheduled task?")) return;

    try {
        const resp = await fetch(`/calendar/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const data = await resp.json();
        if (data.success) {
            // Find and remove task DOM row
            const row = document.querySelector(`.task-row[data-id="${taskId}"]`);
            if (row) {
                row.remove();
                
                // Update pending count if incomplete
                const checkbox = row.querySelector('input[type="checkbox"]');
                if (checkbox && !checkbox.checked) {
                    const countEl = document.getElementById("pending-count");
                    if (countEl) {
                        let val = parseInt(countEl.textContent, 10);
                        if (!isNaN(val) && val > 0) {
                            countEl.textContent = val - 1;
                        }
                    }
                }

                // If tasks container is empty, show fallback reload link
                const list = document.getElementById("tasks-list-container");
                if (list && list.children.length === 0) {
                    location.reload();
                }
            }
        } else {
            alert(data.message || "Failed to delete task.");
        }
    } catch (err) {
        console.error("Delete task failed:", err);
        alert("Connection error deleting task.");
    }
}
