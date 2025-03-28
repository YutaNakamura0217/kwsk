document.getElementById('contact-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = {
        companyName: document.getElementById('company-name').value,
        name: document.getElementById('name').value,
        email: document.getElementById('email').value,
        phone: document.getElementById('phone').value,
        category: document.getElementById('category').value,
        details: document.getElementById('details').value
    };

    console.log(formData);
});
