document.addEventListener('DOMContentLoaded', function() {
    // 获取表单和输入元素
    const form = document.getElementById('post-note-form');
    const titleInput = document.getElementById('new-title');
    const contentInput = document.getElementById('new-content');
    const notebookId = document.getElementById('notebook-id').getAttribute('data-note-id');
	
	const noteId = document.getElementById('notebook-id').getAttribute('data-notebook-id');
    const notesApi = document.getElementById('createnotes-api').getAttribute('data-createnotes-api');
	console.log(notesApi)

    // 获取API端点
    const apiEndpoint = `${notesApi}${noteId}/notes/`;

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // 防止表单的默认提交行为

        // 获取用户输入的标题和内容
        const title = titleInput.value.trim();
        const content = contentInput.value.trim();

        // 确保标题和内容不为空
        if (!title || !content) {
            alert("Please fill in both the title and content.");
            return;
        }

        // 准备请求数据
        const noteData = {
            title: title,
            content: content
        };

        // 发送POST请求到API
        fetch(apiEndpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // 如果需要，在此处添加Authorization头
            },
            body: JSON.stringify(noteData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
			else{
				window.location.href = '/note'; 
			}
            return response.json();
        })
        .then(data => {
            console.log('Note created successfully:', data);
            alert('Note created successfully!');
            // 清空表单
            titleInput.value = '';
            contentInput.value = '';
        })
        .catch(error => {
            console.error('Error creating note:', error);
            alert('Error creating note');
        });
    });
});
