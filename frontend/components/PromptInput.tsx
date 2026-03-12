'use client'

import { useState } from 'react'

interface PromptInputProps {
  onSubmit: (prompt: string) => void
  isLoading: boolean
}

export default function PromptInput({ onSubmit, isLoading }: PromptInputProps) {
  const [prompt, setPrompt] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (prompt.trim()) {
      onSubmit(prompt)
      setPrompt('')
    }
  }

  const examples = [
    'Build a task manager with authentication and real-time updates',
    'Create a blog platform with user profiles and comments',
    'Build a weather dashboard with 5-day forecast',
    'Create an e-commerce product catalog with search and filters',
  ]

  return (
    <div className="space-y-4">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="prompt" className="block text-sm font-medium mb-2">
            Describe Your Project
          </label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Example: Build a task manager with authentication, real-time updates, and a clean dashboard..."
            rows={4}
            className="w-full px-4 py-3 bg-white text-gray-900 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-white"
          />
        </div>
        <button
          type="submit"
          disabled={isLoading || !prompt.trim()}
          className={`w-full py-3 px-4 rounded-lg font-semibold transition ${
            isLoading || !prompt.trim()
              ? 'bg-gray-400 cursor-not-allowed'
              : 'bg-white text-indigo-600 hover:bg-gray-100'
          }`}
        >
          {isLoading ? 'Generating...' : 'Generate Project'}
        </button>
      </form>

      <div>
        <p className="text-sm font-medium mb-3">Try These Examples:</p>
        <div className="space-y-2">
          {examples.map((example, idx) => (
            <button
              key={idx}
              type="button"
              onClick={() => {
                setPrompt(example)
                onSubmit(example)
              }}
              disabled={isLoading}
              className="w-full text-left px-4 py-2 bg-white bg-opacity-20 hover:bg-opacity-30 rounded-lg text-sm transition disabled:opacity-50 disabled:cursor-not-allowed"
            >
              → {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}
