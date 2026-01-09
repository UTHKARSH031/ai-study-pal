"""
Study Plan Generation Module
Creates study schedules based on user inputs
"""

import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List
import csv


class StudyPlanner:
    """Generates study plans and schedules"""
    
    def __init__(self):
        self.scenarios = {
            "exam_prep": {
                "focus": "intensive review",
                "daily_hours": 3,
                "structure": "review -> practice -> test"
            },
            "homework": {
                "focus": "completion",
                "daily_hours": 2,
                "structure": "understand -> solve -> verify"
            },
            "general": {
                "focus": "learning",
                "daily_hours": 1.5,
                "structure": "read -> practice -> review"
            }
        }
    
    def generate_study_plan(self, subject: str, study_hours: float, scenario: str = "exam_prep") -> Dict:
        """
        Generate a study plan based on inputs
        
        Args:
            subject: Subject name
            study_hours: Total study hours
            scenario: Study scenario (exam_prep, homework, general)
            
        Returns:
            Dictionary with study plan details
        """
        scenario_config = self.scenarios.get(scenario, self.scenarios["general"])
        
        # Calculate study days
        daily_hours = scenario_config["daily_hours"]
        num_days = max(1, int(study_hours / daily_hours))
        
        # Generate plan structure
        plan = {
            "subject": subject,
            "total_hours": study_hours,
            "scenario": scenario,
            "num_days": num_days,
            "daily_hours": daily_hours,
            "focus": scenario_config["focus"],
            "structure": scenario_config["structure"],
            "schedule": self._create_daily_schedule(num_days, daily_hours, subject)
        }
        
        return plan
    
    def _create_daily_schedule(self, num_days: int, daily_hours: float, subject: str) -> List[Dict]:
        """
        Create daily schedule breakdown
        
        Args:
            num_days: Number of study days
            daily_hours: Hours per day
            subject: Subject name
            
        Returns:
            List of daily schedule dicts
        """
        schedule = []
        start_date = datetime.now()
        
        activities = [
            "Review key concepts",
            "Practice problems",
            "Read new material",
            "Take practice quiz",
            "Review notes"
        ]
        
        for day in range(num_days):
            date = start_date + timedelta(days=day)
            day_schedule = {
                "day": day + 1,
                "date": date.strftime("%Y-%m-%d"),
                "hours": daily_hours,
                "activities": activities[day % len(activities)],
                "focus": f"{subject} - Day {day + 1}"
            }
            schedule.append(day_schedule)
        
        return schedule
    
    def create_csv_schedule(self, plan: Dict, filename: str = "study_schedule.csv") -> str:
        """
        Create downloadable CSV schedule
        
        Args:
            plan: Study plan dictionary
            filename: Output filename
            
        Returns:
            Path to created CSV file
        """
        schedule = plan.get("schedule", [])
        
        rows = []
        rows.append(["Day", "Date", "Hours", "Activities", "Focus"])
        
        for day_plan in schedule:
            rows.append([
                day_plan["day"],
                day_plan["date"],
                day_plan["hours"],
                day_plan["activities"],
                day_plan["focus"]
            ])
        
        # Write CSV
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(rows)
        
        return filename
    
    def get_plan_summary(self, plan: Dict) -> str:
        """
        Get text summary of study plan
        
        Args:
            plan: Study plan dictionary
            
        Returns:
            Text summary
        """
        summary = f"""
Study Plan for {plan['subject']}
Total Hours: {plan['total_hours']}
Study Days: {plan['num_days']}
Daily Hours: {plan['daily_hours']}
Focus: {plan['focus']}
Structure: {plan['structure']}

Schedule:
"""
        for day in plan['schedule']:
            summary += f"Day {day['day']} ({day['date']}): {day['hours']} hours - {day['activities']}\n"
        
        return summary

