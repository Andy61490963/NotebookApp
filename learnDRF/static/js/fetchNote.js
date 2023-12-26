document.addEventListener('DOMContentLoaded', function() {
    const noteDataElement = document.getElementById('note-id');
    const note_Id = noteDataElement.getAttribute('data-note-id');
    
    const noteApiElement = document.getElementById('note-api');
    const notes_Api = noteApiElement.getAttribute('data-note-api');
    
    const apiEndpoint = `${notes_Api}/${note_Id}/`;
    
    const noteTitleElement = document.getElementById('note-title');
    const noteContentElement = document.getElementById('note-content');
    const newTitleInput = document.getElementById('new-title');  // 获取新标题的输入框
    const newContentTextarea = document.getElementById('new-content');  // 获取新内容的文本区域

    fetch(apiEndpoint, {
        method: 'GET',
        credentials: 'include'
    })
    .then(response => response.json())
    .then(data => {
        noteTitleElement.textContent = data.title;  
        const safeHtml = DOMPurify.sanitize(marked.parse(data.content));  
        noteContentElement.innerHTML = safeHtml;  
        
        newTitleInput.value = data.title; 
        newContentTextarea.value = data.content;  
    })
    .catch(error => console.error('Error fetching note:', error));
});
