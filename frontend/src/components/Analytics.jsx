import { useState, useEffect } from 'react'
// Anti-pattern: gci9-javascript-importing-everything-from-library-should-be-avoided
// Should import specific functions instead of entire library
import _ from 'lodash'

function Analytics() {
  const [stats, setStats] = useState(null)
  const [userSummary, setUserSummary] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const [statsRes, summaryRes] = await Promise.all([
        fetch('/api/analytics/stats'),
        fetch('/api/analytics/user-summary')
      ])

      const statsData = await statsRes.json()
      const summaryData = await summaryRes.json()

      setStats(statsData)
      setUserSummary(summaryData.summaries || [])
      setLoading(false)
    } catch (err) {
      console.error('Failed to fetch analytics:', err)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="card">
        <h2>Analytics</h2>
        <p>Loading analytics...</p>
      </div>
    )
  }

  // Anti-pattern: Using lodash for simple operations
  const totalTasks = stats ? _.sum(_.values(stats.stats)) : 0
  const hasData = !_.isEmpty(userSummary)

  // More unnecessary lodash usage
  const sortedUsers = _.orderBy(userSummary, ['total_tasks'], ['desc'])
  const topUser = _.first(sortedUsers)

  return (
    <div className="card">
      <h2>Analytics</h2>

      {stats && (
        <div style={{
          // Anti-pattern: gci26 - Non-shorthand CSS
          marginTop: '0',
          marginBottom: '15px',
          paddingTop: '10px',
          paddingBottom: '10px',
          paddingLeft: '15px',
          paddingRight: '15px',
          backgroundColor: '#f8f9fa',
          borderRadius: '6px'
        }}>
          <h3 style={{ marginTop: '0', marginBottom: '10px', fontSize: '16px' }}>
            Status Overview
          </h3>
          <div>
            {/* Using lodash map instead of native */}
            {_.map(stats.stats, (count, status) => (
              <div key={status} style={{
                display: 'flex',
                justifyContent: 'space-between',
                marginBottom: '5px'
              }}>
                <span>{_.capitalize(status.replace('_', ' '))}:</span>
                <strong>{count}</strong>
              </div>
            ))}
          </div>
          <div style={{
            borderTop: '1px solid #ddd',
            marginTop: '10px',
            paddingTop: '10px'
          }}>
            <strong>Total: {totalTasks}</strong>
          </div>
        </div>
      )}

      {hasData && (
        <div>
          <h3 style={{ fontSize: '16px', marginBottom: '10px' }}>
            Top Contributor
          </h3>
          {topUser && (
            <div style={{
              padding: '10px',
              backgroundColor: '#e3f2fd',
              borderRadius: '6px',
              // Anti-pattern: gci29 - CSS animations
              transition: 'background-color 0.3s ease'
            }}>
              <div><strong>{topUser.name}</strong></div>
              <div style={{ fontSize: '14px', color: '#666' }}>
                {topUser.total_tasks} tasks ({topUser.completed_tasks} completed)
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default Analytics
