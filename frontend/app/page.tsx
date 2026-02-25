'use client'

import { useState, useEffect } from 'react'
import PromptInput from '@/components/PromptInput'
import ProjectStatus from '@/components/ProjectStatus'
import { api } from '@/services/api'

interface Project {
  id: string
  name: string
  prompt: string
  status: string
  output_path?: string
  error_message?: string
  created_at: string
  updated_at: string
}

export default function Home() {
  const [projects, setProjects] = useState<Project[]>([])
  const [loading, setLoading] = useState(false)
  const [selectedProject, setSelectedProject] = useState<Project | null>(null)

  const fetchProjects = async () => {
    try {
      const response = await api.get('/projects')
      setProjects(response.data.projects)
    } catch (error) {
      console.error('Failed to fetch projects:', error)
    }
  }

  useEffect(() => {
    fetchProjects()
    const interval = setInterval(fetchProjects, 5000)
    return () => clearInterval(interval)
  }, [])

  const handleGenerateProject = async (prompt: string) => {
    setLoading(true)
    try {
      const response = await api.post('/generate', { prompt })
      setSelectedProject(response.data)
      setProjects([response.data, ...projects])
    } catch (error) {
      console.error('Failed to generate project:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-8">
      <section className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-lg shadow-lg p-8 text-white">
        <h2 className="text-3xl font-bold mb-4">Generate Your Project</h2>
        <p className="text-lg mb-6">
          Describe what you want to build, and AutoDev-AI will generate a complete full-stack application.
        </p>
        <PromptInput onSubmit={handleGenerateProject} isLoading={loading} />
      </section>

      <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2">
          <div className="bg-white rounded-lg shadow">
            <div className="px-6 py-4 border-b">
              <h3 className="text-xl font-semibold text-gray-900">Recent Projects</h3>
            </div>
            <div className="divide-y">
              {projects.length === 0 ? (
                <div className="px-6 py-8 text-center text-gray-500">
                  <p>No projects yet. Create one to get started!</p>
                </div>
              ) : (
                projects.map((project) => (
                  <div
                    key={project.id}
                    onClick={() => setSelectedProject(project)}
                    className="px-6 py-4 hover:bg-gray-50 cursor-pointer transition"
                  >
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium text-gray-900">{project.name}</h4>
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                        project.status === 'completed'
                          ? 'bg-green-100 text-green-800'
                          : project.status === 'failed'
                          ? 'bg-red-100 text-red-800'
                          : 'bg-blue-100 text-blue-800'
                      }`}>
                        {project.status}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600 line-clamp-2">{project.prompt}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        <div>
          {selectedProject && (
            <ProjectStatus project={selectedProject} />
          )}
        </div>
      </section>
    </div>
  )
}
