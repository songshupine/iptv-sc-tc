"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Play, ExternalLink, Zap, Copy, Check, Gauge, FileJson, RefreshCw } from "lucide-react"

interface ApiEndpoint {
  name: string
  method: string
  path: string
  description: string
  body?: object
}

const endpoints: ApiEndpoint[] = [
  {
    name: "Info",
    method: "GET",
    path: "/api/info",
    description: "Returns FastAPI app metadata with Pydantic response model",
  },
  {
    name: "Get User",
    method: "GET",
    path: "/api/users/42",
    description: "Fetch user by typed path param (user_id: int)",
  },
  {
    name: "Create User",
    method: "POST",
    path: "/api/users",
    description: "Create user with Pydantic UserCreate model validation",
    body: { username: "alice", email: "alice@example.com" },
  },
  {
    name: "Search",
    method: "GET",
    path: "/api/search?q=fastapi&limit=3",
    description: "Search with Query() params — includes ge/le validation",
  },
]

export default function Home() {
  const [results, setResults] = useState<Record<string, { data: string; status: number } | null>>({})
  const [loadingStates, setLoadingStates] = useState<Record<string, boolean>>({})
  const [copied, setCopied] = useState(false)

  const handleApiCall = async (endpoint: ApiEndpoint) => {
    const key = `${endpoint.method}:${endpoint.path}`
    setLoadingStates(prev => ({ ...prev, [key]: true }))
    const options: RequestInit = {
      method: endpoint.method,
      headers: { "Content-Type": "application/json" },
    }
    if (endpoint.body) {
      options.body = JSON.stringify(endpoint.body)
    }
    const response = await fetch(endpoint.path, options)
    const data = await response.json()
    setResults(prev => ({
      ...prev,
      [key]: { data: JSON.stringify(data, null, 2), status: response.status },
    }))
    setLoadingStates(prev => ({ ...prev, [key]: false }))
  }

  const handleCopy = () => {
    navigator.clipboard.writeText(codeExample)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const codeExample = `from fastapi import FastAPI
from pydantic import BaseModel
import time

app = FastAPI()

class UserCreate(BaseModel):
    name: str
    email: str

@app.get("/")
async def root():
    return {
        "message": "Hello from FastAPI Cloud Function!",
        "framework": "FastAPI",
        "timestamp": time.time()
    }

@app.post("/users")
async def create_user(user: UserCreate):
    return {"id": 1, **user.dict()}`

  return (
    <div className="min-h-screen bg-black text-white relative overflow-hidden">
      {/* Background Gradient Orbs - FastAPI Teal */}
      <div className="gradient-orb gradient-orb-primary w-[600px] h-[600px] -top-[200px] -left-[150px] animate-pulse-glow" />
      <div className="gradient-orb gradient-orb-secondary w-[500px] h-[500px] top-[30%] -right-[100px] animate-pulse-glow animation-delay-200" />
      <div className="gradient-orb gradient-orb-primary w-[350px] h-[350px] bottom-[15%] left-[25%] animate-pulse-glow animation-delay-400" />

      {/* Pulse Rings */}
      <div className="pulse-ring w-[300px] h-[300px] top-[20%] left-[10%]" />
      <div className="pulse-ring w-[200px] h-[200px] top-[50%] right-[15%] animation-delay-100" />

      {/* Lightning Bolt Decorations */}
      <svg className="lightning-bolt w-[80px] h-[150px] top-[15%] right-[20%]" viewBox="0 0 24 24" fill="currentColor">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
      </svg>
      <svg className="lightning-bolt w-[60px] h-[120px] bottom-[25%] left-[8%] animation-delay-200" viewBox="0 0 24 24" fill="currentColor">
        <path d="M13 2L3 14h9l-1 8 10-12h-9l1-8z"/>
      </svg>

      {/* Header */}
      <header className="header-border relative z-10">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-end">
            <a
              href="https://github.com/TencentEdgeOne/python-fastapi-template"
              target="_blank"
              rel="noopener noreferrer"
              className="icon-glow text-gray-400 hover:text-[#00BFA5] transition-colors p-2"
              aria-label="GitHub"
            >
              <svg className="w-6 h-6" fill="currentColor" viewBox="0 0 24 24" aria-hidden="true">
                <path fillRule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clipRule="evenodd" />
              </svg>
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-6 py-16 relative z-10">
        <div className="max-w-4xl mx-auto text-center space-y-12">
          {/* Hero Section */}
          <div className="space-y-6 animate-fade-in-up">
            {/* Title */}
            <h1 className="text-5xl md:text-6xl font-bold leading-tight">
              <span className="bg-clip-text text-transparent bg-gradient-to-r from-[#00BFA5] via-[#009688] to-white">
                FastAPI
              </span>
              <span className="text-white/80"> + EdgeOne Pages</span>
            </h1>

            {/* Subtitle */}
            <p className="text-xl text-gray-400 max-w-3xl mx-auto leading-relaxed">
              High performance, easy to learn, fast to code, ready for production.
              <span className="text-[#00BFA5]"> Modern</span>,
              <span className="text-[#009688]"> async</span>,
              <span className="text-white/90"> blazing fast</span>.
            </p>
          </div>

          {/* Action Buttons */}
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center animate-fade-in-up animation-delay-100">
            <a href="https://edgeone.ai/pages/new?from=github&template=python-fastapi-template" target="_blank" rel="noopener noreferrer">
              <Button size="lg" className="btn-primary px-8 py-6 text-lg rounded-xl cursor-pointer">
                <Zap className="w-5 h-5 mr-2" />
                One-Click Deployment
              </Button>
            </a>
            <a href="https://pages.edgeone.ai/document/python" target="_blank" rel="noopener noreferrer">
              <Button variant="outline" size="lg" className="btn-outline px-8 py-6 text-lg rounded-xl cursor-pointer">
                <ExternalLink className="w-5 h-5 mr-2" />
                View Documentation
              </Button>
            </a>
          </div>

          {/* Code Block */}
          <div className="code-block text-left animate-fade-in-up animation-delay-200">
            <div className="code-block-header">
              <Zap className="w-5 h-5 text-[#00BFA5]" />
              <span className="text-sm font-mono text-gray-400 flex-1">
                cloud-functions/api/[[default]].py
              </span>
              <button 
                onClick={handleCopy}
                className="p-1.5 rounded-md hover:bg-[#00BFA5]/10 transition-colors cursor-pointer"
                aria-label="Copy code"
              >
                {copied ? (
                  <Check className="w-4 h-4 text-[#00BFA5]" />
                ) : (
                  <Copy className="w-4 h-4 text-gray-400" />
                )}
              </button>
            </div>
            <pre className="text-sm text-gray-200 font-mono leading-relaxed p-4 overflow-x-auto">
              <code>{codeExample}</code>
            </pre>
          </div>

          {/* API Endpoints */}
          <div className="space-y-4 animate-fade-in-up animation-delay-300">
            <h2 className="text-lg font-semibold text-gray-300 pb-2 border-b border-[#00BFA5]/20">
              API Endpoints
            </h2>
            {endpoints.map(endpoint => {
              const key = `${endpoint.method}:${endpoint.path}`
              const result = results[key]
              const isLoading = loadingStates[key]

              return (
                <div key={key} className="route-card p-4 space-y-3">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div className="space-y-1">
                      <div className="flex items-center gap-2">
                        <span className={`method-badge ${endpoint.method === "POST" ? "method-post" : "method-get"}`}>
                          {endpoint.method}
                        </span>
                        <span className="font-mono text-sm text-gray-200">{endpoint.path}</span>
                      </div>
                      <p className="text-xs text-gray-500">{endpoint.description}</p>
                    </div>
                    <Button
                      size="sm"
                      onClick={() => handleApiCall(endpoint)}
                      disabled={isLoading}
                      className="btn-primary rounded cursor-pointer"
                    >
                      {isLoading ? (
                        <div className="w-3 h-3 border-2 border-white border-t-transparent rounded-full animate-spin mr-1" />
                      ) : (
                        <Play className="w-3 h-3 mr-1" />
                      )}
                      Call
                    </Button>
                  </div>

                  {endpoint.body && (
                    <div className="request-body px-3 py-2 text-left">
                      <p className="text-xs text-yellow-500/70 mb-1 font-medium">Request Body:</p>
                      <pre className="text-xs text-yellow-300 font-mono whitespace-pre">
{JSON.stringify(endpoint.body, null, 2)}
                      </pre>
                    </div>
                  )}

                  {result && (
                    <div className="api-response text-left">
                      <div className="px-3 py-2 border-b border-green-500/20">
                        <p className="text-xs text-gray-500 font-mono">
                          Response {result.status > 0 ? `(${result.status})` : ""}
                        </p>
                      </div>
                      <pre className="p-3 text-xs overflow-x-auto whitespace-pre">
{result.data}
                      </pre>
                    </div>
                  )}
                </div>
              )
            })}
          </div>

          {/* Features Grid */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-16">
            <div className="feature-card p-6 text-center animate-fade-in-up animation-delay-100">
              <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-br from-[#009688]/30 to-[#00BFA5]/20 flex items-center justify-center">
                <Gauge className="w-6 h-6 text-[#00BFA5]" />
              </div>
              <h3 className="font-semibold text-lg mb-2">High Performance</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                One of the fastest Python frameworks available, on par with NodeJS and Go
              </p>
            </div>

            <div className="feature-card p-6 text-center animate-fade-in-up animation-delay-200">
              <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-br from-[#009688]/30 to-[#00BFA5]/20 flex items-center justify-center">
                <FileJson className="w-6 h-6 text-[#00BFA5]" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Auto Documentation</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Interactive API documentation with Swagger UI and ReDoc built-in
              </p>
            </div>

            <div className="feature-card p-6 text-center animate-fade-in-up animation-delay-300">
              <div className="w-12 h-12 mx-auto mb-4 rounded-xl bg-gradient-to-br from-[#009688]/30 to-[#00BFA5]/20 flex items-center justify-center">
                <RefreshCw className="w-6 h-6 text-[#00BFA5]" />
              </div>
              <h3 className="font-semibold text-lg mb-2">Async Support</h3>
              <p className="text-gray-400 text-sm leading-relaxed">
                Native async/await support for high-concurrency applications
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="footer-border relative z-10 mt-16">
        <div className="container mx-auto px-6 py-8">
          <div className="flex items-center justify-center gap-2 text-gray-500">
            <span>Powered by</span>
            <a 
              href="https://pages.edgeone.ai" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-gray-400 hover:text-[#00BFA5] transition-colors flex items-center gap-1"
            >
              <img src="/eo-logo-blue.svg" alt="EdgeOne" width={16} height={16} />
              EdgeOne Pages
            </a>
          </div>
        </div>
      </footer>
    </div>
  )
}
