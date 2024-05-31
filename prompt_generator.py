# Example output for a student's Monday study schedule
example_result = '''
    {
      "1": [
        {
          "start_hour": 8,
          "start_minute": 0,
          "duration": 30,
          "subject": "Breakfast"
        },
        {
          "start_hour": 8,
          "start_minute": 30,
          "duration": 120,
          "subject": "Algorithms"
        },
        {
          "start_hour": 10,
          "start_minute": 30,
          "duration": 15,
          "subject": "Break"
        },
        {
          "start_hour": 10,
          "start_minute": 45,
          "duration": 105,
          "subject": "Databases"
        },
        {
          "start_hour": 12,
          "start_minute": 30,
          "duration": 45,
          "subject": "Lunch"
        },
        {
          "start_hour": 13,
          "start_minute": 15,
          "duration": 75,
          "subject": "Break"
        },
        {
          "start_hour": 14,
          "start_minute": 30,
          "duration": 90,
          "subject": "Operating Systems"
        },
        {
          "start_hour": 16,
          "start_minute": 0,
          "duration": 15,
          "subject": "Break"
        },
        {
          "start_hour": 16,
          "start_minute": 15,
          "duration": 105,
          "subject": "Cloud Computing"
        },
        {
          "start_hour": 18,
          "start_minute": 0,
          "duration": 60,
          "subject": "Dinner"
        }
      ]
    },'''


# Constructs and returns prompt
def generate_prompt(name, topics_str, start_hr, start_min, end_hr, end_min, breakfast_hr, breakfast_min, lunch_hr, lunch_min, dinner_hr, dinner_min, meal_duration, breaks_num, break_duration, hours, minutes, preferences, priority_subjects, goals):
    prompt = f'''
    You are an assistant tasked with creating personalized study schedules for students. Generate a 5-Day personalized study schedule in JSON format for a student named {name} who is preparing for final exam week. {name} needs to study the following subjects: {topics_str}.

    Daily Schedule Requirements:
    - All days follow the 24-hour clock 
    - Start day at {start_hr}:{start_min} and end at {end_hr}:{end_min} for all five days.
    - Meals: 
      - Breakfast MUST occur at {breakfast_hr}:{breakfast_min} and last a total of {meal_duration} minutes for all five days.
      - Lunch MUST occur at {lunch_hr}:{lunch_min} and last a total of {meal_duration} minutes for all five days.
      - Dinner MUST occur at {dinner_hr}:{dinner_min} and last a total of {meal_duration} minutes for all five days.
    - Breaks: 
      - There must be exactly {breaks_num} breaks each day, each lasting a total of {break_duration} minutes.
    - For the {topics_str} topics that {name} MUST study for:
      - {name} MUST dedicate a total of {hours} hours and {minutes} minutes to studying each day.
      - {preferences}
      - {name} needs to prioritize studying the following topics: {priority_subjects}.
      - {name}'s main goals are to: {goals}.
      - The studying subjects start times and durations are determined based on {name}'s specified time availability, preferences, priority subjects, and main goals. Ensure they don't conflict with the already established meal/break start times and durations.

    Instructions:
    - Each day is represented by an integer (1=Monday, 2=Tuesday, 3=Wednesday, 4=Thursday, 5=Friday).
    - List activities for each day with start_hour (integer), start_minute (integer), duration (minutes as an integer), and subject (either meals, breaks, or topics {name} must study for).
    - Ensure no time conflicts and consistent start and end times for each day.
    - Include meals at the specified times and durations. Also, include breaks at the specified durations. This means do not allocate more time or less time for meals and break times than what is specified.
    - ONLY create subjects for meals, breaks, and {topics_str} topics that {name} must study for.
    - Ensure the schedule adheres to the provided information and return it in JSON format without any markdown notation. You must follow the EXACT format as shown in this example for a person's Monday schedule delimited by triple backticks```{example_result}```. Once again this is only an example and you must make sure to construct {name}'s schedule based on the daily schedule requirements, instructions, and the rest of the information provided before.'''
    return prompt