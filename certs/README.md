# Certificates Directory

Store TLS/SSL certificates here for secure communication.

For development, you can generate self-signed certificates:

```bash
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout key.pem \
  -out cert.pem
```

For production, use certificates from a trusted CA (e.g., Let's Encrypt).

**Never commit private keys to the repository!**
