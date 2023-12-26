document.addEventListener('DOMContentLoaded', function() {
    const notebooksContainer = document.getElementById('notebooks-container');
    const notebooksDataElement = document.getElementById('notebooks-api');    
    const apiEndpoint = notebooksDataElement.getAttribute('data-notebooks-api');

    fetch(apiEndpoint, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(notebooks => {
        notebooks.forEach(notebook => {
            const notebookElement = document.createElement('div');
            notebookElement.classList.add('notebook');

            // Create a header section for the notebook title and action buttons
            const headerSection = document.createElement('div');
            headerSection.classList.add('notebook-header');

            // Notebook title
            const title = document.createElement('h2');
            title.textContent = notebook.name;
            headerSection.appendChild(title);

            // Actions div for the buttons
            const actionsDiv = document.createElement('div');
            actionsDiv.classList.add('actions');
			
			const updateLink = document.createElement('a');
            updateLink.href = `/createnote/${notebook.id}`;  // Set the href to the update URL
            updateLink.classList.add('btn', 'btn-update');
            updateLink.textContent = 'Post';
            actionsDiv.appendChild(updateLink);
            

            // Delete button
            const deleteLink = document.createElement('a');
            deleteLink.classList.add('btn', 'btn-delete', 'delete-note');
            deleteLink.textContent = 'Delete';
            deleteLink.setAttribute('data-notebook-id', notebook.id);  // Set the notebook ID as data attribute
            actionsDiv.appendChild(deleteLink);

			// Add click event listener for delete button
            deleteLink.addEventListener('click', function(event) {
                event.preventDefault();
                if (confirm(`Are you sure you want to delete the notebook "${notebook.name}"?`)) {
                    deleteNotebook(notebook.id);
                }
            });

            // Append actions to the header
            headerSection.appendChild(actionsDiv);

            // Append the header section to the notebook element
            notebookElement.appendChild(headerSection);

            const notesList = document.createElement('ul');
            notebook.notes.forEach(note => {
                const noteLink = document.createElement('a');
                noteLink.href = `/note/${note.id}/`;
                noteLink.textContent = note.title;
                noteLink.classList.add('note');
                
                const noteItem = document.createElement('li');
                noteItem.appendChild(noteLink);
                notesList.appendChild(noteItem);
            });

            notebookElement.appendChild(notesList);
            notebooksContainer.appendChild(notebookElement);
        });
    })
    .catch(error => console.error('Error fetching notebooks:', error));
});

function deleteNotebook(notebookId) {
    const deleteEndpoint = `/api/notebooks/${notebookId}/`;  // Adjust if your delete API endpoint is different

    fetch(deleteEndpoint, {
        method: 'DELETE',
        credentials: 'include'
    })
    .then(response => {
        if (response.ok) {
            // Remove the notebook element from the DOM
            document.querySelector(`[data-notebook-id="${notebookId}"]`).closest('.notebook').remove();
            alert('Notebook deleted successfully.');
        } else {
            alert('Failed to delete the notebook. Please try again.');
        }
    })
    .catch(error => console.error('Error deleting notebook:', error));
}