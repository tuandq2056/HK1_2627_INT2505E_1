``` bash
tuanlala@192:~/.gemini/antigravity/scratch/caldera-project$ curl -i -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer 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" \
  https://api.github.com/repos/tuandq2056/audit-test-repo
curl: (6) Could not resolve host:  
curl: (6) Could not resolve host:  
curl: (6) Could not resolve host:  
HTTP/2 403 
date: Fri, 18 Sep 2026 15:52:12 GMT
content-type: application/json; charset=utf-8
content-length: 163
x-oauth-scopes: repo
x-accepted-oauth-scopes: delete_repo
github-authentication-token-expiration: 2026-10-03 11:43:41 UTC
x-github-media-type: github.v3; format=json
x-github-api-version-selected: 2022-11-28
access-control-expose-headers: ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateLimit-Resource, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, X-GitHub-SSO, X-GitHub-Request-Id, Deprecation, Sunset, Warning
access-control-allow-origin: *
strict-transport-security: max-age=31536000; includeSubdomains; preload
x-frame-options: deny
x-content-type-options: nosniff
x-xss-protection: 0
referrer-policy: origin-when-cross-origin, strict-origin-when-cross-origin
content-security-policy: default-src 'none'
vary: Accept-Encoding, Accept, X-Requested-With
server: github.com
x-ratelimit-limit: 5000
x-ratelimit-remaining: 4993
x-ratelimit-reset: 1789748691
x-ratelimit-used: 7
x-ratelimit-resource: core
x-github-request-id: 08AB:2C96C3:4B92BD7:4F3218C:6AAD5E2B
x-github-edge-region: southeastasia

{
  "message": "Must have admin rights to Repository.",
  "documentation_url": "https://docs.github.com/rest/repos/repos#delete-a-repository",
  "status": "403"
}
```
