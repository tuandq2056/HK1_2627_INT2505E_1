```bash
tuanlala@192:~/.gemini/antigravity/scratch/caldera-project$ curl -i -X GET \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/users/octocat/repos?per_page=2"


HTTP/2 200 
date: Fri, 18 Sep 2026 14:48:19 GMT

content-type: application/json; charset=utf-8

cache-control: public, max-age=60, s-maxage=60
vary: Accept,Accept-Encoding, Accept, X-Requested-With
etag: W/"22a6602a2a02e51cd9d05d80234d9e0ef1d3a29f4be1ac937ca30b48b08a935c"
x-github-media-type: github.v3; format=json


link: <https://api.github.com/user/583231/repos?per_page=2&page=2>; rel="next", <https://api.github.com/user/583231/repos?per_page=2&page=4>; rel="last"


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
accept-ranges: bytes
x-ratelimit-limit: 60
x-ratelimit-remaining: 57
x-ratelimit-used: 3
x-ratelimit-resource: core
x-ratelimit-reset: 1789744512
content-length: 11978
x-github-request-id: 4D14:23FF15:4305683:468B786:6AAD4F33
x-github-edge-region: southeastasia

```
