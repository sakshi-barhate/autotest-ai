const API_URL = "https://autotest-ai-h360.onrender.com"

export async function generateTests(sourceCode) {
  const response = await fetch(`${API_URL}/generate-tests`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source_code: sourceCode }),
  })
  return response.json()
}

export async function runCoverage(sourceCode) {
  const response = await fetch(`${API_URL}/run-coverage`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ source_code: sourceCode }),
  })
  return response.json()
}