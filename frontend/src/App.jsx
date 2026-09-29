import { useState } from 'react'
import { generateTests, runCoverage } from './api'

function App() {
  const [code, setCode] = useState('')
  const [testData, setTestData] = useState(null)
  const [coverage, setCoverage] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleGenerate = async () => {
    setLoading(true)
    setTestData(null)
    setCoverage(null)
    setError(null)

    const genResult = await generateTests(code)
    console.log("genResult:", genResult)

    if (genResult.error) {
      setError(genResult.error)
      setLoading(false)
      return
    }

    setTestData(genResult.test_data)

    const covResult = await runCoverage(code)
    console.log("covResult:", covResult)

    if (covResult.error) {
      setError(covResult.error)
      setLoading(false)
      return
    }

    setCoverage(covResult)
    setLoading(false)
    console.log("Done - loading set to false")
  }

  const handleTrySample = () => {
    setCode(`def calculate_discount(price: float, discount_percent: float) -> float:
    if discount_percent < 0 or discount_percent > 100:
        raise ValueError("Invalid discount percentage")
    if price < 0:
        raise ValueError("Price cannot be negative")
    return price - (price * discount_percent / 100)`)
  }

  return (
    <div className="min-h-screen bg-pink-50 flex flex-col items-center px-6 py-12">
      <h1 className="text-4xl font-bold text-pink-600 mb-2">AutoTest AI</h1>
      <p className="text-gray-600 mb-8">Paste your Python function and generate real test cases</p>

      <div className="w-full max-w-2xl bg-white rounded-2xl shadow-md p-6 border border-pink-100">
        <div className="flex justify-end mb-2">
          <button
            onClick={handleTrySample}
            className="text-sm text-pink-600 hover:text-pink-700 font-medium underline"
          >
            Try sample code
          </button>
        </div>

        <textarea
          value={code}
          onChange={(e) => setCode(e.target.value)}
          placeholder="def your_function(param: type) -> type:&#10;    ..."
          className="w-full h-64 font-mono text-sm p-4 rounded-lg border border-gray-200 focus:outline-none focus:ring-2 focus:ring-pink-400 resize-none"
        />

        <button
          onClick={handleGenerate}
          disabled={loading || !code}
          className="mt-4 w-full bg-pink-600 hover:bg-pink-700 disabled:bg-pink-300 text-white font-semibold py-3 rounded-lg transition"
        >
          {loading ? "Generating..." : "Generate Tests"}
        </button>
      </div>

      {error && (
        <div className="w-full max-w-2xl bg-red-50 border border-red-200 rounded-2xl p-4 mt-6">
          <p className="text-red-600 font-medium">{error}</p>
        </div>
      )}

      {coverage && (
        <div className="w-full max-w-2xl bg-white rounded-2xl shadow-md p-6 border border-pink-100 mt-6">
          <h2 className="text-xl font-bold text-pink-600 mb-2">Coverage Result</h2>
          <p className="text-gray-700">Coverage: <span className="font-bold">{coverage.percent_covered}%</span></p>
          <p className="text-gray-700">Lines covered: {coverage.lines_covered} / {coverage.num_statements}</p>
        </div>
      )}

      {testData && (
        <div className="w-full max-w-2xl bg-white rounded-2xl shadow-md p-6 border border-pink-100 mt-6">
          <h2 className="text-xl font-bold text-pink-600 mb-4">Generated Test Cases</h2>
          {testData.test_cases.map((tc, i) => (
            <div key={i} className="mb-3 pb-3 border-b border-gray-100 last:border-0">
              <p className="font-semibold text-gray-800">{tc.name} <span className="text-xs text-pink-500 uppercase">{tc.type}</span></p>
              <p className="text-sm text-gray-500">{tc.expected_behavior}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default App