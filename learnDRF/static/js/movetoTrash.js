document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('move-to-trash').onclick = function() {
        const noteId = document.getElementById('note-id').getAttribute('data-note-id');
        fetch(`/api/move_to_trash/${noteId}/`, { method: 'POST' })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok. Status: ' + response.status);
                }
				else {
					window.location.href = `/note`;
				}
                return response.json();
            })
            
    };
});
