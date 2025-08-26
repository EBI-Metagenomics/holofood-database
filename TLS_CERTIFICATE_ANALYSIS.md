# TLS Certificate Handling Analysis for HoloFood Database

## Summary

The HoloFood Database repository follows a **infrastructure-level TLS termination** approach, where TLS certificates are not handled directly by the Django application but rather by external infrastructure components like load balancers and ingress controllers.

## Current TLS Certificate Handling

### 1. Application Level (Django)
- **No direct TLS handling**: The Django application runs on HTTP port 8000
- **Expects HTTPS externally**: Configuration assumes the application will be accessed via HTTPS
- **CSRF protection**: `CSRF_TRUSTED_ORIGINS` in `settings.py` includes both HTTP and HTTPS versions
- **External service URLs**: All configured external services use HTTPS endpoints

### 2. Kubernetes Deployment (EBI WebProd)

#### Ingress Configuration (`k8s-hl/holofood-ingress.yaml`)
```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: holofood-ingress
  namespace: holofood-hl-prod
  annotations:
    kubernetes.io/ingress.class: "nginx"
spec:
  rules:
    - host: www.holofooddata.org
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: holofood
                port:
                  number: 8000
```

**Missing TLS Configuration**: The ingress lacks TLS specification, which should typically include:
- `spec.tls` section
- Certificate references
- Secret names containing TLS certificates

#### Service Configuration
- Services expose port 8000 (HTTP only)
- No TLS configuration at service level
- Application container runs gunicorn on port 8000 without SSL parameters

#### Proxy Settings (`k8s-hl/holofood-configmap.yaml`)
```yaml
HTTP_PROXY: "http://hh-wwwcache.ebi.ac.uk:3128"
HTTPS_PROXY: "http://hh-wwwcache.ebi.ac.uk:3128"
```
- Configured for outbound connections through EBI's proxy infrastructure
- Used for external API calls to ENA, MGnify, MetaboLights, etc.

### 3. AWS Elastic Beanstalk Deployment
- **Infrastructure-managed TLS**: AWS Application Load Balancer handles TLS termination
- **No application-level SSL**: Django app runs on HTTP behind the load balancer
- **Certificate management**: Handled through AWS Certificate Manager (not in repository)

### 4. Local Development
- **HTTP only**: Local development runs on HTTP without TLS
- **No certificate requirements**: Uses localhost/127.0.0.1

## TLS Termination Architecture

```
Internet (HTTPS) → Load Balancer/Ingress (TLS Termination) → Service (HTTP) → Application (HTTP:8000)
```

### Production Flow:
1. External users access `https://www.holofooddata.org`
2. TLS is terminated at the infrastructure level (nginx ingress or AWS ALB)
3. Traffic is forwarded to the application over HTTP
4. Application responds over HTTP
5. Response is encrypted by infrastructure before reaching the user

## Identified Gaps

### 1. Missing Kubernetes TLS Configuration
The ingress configuration lacks TLS specification. A complete configuration would include:

```yaml
spec:
  tls:
    - hosts:
        - www.holofooddata.org
      secretName: holofood-tls-secret
```

### 2. No Certificate Management Documentation
- No documentation on how certificates are obtained/renewed
- No reference to certificate authorities used
- No mention of certificate storage (Kubernetes secrets)

### 3. No TLS Security Headers
The Django application could benefit from security middleware for:
- HTTP Strict Transport Security (HSTS)
- Secure cookie settings
- Content Security Policy (CSP)

## Recommendations

### 1. Complete Kubernetes TLS Configuration
Add TLS specification to the ingress configuration:

```yaml
spec:
  tls:
    - hosts:
        - www.holofooddata.org
      secretName: holofood-tls-secret
  rules:
    # existing rules
```

### 2. Add Django Security Settings
Consider adding to `settings.py`:

```python
# HTTPS Security Settings (when behind TLS-terminating proxy)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True  # Only if not handled by load balancer
USE_TLS = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### 3. Document Certificate Management Process
Create documentation covering:
- How certificates are obtained (Let's Encrypt, commercial CA, etc.)
- Certificate renewal process
- Emergency certificate replacement procedures
- Certificate monitoring and alerting

## External Dependencies

The application makes HTTPS requests to several external services:
- EBI BioSamples API (`https://www.ebi.ac.uk/biosamples`)
- ENA Portal API (`https://www.ebi.ac.uk/ena/portal/api`)
- MGnify API (`https://www.ebi.ac.uk/metagenomics/api/v1`)
- MetaboLights API (`https://www.ebi.ac.uk/metabolights/ws`)

These connections rely on:
- System CA bundle for certificate validation
- Proxy configuration for EBI deployments
- Python requests library's default SSL verification

## Conclusion

The HoloFood Database follows a standard cloud-native approach where TLS certificates are managed at the infrastructure level rather than within the application. This is a security best practice that:

1. **Centralizes certificate management**
2. **Reduces application complexity**
3. **Leverages infrastructure expertise**
4. **Enables certificate automation**

However, the repository could benefit from completing the TLS configuration in the Kubernetes manifests and adding appropriate Django security settings for production deployments.