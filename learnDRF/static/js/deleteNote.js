document.addEventListener('DOMContentLoaded', function() {
	const noteDataElement = document.getElementById('note-id');
    const note_Id = noteDataElement.getAttribute('data-note-id');
	
    const noteApiElement = document.getElementById('note-api');
    const notes_Api = noteApiElement.getAttribute('data-note-api');
	
    const apiEndpoint = `${notes_Api}/${note_Id}/`;
	console.log(apiEndpoint)
    const deleteButton = document.getElementById('delete-note');

    deleteButton.addEventListener('click', function() {
        if(confirm('Are you sure you want to delete this note?')) {
            fetch(apiEndpoint, {
                method: 'DELETE',
                credentials: 'include'
            })
            .then(response => {
                if(response.ok) {
                    alert('The note have been deleted！');
                    window.location.href = '/note'; 
                } else {
                    alert('Error！');
                }
            })
            .catch(error => console.error('Error deleting note:', error));
        }
    });
});
