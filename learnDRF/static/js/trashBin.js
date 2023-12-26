document.addEventListener('DOMContentLoaded', function() {
    const apiEndpoint = '/api/trash_bin/';
    const trashedNotesList = document.getElementById('trashed-notes-list');

    fetch(apiEndpoint, { method: 'GET', credentials: 'include' })
    .then(response => response.json())
    .then(notes => {
        notes.forEach(note => {
            const listItem = document.createElement('li');
            listItem.textContent = note.title;

            // Create the restore button
            const restoreButton = document.createElement('button');
            restoreButton.textContent = 'Restore';
            restoreButton.style.backgroundColor = 'blue'; // Set the button color to blue
            restoreButton.style.color = 'white'; // Text color white for better readability
            restoreButton.onclick = () => restoreNote(note.id);

            // Create the delete button
            const deleteButton = document.createElement('button');
            deleteButton.textContent = 'Delete Permanently';
            deleteButton.style.backgroundColor = 'red'; // Set the button color to red
            deleteButton.style.color = 'white'; // Text color white for better readability
            deleteButton.onclick = () => deleteNotePermanently(note.id);

            // Button container to align buttons to the right
            const buttonContainer = document.createElement('div');
            buttonContainer.style.display = 'flex';
            buttonContainer.style.gap = '10px'; // Adds a small space between buttons

            // Append buttons to the container
            buttonContainer.appendChild(restoreButton);
            buttonContainer.appendChild(deleteButton);

            // Append the text and button container to the list item
            listItem.appendChild(buttonContainer);

            // Append the list item to the list
            trashedNotesList.appendChild(listItem);
        });
    })
    .catch(error => console.error('Error fetching trashed notes:', error));
});

// 恢复笔记的函数
function restoreNote(noteId) {
    const restoreEndpoint = `api/restore_from_trash/${noteId}/`;
    fetch(restoreEndpoint, {
        method: 'POST',
        credentials: 'include'
    })
    .then(response => {
        if (response.ok) {
            alert('Note restored successfully');
            location.reload();  // 重新加载页面以更新列表
        } else {
            alert('Failed to restore the note');
        }
    })
    .catch(error => console.error('Error restoring note:', error));
}

// 永久删除笔记的函数
function deleteNotePermanently(noteId) {
    const deleteEndpoint = `/api/delete-note-permanently/${noteId}/`;
    fetch(deleteEndpoint, {
        method: 'DELETE',
        credentials: 'include'
    })
    .then(response => {
        if (response.ok) {
            alert('Note deleted permanently');
            location.reload();  // 重新加载页面以更新列表
        } else {
            alert('Failed to delete the note');
        }
    })
    .catch(error => console.error('Error deleting note:', error));
}
