document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('create-notebook-form');

    form.addEventListener('submit', function(event) {
        event.preventDefault();  // 防止表單的默認提交行為

        const notebookName = document.getElementById('notebook-name').value;
        const notebooksContainer = document.getElementById('notebooks-container');
		
		const notebooksDataElement = document.getElementById('notebooks-api');	
		const apiEndpoint = notebooksDataElement.getAttribute('data-notebooks-api');

        fetch(apiEndpoint, {
            method: 'POST',
            credentials: 'include',  // 確保携带cookies (JWT Token)
            headers: {
                'Content-Type': 'application/json',
                // 如果使用Token，可能還需要在這裡添加Authorization頭
            },
            body: JSON.stringify({ name: notebookName })  // 將數據轉為JSON
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
            // 創建成功後，可以進行的操作，例如重定向或更新頁面列表
            console.log('Notebook created successfully:', data);
            alert('Notebook created successfully!');
            // 清空輸入字段
            document.getElementById('notebook-name').value = '';
        })
        .catch(error => {
            console.error('Error creating notebook:', error);
            alert('Error creating notebook');
        });
    });
});
