import { useEffect } from 'react'

function TaskList({ tasks, onTaskUpdate }) {

  useEffect(() => {
    // Anti-pattern: gci11-javascript-multiple-access-of-same-dom-element-should-be-limited
    // Accessing the same DOM element multiple times
    const container = document.getElementById('task-container')
    if (container) {
      const width = document.getElementById('task-container').clientWidth
      const height = document.getElementById('task-container').clientHeight
      const offsetTop = document.getElementById('task-container').offsetTop

      console.log('Container dimensions:', width, height, offsetTop)
    }
  }, [tasks])

  const handleTaskClick = (taskId) => {
    const taskElement = document.getElementById(`task-${taskId}`)

    if (taskElement) {
      // Anti-pattern: gci12-javascript-multiple-style-changes-should-be-batched
      // Multiple individual style changes instead of batching
      taskElement.style.backgroundColor = '#e3f2fd'
      taskElement.style.borderColor = '#2196f3'
      taskElement.style.borderWidth = '2px'
      taskElement.style.paddingLeft = '15px'

      // Reset after a delay
      setTimeout(() => {
        taskElement.style.backgroundColor = ''
        taskElement.style.borderColor = ''
        taskElement.style.borderWidth = ''
        taskElement.style.paddingLeft = ''
      }, 2000)
    }
  }

  const getStatusColor = (status) => {
    if (status === 'todo') return '#3498db'
    if (status === 'in_progress') return '#f39c12'
    if (status === 'done') return '#2ecc71'
    return '#95a5a6'
  }

  const getPriorityLabel = (priority) => {
    if (priority === 1) return 'Low'
    if (priority === 2) return 'Medium'
    if (priority === 3) return 'High'
    return 'Unknown'
  }

  return (
    <div className="card" id="task-container">
      <h2>All Tasks</h2>
      <ul className="task-list">
        {tasks.map((task, index) => (
          <li
            key={index}
            id={`task-${task[0]}`}
            className="task-item"
            onClick={() => handleTaskClick(task[0])}
          >
            <div className="task-title">{task[1]}</div>
            <div className="task-meta">
              <span style={{
                color: getStatusColor(task[3]),
                fontWeight: 'bold'
              }}>
                {task[3] || 'unknown'}
              </span>
              {' '} | Priority: {getPriorityLabel(task[5])}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default TaskList
