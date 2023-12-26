document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('update-note-form');

    // 从data属性中获取笔记ID和API端点
    const noteId = document.getElementById('note-id').getAttribute('data-note-id');
    const notesApi = document.getElementById('note-api').getAttribute('data-note-api');
    const apiEndpoint = `${notesApi}/${noteId}/`;

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // 阻止表单的默认提交行为

        // 获取用户输入的新标题和内容
        const newTitle = document.getElementById('new-title').value;
        const newContent = document.getElementById('new-content').value;

        // 构建要发送的数据
        const updatedData = {
            title: newTitle,
            content: newContent
        };

        // 发送PUT请求到API以更新笔记
        fetch(apiEndpoint, {
            method: 'PUT',
            credentials: 'include',  // 确保携带cookies (JWT Token)
            headers: {
                'Content-Type': 'application/json',
                // 如果使用Token，可能还需要在这里添加Authorization头
            },
            body: JSON.stringify(updatedData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }

            return response.json(); // 解析JSON数据
        })
        .then(data => {
            // 更新成功后，刷新页面以显示最新内容
            window.location.reload();
        })
        .catch(error => {
            console.error('Error', error);
            alert('Error');
        });
    });
});
