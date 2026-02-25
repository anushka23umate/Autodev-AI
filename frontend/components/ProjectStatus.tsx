'use client'

import { useEffect, useState } from 'react'
import { api } from '@/services/api'

interface ProjectStatusProps {
  project: {
    id: string
    name: string
    status: string
    output_path?: string
    error_message?: string
  }
}

const statusSteps = [
  { key: 'queued', label: 'Queued' },
  { key: 'analyzing', label: 'Analyzing' },
  { key: 'generating_backend', label: 'Backend' },
  { key: 'generating_frontend', label: 'Frontend' },
  { key: 'dockerizing', label: 'Docker' },
  { key: 'completed', label: 'Completed' },
]

export default function ProjectStatus({ project: initialProject }: ProjectStatusProps) {
  const [project, setProject] = useState(initialProject)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (project.status !== 'completed' && project.status !== 'failed') {
      setLoading(true)
      const interval = setInterval(async () => {
        try {
          const response = await api.get(`/projects/${project.id}`)
          setProject(response.data)
          if (response.data.status === 'completed' || response.data.status === 'failed') {
            setLoading(false)
          }
        } catch (error) {
          console.error('Failed to fetch project status:', error)
        }
      }, 2000)
      return () => clearInterval(interval)
    }
  }, [project.id, project.status])

  const currentStepIndex = statusSteps.findIndex((s) => s.key === project.status)

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">Project Status</h3>

      <div className="space-y-6">
        <div>
          <p className="text-sm text-gray-600 mb-2">Project ID</p>
          <p className="font-mono text-sm text-gray-900">{project.id}</p>
        </div>

        <div>
          <p className="text-sm text-gray-600 mb-3">Generation Progress</p>
          <div className="space-y-3">
            {statusSteps.map((step, idx) => (
              <div key={step.key} className="flex items-center">
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-medium ${
                    idx < currentStepIndex
                      ? 'bg-green-500 text-white'
                      : idx === currentStepIndex
                      ? 'bg-blue-500 text-white'
                      : 'bg-gray-200 text-gray-600'
                  }`}
                >
                  {idx < currentStepIndex ? '✓' : idx + 1}
                </div>
                <div className="ml-3">
                  <p className={`text-sm font-medium ${
                    idx <= currentStepIndex ? 'text-gray-900' : 'text-gray-500'
                  }`}>
                    {step.label}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {project.status === 'completed' && (
          <div className="bg-green-50 border border-green-200 rounded-lg p-4">
            <p className="text-sm font-medium text-green-900 mb-2">✓ Project Generated Successfully!</p>
            {project.output_path && (
              <p className="text-xs text-green-700 font-mono">{project.output_path}</p>
            )}
          </div>
        )}

        {project.status === 'failed' && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4">
            <p className="text-sm font-medium text-red-900 mb-2">✗ Generation Failed</p>
            {project.error_message && (
              <p className="text-xs text-red-700">{project.error_message}</p>
            )}
          </div>
        )}

        {(project.status === 'analyzing' ||
          project.status === 'generating_backend' ||
          project.status === 'generating_frontend' ||
          project.status === 'dockerizing') && (
          <div className="flex items-center justify-center py-4">
            <div className="animate-spin h-6 w-6 text-indigo-600">
              <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24">
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                />
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                />
              </svg>
            </div>
            <p className="ml-3 text-sm text-gray-600">Generating...</p>
          </div>
        )}
      </div>
    </div>
  )
}
