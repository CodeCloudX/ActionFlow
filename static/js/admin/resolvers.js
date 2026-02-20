// Modal functionality
const modal = document.getElementById('resolverModal');
const openModalBtn = document.getElementById('openModalBtn');
const closeModalBtns = document.querySelectorAll('.close-modal, .btn-cancel');
const form = document.getElementById('resolverForm');
const modalTitle = document.getElementById('modalTitle');
const resolverIdInput = document.getElementById('resolverId');
const addResolverUrl = openModalBtn.dataset.addUrl;
const editResolverUrl = openModalBtn.dataset.editUrl;

// Open modal for adding new resolver
openModalBtn.addEventListener('click', () => {
    modalTitle.textContent = 'Add New Resolver';
    form.reset();
    resolverIdInput.value = '';
    form.action = addResolverUrl;
    modal.style.display = 'block';
});

// Open modal for editing resolver
document.querySelectorAll('.edit-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        modalTitle.textContent = 'Edit Resolver';

        resolverIdInput.value = btn.dataset.id;
        document.getElementById('name').value = btn.dataset.name;
        document.getElementById('email').value = btn.dataset.email;
        document.getElementById('category').value = btn.dataset.category;

        form.action = editResolverUrl.replace('0', btn.dataset.id);

        modal.style.display = 'block';
    });
});

// Close modal
closeModalBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        modal.style.display = 'none';
    });
});

// Close modal when clicking outside
window.addEventListener('click', (event) => {
    if (event.target === modal) {
        modal.style.display = 'none';
    }
});

// Handle form submission
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        });

        const result = await response.json();

        if (result.success) {
            window.location.reload();
        } else {
            alert(result.message || 'An error occurred');
        }
    } catch (error) {
        console.error('Error:', error);
        alert('An error occurred while saving the resolver');
    }
});
