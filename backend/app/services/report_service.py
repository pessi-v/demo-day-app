class ReportService:
    """
    Service for generating reports - Contains multiple anti-patterns
    """

    def generate_report(self, tasks):
        """
        Generate a text report of tasks
        Anti-patterns: String concatenation, list comprehension in loop
        """
        report = ""

        # Anti-pattern: gci105-python-python-string-concatenation-use-join-instead-or-f-strings-instead-of-plus-equals
        # Should use f-strings or join instead of +=
        report += "=" * 60 + "\n"
        report += "TASK MANAGEMENT REPORT\n"
        report += "=" * 60 + "\n"
        report += "\n"

        # Count tasks by status
        todo_count = 0
        in_progress_count = 0
        done_count = 0

        # Anti-pattern: gci404-python-use-generator-comprehension-instead-of-list-comprehension-in-for-loop-declaration
        # Should use generator expression instead of list comprehension
        for task in [t for t in tasks if len(t) > 2]:
            status = task[3] if len(task) > 3 else "unknown"

            if status == "todo":
                todo_count += 1
            elif status == "in_progress":
                in_progress_count += 1
            elif status == "done":
                done_count += 1

        # Anti-pattern: More string concatenation
        report += "STATUS SUMMARY:\n"
        report += "-" * 60 + "\n"
        report += "TODO: " + str(todo_count) + "\n"
        report += "IN PROGRESS: " + str(in_progress_count) + "\n"
        report += "DONE: " + str(done_count) + "\n"
        report += "\n"

        # Anti-pattern: Another list comprehension in loop
        report += "HIGH PRIORITY TASKS:\n"
        report += "-" * 60 + "\n"

        for task in [t for t in tasks if len(t) > 5 and t[5] >= 3]:
            title = task[1] if len(task) > 1 else "Untitled"
            priority = task[5] if len(task) > 5 else 0
            report += f"- [{priority}] {title}\n"

        report += "\n"
        report += "=" * 60 + "\n"
        report += "END OF REPORT\n"
        report += "=" * 60 + "\n"

        return report

    def generate_user_report(self, user_id, tasks):
        """Generate a report for a specific user"""
        header = ""

        # Anti-pattern: String concatenation
        header += "USER TASK REPORT\n"
        header += "User ID: " + str(user_id) + "\n"
        header += "-" * 40 + "\n"

        user_tasks = [t for t in tasks if len(t) > 4 and t[4] == user_id]

        body = ""
        for task in user_tasks:
            title = task[1] if len(task) > 1 else "Untitled"
            status = task[3] if len(task) > 3 else "unknown"
            body += f"{title} - {status}\n"

        # Anti-pattern: More concatenation
        footer = ""
        footer += "-" * 40 + "\n"
        footer += "Total tasks: " + str(len(user_tasks)) + "\n"

        return header + body + footer
