// Anti-pattern: gci9-javascript-importing-everything-from-library-should-be-avoided
// Importing entire lodash library when only specific functions are needed
import * as _ from 'lodash'

export const formatTaskData = (tasks) => {
  // Using lodash for operations that could be done with native JS
  return _.map(tasks, (task) => ({
    id: task[0],
    title: task[1],
    description: task[2],
    status: task[3],
    userId: task[4],
    priority: task[5]
  }))
}

export const filterTasksByStatus = (tasks, status) => {
  // Could use native filter instead
  return _.filter(tasks, (task) => task[3] === status)
}

export const groupTasksByUser = (tasks) => {
  // Could use reduce instead
  return _.groupBy(tasks, (task) => task[4])
}

export const getHighPriorityTasks = (tasks) => {
  // Chaining lodash methods unnecessarily
  return _.chain(tasks)
    .filter((task) => task[5] >= 3)
    .sortBy((task) => task[5])
    .reverse()
    .value()
}

export const calculateCompletionRate = (tasks) => {
  const total = _.size(tasks)
  if (total === 0) return 0

  const completed = _.filter(tasks, (task) => task[3] === 'done').length
  return _.round((completed / total) * 100, 2)
}

export const getUniqueStatuses = (tasks) => {
  // Could use Set instead
  return _.uniq(_.map(tasks, (task) => task[3]))
}

export const findTaskById = (tasks, id) => {
  // Simple find operation using lodash
  return _.find(tasks, (task) => task[0] === id)
}

export const sortTasksByPriority = (tasks) => {
  // Could use native sort
  return _.orderBy(tasks, [(task) => task[5]], ['desc'])
}
