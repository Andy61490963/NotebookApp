document.addEventListener('DOMContentLoaded', function() {
    // 動態創建刪除連結
    const deleteLink = document.createElement('a');
    deleteLink.href = "javascript:void(0)"; // 防止頁面跳轉
    deleteLink.classList.add('btn', 'btn-delete', 'delete-notebook');
    deleteLink.textContent = '刪除筆記本';
    
    // 添加到DOM中的某個元素
    const actionsDiv = document.getElementById('actions');
    actionsDiv.appendChild(deleteLink);

    // 獲取API和筆記本資訊
    const notebookId = /* 獲取筆記本ID */;
    const notebooksApi = /* 獲取API的基本URL */;
    const apiEndpoint = `${notebooksApi}/${notebookId}/`;

    // 添加點擊事件監聽器
    deleteLink.addEventListener('click', function() {
        if(confirm('確定要刪除這個筆記本嗎？')) {
            fetch(apiEndpoint, {
                method: 'DELETE',
                credentials: 'include'
            })
            .then(response => {
                if(response.ok) {
                    alert('筆記本已刪除！');
                    window.location.href = '/note'; // 或其他重定向頁面
                } else {
                    alert('刪除失敗！');
                }
            })
            .catch(error => console.error('Error deleting notebook:', error));
        }
    });
});
