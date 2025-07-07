document.addEventListener('DOMContentLoaded', function() {
    if (typeof CKEDITOR !== 'undefined') {
        CKEDITOR.replace('id_content', {
            toolbar: [
                { name: 'basicstyles', items: ['Bold', 'Italic', 'Underline'] },
                { name: 'paragraph', items: ['NumberedList', 'BulletedList'] },
                { name: 'links', items: ['Link', 'Unlink'] },
                { name: 'tools', items: ['Maximize'] }
            ],
            height: 300
        });
    }

    document.querySelectorAll('.delete-news').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Вы уверены, что хотите удалить эту новость?')) {
                e.preventDefault();
            }
        });
    });

    document.querySelectorAll('.toggle-news-status').forEach(btn => {
        btn.addEventListener('click', function() {
            const newsId = this.dataset.newsId;
            const isPublished = this.checked;
            
            fetch(`/admin/toggle-news-status/${newsId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    is_published: isPublished
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const statusBadge = document.querySelector(`.news-status[data-news-id="${newsId}"]`);
                    if (statusBadge) {
                        statusBadge.className = `news-status status-${isPublished ? 'published' : 'draft'}`;
                        statusBadge.textContent = isPublished ? 'Опубликовано' : 'Черновик';
                    }
                } else {
                    this.checked = !isPublished;
                    alert('Ошибка при обновлении статуса');
                }
            });
        });
    });
});