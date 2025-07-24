// Динамическая загрузка полей формы для генератора документов
function loadTemplateFields(templateId) {
    if (!templateId) return;
    
    fetch(`/api/template/${templateId}/fields/`)
        .then(response => response.json())
        .then(data => {
            const fieldsContainer = document.getElementById('template-fields');
            fieldsContainer.innerHTML = '';
            
            data.fields.forEach(field => {
                const fieldDiv = document.createElement('div');
                fieldDiv.className = 'mb-3';
                fieldDiv.innerHTML = `
                    <label for="${field.name}" class="form-label">${field.label}</label>
                    <input type="text" class="form-control" id="${field.name}" name="${field.name}" required>
                `;
                fieldsContainer.appendChild(fieldDiv);
            });
        })
        .catch(error => console.error('Error loading template fields:', error));
}

// Предварительный просмотр документа
function previewDocument() {
    const form = document.getElementById('document-form');
    const formData = new FormData(form);
    
    fetch('/documents/preview/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        const previewContainer = document.getElementById('document-preview');
        previewContainer.innerHTML = data.preview;
        previewContainer.style.display = 'block';
    })
    .catch(error => console.error('Error previewing document:', error));
}
