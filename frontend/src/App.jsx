import { useState, useEffect } from 'react'
import TaskList from './components/TaskList'
import Dashboard from './components/Dashboard'
import Analytics from './components/Analytics'

function App() {
  const [tasks, setTasks] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetchTasks()
  }, [])

  const fetchTasks = async () => {
    try {
      const response = await fetch('/api/tasks/')
      const data = await response.json()
      setTasks(data.tasks || [])
      setLoading(false)
    } catch (err) {
      setError('Failed to fetch tasks')
      setLoading(false)
    }
  }

  if (loading) {
    return <div className="loading">Loading tasks...</div>
  }

  if (error) {
    return (
      <div className="app">
        <div className="error">{error}</div>
      </div>
    )
  }

  return (
    <div className="app">
      <div className="header">
        <h1>Task Manager</h1>
        <p>Demo application for Carbonara - Sustainable Software Analysis Tool</p>
      </div>

      <div className="dashboard">
        <Dashboard tasks={tasks} />
        <Analytics />
      </div>

      <TaskList tasks={tasks} onTaskUpdate={fetchTasks} />
    </div>
  )
}

export default App
