``` bash
tuanlala@192:~/.gemini/antigravity/scratch/caldera-project$ curl -i -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer token....." \
  -d '{"name":"audit-test-repo", "description":"Tạo repo để làm bài tập audit"}' \
  https://api.github.com/user/repos
curl: (6) Could not resolve host:  
curl: (6) Could not resolve host:  
curl: (6) Could not resolve host:  
curl: (6) Could not resolve host:  
HTTP/2 201 
date: Fri, 18 Sep 2026 15:45:09 GMT
content-type: application/json; charset=utf-8
content-length: 6376
cache-control: private, max-age=60, s-maxage=60
vary: Accept, Authorization, Cookie, X-GitHub-OTP,Accept-Encoding, Accept, X-Requested-With
etag: "6ad7af13a400f7995afbf38c52eab698e12a75f4a485e0f07bbf66e88be406b5"
x-oauth-scopes: repo
x-accepted-oauth-scopes: public_repo, repo
github-authentication-token-expiration: 2026-10-03 11:43:41 UTC
location: https://api.github.com/repos/tuandq2056/audit-test-repo
x-github-media-type: github.v3; format=json
deprecation: Tue, 10 Mar 2026 00:00:00 GMT
sunset: Fri, 10 Mar 2028 00:00:00 GMT
link: <https://docs.github.com/en/rest/about-the-rest-api/api-versions>; rel="deprecation"; type="text/html"
x-github-api-version-selected: 2022-11-28
access-control-expose-headers: ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateLimit-Resource, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, X-GitHub-SSO, X-GitHub-Request-Id, Deprecation, Sunset, Warning
access-control-allow-origin: *
strict-transport-security: max-age=31536000; includeSubdomains; preload
x-frame-options: deny
x-content-type-options: nosniff
x-xss-protection: 0
referrer-policy: origin-when-cross-origin, strict-origin-when-cross-origin
content-security-policy: default-src 'none'
server: github.com
x-ratelimit-limit: 5000
x-ratelimit-remaining: 4995
x-ratelimit-reset: 1789748691
x-ratelimit-used: 5
x-ratelimit-resource: core
x-github-request-id: 5778:1FA3F6:58C5CCB:5C60E33:6AAD5C82
x-github-edge-region: southeastasia
```
