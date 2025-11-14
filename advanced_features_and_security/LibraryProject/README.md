This file contains contents on Managing Permissions and Groups

## 🚀 Features Implemented

- **Custom User Model**
  - Extended `AbstractUser` with `date_of_birth` and `profile_photo`.
  - Integrated with Django admin for management.
- **Permissions and Groups**
  - Custom permissions: `can_view`, `can_create`, `can_edit`, `can_delete`.
  - Groups: `Editors`, `Viewers`, `Admins` with role-based access control.
- **Security Best Practices**
  - CSRF protection with `{% csrf_token %}`.
  - Secure settings (`DEBUG=False`, `SESSION_COOKIE_SECURE`, `CSRF_COOKIE_SECURE`).
  - Protection against XSS, SQL injection, and clickjacking.
- **HTTPS and Secure Redirects**
  - Configured `SECURE_SSL_REDIRECT`, HSTS headers, and secure cookies.
