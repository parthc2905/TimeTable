import datetime
from typing import List, Dict, Optional

class Task:
    def __init__(self, name: str, duration: int, priority: int = 1, deadline: Optional[datetime.datetime] = None):
        self.name = name
        self.duration = duration  # in minutes
        self.priority = priority  # 1-5, where 5 is highest priority
        self.deadline = deadline
        self.completed = False

class TaskScheduler:
    def __init__(self):
        self.tasks: List[Task] = []
        self.schedule: Dict[datetime.date, List[Task]] = {}

    def add_task(self, task: Task):
        """Add a new task to the scheduler"""
        self.tasks.append(task)
        self._sort_tasks()

    def _sort_tasks(self):
        """Sort tasks by priority and deadline"""
        self.tasks.sort(key=lambda x: (x.priority, x.deadline if x.deadline else datetime.datetime.max), reverse=True)

    def generate_schedule(self, start_date: datetime.date, end_date: datetime.date):
        """Generate a schedule for the given date range"""
        current_date = start_date
        self.schedule = {}
        
        while current_date <= end_date:
            self.schedule[current_date] = []
            current_date += datetime.timedelta(days=1)

        # Distribute tasks across available days
        for task in self.tasks:
            if not task.completed:
                # Find the earliest available day
                for date in self.schedule:
                    if len(self.schedule[date]) < 8:  # Assuming max 8 tasks per day
                        self.schedule[date].append(task)
                        break

    def view_schedule(self, date: Optional[datetime.date] = None):
        """View the schedule for a specific date or all dates"""
        if date:
            if date in self.schedule:
                print(f"\nSchedule for {date}:")
                for i, task in enumerate(self.schedule[date], 1):
                    print(f"{i}. {task.name} ({task.duration} minutes) - Priority: {task.priority}")
            else:
                print(f"No schedule found for {date}")
        else:
            for date, tasks in self.schedule.items():
                print(f"\nSchedule for {date}:")
                for i, task in enumerate(tasks, 1):
                    print(f"{i}. {task.name} ({task.duration} minutes) - Priority: {task.priority}")

    def mark_task_completed(self, task_name: str):
        """Mark a task as completed"""
        for task in self.tasks:
            if task.name == task_name:
                task.completed = True
                break

def main():
    scheduler = TaskScheduler()
    
    while True:
        print("\nTask Scheduler Menu:")
        print("1. Add Task")
        print("2. Generate Schedule")
        print("3. View Schedule")
        print("4. Mark Task as Completed")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == "1":
            name = input("Enter task name: ")
            duration = int(input("Enter task duration (in minutes): "))
            priority = int(input("Enter priority (1-5): "))
            deadline_str = input("Enter deadline (YYYY-MM-DD) or press Enter for no deadline: ")
            
            deadline = None
            if deadline_str:
                deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d")
            
            task = Task(name, duration, priority, deadline)
            scheduler.add_task(task)
            print("Task added successfully!")
            
        elif choice == "2":
            start_date_str = input("Enter start date (YYYY-MM-DD): ")
            end_date_str = input("Enter end date (YYYY-MM-DD): ")
            
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            
            scheduler.generate_schedule(start_date, end_date)
            print("Schedule generated successfully!")
            
        elif choice == "3":
            date_str = input("Enter date to view (YYYY-MM-DD) or press Enter for all dates: ")
            if date_str:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                scheduler.view_schedule(date)
            else:
                scheduler.view_schedule()
                
        elif choice == "4":
            task_name = input("Enter task name to mark as completed: ")
            scheduler.mark_task_completed(task_name)
            print("Task marked as completed!")
            
        elif choice == "5":
            print("Exiting Task Scheduler. Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main() 