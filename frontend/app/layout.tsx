import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'AutoDev-AI - Code Generation Platform',
  description: 'Generate full-stack applications with AI',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="bg-gray-50">
        <nav className="bg-white shadow">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16 items-center">
              <h1 className="text-2xl font-bold text-indigo-600">AutoDev-AI</h1>
              <p className="text-gray-600">Autonomous Code Generation Platform</p>
            </div>
          </div>
        </nav>
        <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
          {children}
        </main>
      </body>
    </html>
  )
}
