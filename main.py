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
        temperature=0.3,
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
    plt.savefig(f'{name}-Study-Plan-.png'.format(title), dpi=200)
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
    time = f"{name} can allocate {hours} hours and {minutes} minutes to studying each day. When making the schedule also " \
           f"consider {name}'s meal and break time durations which will be specified later on. Also, ensure that all the " \
           f"{hours} hours and {minutes} minutes that {name} requested to be allocated for studying are allocated for " \
           f"studying in his schedule creation. This means that if {name} requested {hours} hours and {minutes} minutes " \
           f"to be allocated for studying then you must ensure that ALL of that time is actually allocated for studying. " \
           f"Assign the meal and break times EXACTLY (meaning not adding or removing time) as how {name} will specify " \
           f"later on."
    # Prompt student for their subjects of main priority
    priority_subjects = f"{name} needs to prioritize studying the following topics: "
    priority_subjects += input(
        'Specify the topics that are the most important for you to focus on right now seperated by '
        'comma: ')
    # Prompt student for their main goals
    goals = f"{name}'s main goals are to: "
    goals += input("List your main goals. Separate each goal by comma: ")
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
    prompt = f'''You are an assistant tasked with creating personalized study schedules for students. Generate a 5-Day 
    personalized study schedule in JSON format for a student named {name} who is preparing for their final exams. {name} 
    needs to study the following subjects: {topics_str}. {time}. {preferences}. {priority_subjects}. {goals}. {name} 
    always starts his day at {start_hr}:{start_min} and ends at {end_hr}:{end_min} for all of the five days. Alex MUST 
    have breakfast everyday at {breakfast_hr}:{breakfast_min}, MUST have lunch everyday at {lunch_hr}:{lunch_min}, 
    MUST have dinner everyday at {dinner_hr}:{dinner_min}. Each meal MUST last {meal_duration} minutes. {name} also MUST 
    have EXACTLY {breaks_num} breaks during each day. Each break MUST last {break_duration} minutes. Each day should be 
    associated with an integer where 1 is Monday, 2 is Tuesday, 3 is Wednesday, 4 is Thursday, and 5 is Friday. Each day 
    should have a list of activities with start_hour (as an integer), start_minute (as an integer), duration in minutes (
    as an integer), and subject. All days follow the 24-hour clock. You MUST ensure there are NO time conflicts. Also, 
    ensure that each day starts and ends at the same specific time. For example, if the initial activity assigned for 
    Monday has a start hour of 9 and start minute of 0, then the rest of the days must have their initial activities 
    start from the same time. Additionally, if the student's day is set to end at {end_hr}:{end_min}, then it MUST end at 
    that time of day for ALL of the days. Also, if the student's breakfast start time is set to start at {breakfast_hr}:
    {breakfast_min}, if student's lunch time is set to start at {lunch_hr}:{lunch_min}, and if student's dinner time is 
    set to start at {dinner_hr}:{dinner_min}, then these subjects MUST be included and these start times specified before 
    in this same sentence MUST happen for ALL of the days. Along with meal start times, each meal (referring to 
    breakfast, lunch, and dinner) MUST last for ONLY a total of {meal_duration} minutes as specified before. This means 
    don't allocate more time or less time for meals and break times than what is required and specified. Ensure that 
    there are breakfast, lunch, dinner, and break activities assigned for each day where each of breakfast, lunch, 
    and dinner can only occur once for each day. Remember that each day must have exactly {breaks_num} breaks and each 
    break is ONLY {break_duration} minutes long. DO NOT create a 'End of Day' subject or any other subjects of your own 
    aside from those specified before. You must generate schedules for Monday(1) to Friday(5) by allocating hours based 
    on {name}'s time availability, priorities, main goals, and the rest of the provided information mentioned before in 
    the previous sentences. You MUST follow a similar format as shown in this example for a person's Monday schedule 
    delimited by triple backticks```{example}```. Remember this is just an example and you MUST make sure to create the 
    schedule based on {name}'s provided information. Once again it has to be returned in JSON format and do not include 
    any markdown notation like ```json so that I can parse the JSON string.'''
    # Retrieve generated schedule in JSON format
    response = get_completion(prompt)
    try:
        schedule_dict = json.loads(response)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    # Plot and display study schedule
    create_schedule(schedule_dict, start_hr, start_min, end_hr, end_min, name, title)


if __name__ == "__main__":
    main()















