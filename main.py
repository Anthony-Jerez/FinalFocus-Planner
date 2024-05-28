from openai import OpenAI
import matplotlib.pyplot as plt
import json

# Retrieve API key
with open('config.json') as config_file:
    config = json.load(config_file)
client = OpenAI(api_key=config['OPENAI_API_KEY'])

# Specify days and colors to be associated with each day
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
colors = ['pink', 'lightgreen', 'lightblue', 'wheat', 'salmon']


example = '''
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


def get_completion(prompt, model="gpt-4o"):
    messages = [{"role": "user", "content": prompt}]
    print("Please wait for your study planner to be generated.")
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=4000,
    )
    return response.choices[0].message.content


def create_schedule(schedule_dict, start_hr, start_min, end_hr, end_min, name, title):
    week_schedule = []
    # Format schedule to be as list of lists
    for day in range(1, 6):  # 1 to 5 for Monday to Friday
        day_activities = schedule_dict.get(str(day), [])
        week_schedule.append(day_activities)
    # Plot schedule
    fig, ax = plt.subplots(figsize=(10, 5.89))
    # For each day's activities
    for day_index, day_activities in enumerate(week_schedule, start=1):
        # For each activity in the current day being examined
        for activity in day_activities:
            day_i = float(day_index)
            start_hour = float(activity["start_hour"])
            start_minute = float(activity["start_minute"])
            duration = float(activity["duration"])
            event = activity["subject"]
            day = day_i - 0.48
            start = start_hour + start_minute / 60
            end = start + duration / 60
            # Plot the subject
            ax.fill_between([day, day + 0.96], [start, start], [end, end], color=colors[int(day_i) - 1], edgecolor='k',
                            linewidth=0.5)
            # Plot the beginning time
            ax.text(day + 0.02, start + 0.05, '{0}:{1:0>2}'.format(int(start_hour), int(start_minute)), va='bottom', fontsize=6)
            # Plot the subject name
            ax.text(day + 0.48, (start + end) * 0.5, event, ha='center', va='center', fontsize=7)
    # Set axis
    start_hr = int(start_hr)
    start_min = int(start_min)
    end_hr = int(end_hr)
    end_min = int(end_min)
    # Calculate decimal representation of start and end times
    end_time_decimal = end_hr + end_min / 60
    start_time_decimal = start_hr + start_min / 60
    ax.yaxis.grid()
    ax.set_xlim(0.5, len(days) + 0.5)
    # Structure axis according to the student's start and end times
    ax.set_ylim(start_time_decimal, end_time_decimal)
    ax.set_xticks(range(1, len(days) + 1))
    ax.set_xticklabels(days)
    ax.set_ylabel('Time')
    # Set second axis
    ax2 = ax.twiny().twinx()
    ax2.set_xlim(ax.get_xlim())
    ax2.set_ylim(ax.get_ylim())
    ax2.set_xticks(ax.get_xticks())
    ax2.set_xticklabels(days)
    ax2.set_ylabel('Time')
    plt.title(title, y=1.07)
    # Save and display study schedule in a generated png file
    plt.savefig(f'{name}-Study-Plan.png'.format(title), dpi=200)
    plt.close(fig)
    print("Study planner was successfully created.")


def main():
    # Prompt for student's name
    name = input("What is your name?")
    # Prompt for student's topics of interest for studying
    topics = input("Enter topics of studying interest separated by comma: ").split(", ")
    topics_str = ", ".join(topics)
    # Prompt student for their preferences
    preferences = ""
    for topic in topics:
        preferences += f'{name} would like to prepare for {topic} on the following day(s): '
        preferences += input(
            f'On which day(s) would you like to prepare for {topic}. Separate each day by comma:') + '. '
    # Prompt for student's availability for studying
    hours, minutes = input('How much time (in hours and minutes) can you dedicate to studying each day. Enter hours '
                           'followed by minutes seperated by comma: ').split(", ")
    # Prompt student for their subjects of main priority
    priority_subjects = input(
        'Specify the topics that are the most important for you to focus on right now seperated by '
        'comma: ')
    # Prompt student for their main goals
    goals = input("List your main goals. Separate each goal by comma: ")
    # Prompt student for start and end times for each day
    start_hr, start_min = input(
        "Enter the time that you start your day based on the 24-hour clock. Specify hour followed "
        "by minutes separated by comma: ").split(", ")
    end_hr, end_min = input("Enter the time that you end your day based on the 24-hour clock. Specify hour followed by "
                            "minutes separated by comma: ").split(", ")
    # Prompt student for start times and duration for each meal
    breakfast_hr, breakfast_min = input(
        "Enter the time that you have breakfast based on the 24-hour clock. Specify hour "
        "followed by minutes separated by comma: ").split(", ")
    lunch_hr, lunch_min = input(
        "Enter the time that you have lunch based on the 24-hour clock. Specify hour followed by "
        "minutes separated by comma: ").split(", ")
    dinner_hr, dinner_min = input(
        "Enter the time that you have dinner based on the 24-hour clock. Specify hour followed "
        "by minutes separated by comma: ").split(", ")
    meal_duration = input("Enter in minutes how long each meal should last: ")
    # Prompt student for their preferred number of breaks and duration of each break for all days
    breaks_num = input("Enter the number of breaks you prefer to have on each day: ")
    break_duration = input("Enter in minutes how long each break should last: ")
    title = f"{name}'s Final Exam Week Five-Day Study Plan"
    # Construction of prompt
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
    - Ensure the schedule adheres to the provided information and return it in JSON format without any markdown notation. You must follow the EXACT format as shown in this example for a person's Monday schedule delimited by triple backticks```{example}```. Once again this is only an example and you must make sure to construct {name}'s schedule based on the daily schedule requirements, instructions, and the rest of the information provided before.'''
    # Retrieve generated schedule in JSON format
    print(prompt)
    response = get_completion(prompt)
    try:
        schedule_dict = json.loads(response)
        print(schedule_dict)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    # Plot study schedule
    create_schedule(schedule_dict, start_hr, start_min, end_hr, end_min, name, title)


if __name__ == "__main__":
    main()















