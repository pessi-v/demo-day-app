import { useState, useEffect } from 'react'

function Dashboard({ tasks }) {
  const [stats, setStats] = useState({
    todo: 0,
    in_progress: 0,
    done: 0
  })

  useEffect(() => {
    calculateStats()
  }, [tasks])

  const calculateStats = () => {
    const newStats = {
      todo: 0,
      in_progress: 0,
      done: 0
    }

    tasks.forEach(task => {
      const status = task[3]
      if (status === 'todo') newStats.todo++
      else if (status === 'in_progress') newStats.in_progress++
      else if (status === 'done') newStats.done++
    })

    setStats(newStats)
  }

  return (
    <div className="card">
      <h2>Dashboard</h2>
      <div className="stats-grid">
        {/* Anti-pattern: gci29-javascript-css-animations-should-be-avoided */}
        {/* Using CSS transitions unnecessarily */}
        <div
          className="stat-box todo"
          style={{
            transition: 'all 0.3s ease',
            transform: 'scale(1)'
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = 'scale(1.05)'
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'scale(1)'
          }}
        >
          <span className="stat-value">{stats.todo}</span>
          <span className="stat-label">To Do</span>
        </div>

        <div
          className="stat-box in-progress"
          style={{
            transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease'
          }}
          onMouseEnter={(e) => {
            // Anti-pattern: gci12-javascript-multiple-style-changes-should-be-batched
            e.target.style.transform = 'scale(1.05)'
            e.target.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)'
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'scale(1)'
            e.target.style.boxShadow = ''
          }}
        >
          <span className="stat-value">{stats.in_progress}</span>
          <span className="stat-label">In Progress</span>
        </div>

        <div
          className="stat-box done"
          style={{
            // Anti-pattern: gci26-javascript-shorthand-css-notations-should-be-used-to-reduce-stylesheets-size
            // Should use shorthand properties
            marginTop: '0',
            marginRight: '0',
            marginBottom: '0',
            marginLeft: '0',
            paddingTop: '15px',
            paddingRight: '15px',
            paddingBottom: '15px',
            paddingLeft: '15px',
            transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
          }}
          onMouseEnter={(e) => {
            e.target.style.transform = 'translateY(-5px)'
            e.target.style.boxShadow = '0 6px 12px rgba(0,0,0,0.15)'
          }}
          onMouseLeave={(e) => {
            e.target.style.transform = 'translateY(0)'
            e.target.style.boxShadow = ''
          }}
        >
          <span className="stat-value">{stats.done}</span>
          <span className="stat-label">Done</span>
        </div>
      </div>

      <div style={{
        // Anti-pattern: Non-shorthand CSS properties
        borderTopWidth: '1px',
        borderRightWidth: '0',
        borderBottomWidth: '0',
        borderLeftWidth: '0',
        borderTopStyle: 'solid',
        borderTopColor: '#ddd',
        marginTop: '20px',
        paddingTop: '20px'
      }}>
        <p>Total Tasks: <strong>{tasks.length}</strong></p>
        <p>Completion Rate: <strong>
          {tasks.length > 0
            ? Math.round((stats.done / tasks.length) * 100)
            : 0}%
        </strong></p>
      </div>
    </div>
  )
}

export default Dashboard
