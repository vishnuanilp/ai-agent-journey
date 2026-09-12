from fetch1 import fetch

print("=== CASE 1: normal page ===")
r = fetch("https://example.com")
print("RESULT:", "response" if r else "None")
print()

print("=== CASE 2: 404, not retryable ===")
r = fetch("https://httpbin.org/status/404")
print("RESULT:", "response" if r else "None")
print()

print("=== CASE 3: 503, retryable ===")
r = fetch("https://httpbin.org/status/503")
print("RESULT:", "response" if r else "None")