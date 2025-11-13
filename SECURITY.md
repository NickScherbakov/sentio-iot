# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| latest  | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

The Sentio IoT team takes security seriously. We appreciate your efforts to responsibly disclose your findings.

### How to Report

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report security vulnerabilities by emailing:

**[INSERT YOUR SECURITY EMAIL HERE]**

You should receive a response within 48 hours. If for some reason you do not, please follow up via email to ensure we received your original message.

Please include the following information in your report:

* Type of vulnerability (e.g., SQL injection, XSS, authentication bypass, etc.)
* Full paths of source file(s) related to the manifestation of the vulnerability
* The location of the affected source code (tag/branch/commit or direct URL)
* Any special configuration required to reproduce the issue
* Step-by-step instructions to reproduce the issue
* Proof-of-concept or exploit code (if possible)
* Impact of the issue, including how an attacker might exploit it

This information will help us triage your report more quickly.

### What to Expect

* **Acknowledgment**: We will acknowledge receipt of your vulnerability report within 48 hours
* **Initial Assessment**: We will provide an initial assessment within 5 business days
* **Updates**: We will keep you informed about our progress as we work on a fix
* **Fix Release**: Once the vulnerability is fixed, we will release a patch and publicly disclose the vulnerability
* **Credit**: We will credit you for the discovery in our release notes (unless you prefer to remain anonymous)

### Security Update Process

1. The security report is received and assigned to a primary handler
2. The problem is confirmed and a list of affected versions is determined
3. Code is audited to find any potential similar problems
4. Fixes are prepared for all supported releases
5. New versions are released as soon as possible
6. The vulnerability is publicly disclosed in the release notes

## Security Best Practices

When deploying Sentio IoT in production:

### Authentication & Authorization
* Change all default passwords immediately
* Use strong, unique passwords
* Rotate JWT secrets regularly
* Implement proper RBAC for your organization
* Use multi-factor authentication where available

### Network Security
* Enable TLS/HTTPS for all connections
* Use mTLS for service-to-service communication
* Restrict network access using firewalls
* Run services on private networks when possible
* Use VPNs for remote access

### Container Security
* Use official Docker images only
* Scan images for vulnerabilities regularly
* Run containers as non-root users
* Limit container capabilities
* Keep Docker and images up to date

### Data Protection
* Encrypt sensitive data at rest
* Encrypt data in transit
* Implement proper backup procedures
* Rotate credentials regularly
* Follow the principle of least privilege

### Monitoring & Auditing
* Enable audit logging
* Monitor for suspicious activity
* Set up security alerts
* Review logs regularly
* Keep security tools updated

### Configuration
* Use environment variables for secrets
* Never commit secrets to version control
* Use a secrets management system (e.g., HashiCorp Vault)
* Regularly review and update configurations
* Follow security hardening guides

## Known Security Considerations

### Default Credentials
The default deployment uses weak credentials for demonstration purposes:
* Username: `admin`
* Password: `admin`

**These MUST be changed before deploying to production.**

### JWT Secret
The default JWT secret key is `change-me-in-production`. This MUST be changed to a strong, random value in production deployments.

### Network Exposure
By default, several services expose ports. In production:
* Use a reverse proxy (nginx, Traefik, etc.)
* Only expose necessary ports
* Use proper firewall rules

## Security Scanning

We use the following tools to maintain security:

* **Dependabot**: Automated dependency updates
* **CodeQL**: Static code analysis
* **Container Scanning**: Docker image vulnerability scanning
* **SAST**: Static Application Security Testing

## Disclosure Policy

When we learn of a security vulnerability, we will:

1. Fix the vulnerability in private
2. Release a patch as quickly as possible
3. Publicly disclose the vulnerability after the patch is released
4. Credit the reporter (unless they prefer anonymity)

We ask security researchers to:

* Give us reasonable time to fix vulnerabilities before public disclosure
* Make a good faith effort to avoid privacy violations, data destruction, and service disruption
* Not exploit vulnerabilities beyond what is necessary to demonstrate the issue

## Bug Bounty Program

We currently do not have a formal bug bounty program. However, we deeply appreciate security researchers who responsibly disclose vulnerabilities and will:

* Publicly acknowledge your contribution (with permission)
* Add you to our security hall of fame
* Consider your contributions when evaluating future bug bounty programs

## Contact

For any security-related questions or concerns:

* Security issues: [INSERT SECURITY EMAIL]
* General questions: Open a GitHub issue
* Project maintainers: [INSERT MAINTAINER EMAIL]

## Additional Resources

* [OWASP Top 10](https://owasp.org/www-project-top-ten/)
* [CWE Top 25](https://cwe.mitre.org/top25/)
* [Docker Security Best Practices](https://docs.docker.com/engine/security/)
* [Kubernetes Security Best Practices](https://kubernetes.io/docs/concepts/security/)

---

Thank you for helping keep Sentio IoT and our users safe!
