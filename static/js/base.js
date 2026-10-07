// Helper function to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Clear all cookies
function clearCookies() {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf('=');
        const name = eqPos > -1 ? cookie.substr(0, eqPos).trim() : cookie.trim();
        document.cookie = name + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/';
    }
}

// Log out and redirect
function logout() {
    clearCookies();
    window.location.href = '/auth/login-page';
}
window.logout = logout;

document.addEventListener('DOMContentLoaded', function () {
    // Add Todo JS
    const todoForm = document.getElementById('todoForm');
    if (todoForm) {
        todoForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            const payload = {
                title: data.title,
                description: data.description,
                priority: parseInt(data.priority),
                complete: false
            };

            try {
                const response = await fetch('/todo/create_todo', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getCookie('access_token')}`
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    form.reset(); // Clear the form
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail || errorData.message || 'Failed to create todo'}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }

    // Edit Todo JS
    const editTodoForm = document.getElementById('editTodoForm');
    if (editTodoForm) {
        editTodoForm.addEventListener('submit', async function (event) {
            event.preventDefault();
            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());
            const url = window.location.pathname;
            const todoId = url.substring(url.lastIndexOf('/') + 1);

            const payload = {
                title: data.title,
                description: data.description,
                priority: parseInt(data.priority),
                complete: data.complete === 'on'
            };

            try {
                const token = getCookie('access_token');
                if (!token) {
                    throw new Error('Authentication token not found');
                }

                const response = await fetch(`/todo/update_todo/${todoId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    window.location.href = '/todo/todo-page';
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail || errorData.message || 'Failed to update todo'}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });

        const deleteButton = document.getElementById('deleteButton');
        if (deleteButton) {
            deleteButton.addEventListener('click', async function () {
                const url = window.location.pathname;
                const todoId = url.substring(url.lastIndexOf('/') + 1);

                try {
                    const token = getCookie('access_token');
                    if (!token) {
                        throw new Error('Authentication token not found');
                    }

                    const response = await fetch(`/todo/delete_todo/${todoId}`, {
                        method: 'DELETE',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (response.ok) {
                        window.location.href = '/todo/todo-page';
                    } else {
                        const errorData = await response.json();
                        alert(`Error: ${errorData.detail || errorData.message || 'Failed to delete todo'}`);
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('An error occurred. Please try again.');
                }
            });
        }
    }

    // Login JS
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);

            const payload = new URLSearchParams();
            for (const [key, value] of formData.entries()) {
                payload.append(key, value);
            }

            try {
                const response = await fetch('/auth/token', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded'
                    },
                    body: payload.toString()
                });

                if (response.ok) {
                    const data = await response.json();
                    clearCookies();
                    document.cookie = `access_token=${data.access_token}; path=/`;
                    window.location.href = '/todo/todo-page';
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.detail || errorData.message || 'Authentication failed'}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }

    // Register JS
    const registerForm = document.getElementById('registerForm');
    if (registerForm) {
        registerForm.addEventListener('submit', async function (event) {
            event.preventDefault();

            const form = event.target;
            const formData = new FormData(form);
            const data = Object.fromEntries(formData.entries());

            if (data.password !== data.password2) {
                alert('Passwords do not match');
                return;
            }

            const payload = {
                email: data.email,
                username: data.username,
                first_name: data.firstname,
                last_name: data.lastname,
                role: data.role,
                phone_number: data.phone_number,
                password: data.password
            };

            try {
                const response = await fetch('/auth/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(payload)
                });

                if (response.ok) {
                    window.location.href = '/auth/login-page';
                } else {
                    const errorData = await response.json();
                    let errorMsg = 'Registration failed.';
                    if (typeof errorData.detail === 'string') {
                        errorMsg = errorData.detail;
                    } else if (Array.isArray(errorData.detail)) {
                        errorMsg = errorData.detail.map(e => e.msg).join(', ');
                    } else if (errorData.message) {
                        errorMsg = errorData.message;
                    }
                    alert(`Error: ${errorMsg}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred. Please try again.');
            }
        });
    }
});