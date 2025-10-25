# Security Policy

## Supported Versions

We release patches for security vulnerabilities in the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability in the Multi-Calendar Dimension Library, please follow these steps:

### 1. Do NOT create a public issue

Security vulnerabilities should be reported privately to avoid potential harm.

### 2. Email us directly

Send an email to: [security@yourdomain.com] (replace with actual email)

Include the following information:
- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if any)

### 3. Response timeline

- We will acknowledge receipt within 48 hours
- We will provide regular updates on our progress
- We aim to resolve critical vulnerabilities within 7 days
- We will coordinate the public disclosure timeline with you

### 4. Public disclosure

Once the vulnerability is fixed:
- We will release a security update
- We will credit you (unless you prefer to remain anonymous)
- We will update the CHANGELOG.md with security fixes

## Security Best Practices

When using this library:

1. **Keep dependencies updated**: Regularly update the library and its dependencies
2. **Validate inputs**: Always validate date inputs before processing
3. **Handle errors gracefully**: Don't expose sensitive information in error messages
4. **Use HTTPS**: When fetching data over the network, use secure connections

## Known Security Considerations

### Date Input Validation
- The library performs basic validation on date inputs
- Always validate user-provided dates before conversion
- Be aware of potential integer overflow in very large year values

### File Operations
- When using Excel/CSV export features, validate file paths
- Be cautious with user-provided file names to prevent path traversal

### Network Operations
- The astronomical calculations may require downloading ephemeris data
- Ensure secure connections when fetching external data

## Security Updates

Security updates will be released as patch versions (e.g., 1.0.1, 1.0.2) and will be clearly marked in the CHANGELOG.md.

## Contact

For security-related questions or concerns, please contact us at: [security@yourdomain.com]
