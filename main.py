from openai import OpenAI
import json
from config import days, colors
from schedule_generator import create_schedule
from prompt_generator import generate_prompt

# Retrieve API key
with open('config.json') as config_file:
    config = json.load(config_file)
client = OpenAI(api_key=config['OPENAI_API_KEY'])


def get_completion(prompt, model="gpt-4o"):
    messages = [{"role": "user", "content": prompt}]
    print("Please wait for your study plan to be generated.")
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=4000,
    )
    return response.choices[0].message.content


def prompt_name():
    return input("What is your name?")


def prompt_topics():
    topics = input("Enter topics of studying interest separated by comma: ").split(", ")
    return ", ".join(topics)


def prompt_preferences(name, topics):
    preferences = ""
    for topic in topics:
        preferences += f'{name} would like to prepare for {topic} on the following day(s): '
        preferences += input(
            f'On which day(s) would you like to prepare for {topic}. Separate each day by comma:') + '. '
    return preferences


def prompt_availability():
    return input('How much time (in hours and minutes) can you dedicate to studying each day. Enter hours '
                 'followed by minutes separated by comma: ').split(", ")


def prompt_priority_subjects():
    return input(
        'Specify the topics that are the most important for you to focus on right now separated by '
        'comma: ')


def prompt_goals():
    return input("List your main goals. Separate each goal by comma: ")


def prompt_day_times(message):
    return input(message).split(", ")


def prompt_meal_times():
    breakfast_hr, breakfast_min = prompt_day_times(
        "Enter the time that you have breakfast based on the 24-hour clock. Specify hour "
        "followed by minutes separated by comma: ")
    lunch_hr, lunch_min = prompt_day_times(
        "Enter the time that you have lunch based on the 24-hour clock. Specify hour followed by "
        "minutes separated by comma: ")
    dinner_hr, dinner_min = prompt_day_times(
        "Enter the time that you have dinner based on the 24-hour clock. Specify hour followed "
        "by minutes separated by comma: ")
    return breakfast_hr, breakfast_min, lunch_hr, lunch_min, dinner_hr, dinner_min


def prompt_breaks():
    breaks_num = input("Enter the number of breaks you prefer to have on each day: ")
    break_duration = input("Enter in minutes how long each break should last: ")
    return breaks_num, break_duration


def main():
    # Prompt for student's name
    name = prompt_name()
    # Prompt for student's topics of interest for studying
    topics_str = prompt_topics()
    # Prompt student for their preferences
    preferences = prompt_preferences(name, topics_str.split(", "))
    # Prompt for student's availability for studying
    hours, minutes = prompt_availability()
    # Prompt student for their subjects of main priority
    priority_subjects = prompt_priority_subjects()
    # Prompt student for their main goals
    goals = prompt_goals()
    # Prompt student for start and end times for each day
    start_hr, start_min = prompt_day_times(
        "Enter the time that you start your day based on the 24-hour clock. Specify hour followed "
        "by minutes separated by comma: ")
    end_hr, end_min = prompt_day_times("Enter the time that you end your day based on the 24-hour clock. Specify hour followed by "
                                        "minutes separated by comma: ")
    # Prompt student for start times and duration for each meal
    breakfast_hr, breakfast_min, lunch_hr, lunch_min, dinner_hr, dinner_min = prompt_meal_times()
    meal_duration = input("Enter in minutes how long each meal should last: ")
    # Prompt student for their preferred number of breaks and duration of each break for all days
    breaks_num, break_duration = prompt_breaks()
    title = f"{name}'s Final Exam Week Five-Day Study Plan"
    # Construct prompt according to student information
    prompt = generate_prompt(
        name=name,
        topics_str=topics_str,
        start_hr=start_hr,
        start_min=start_min,
        end_hr=end_hr,
        end_min=end_min,
        breakfast_hr=breakfast_hr,
        breakfast_min=breakfast_min,
        lunch_hr=lunch_hr,
        lunch_min=lunch_min,
        dinner_hr=dinner_hr,
        dinner_min=dinner_min,
        meal_duration=meal_duration,
        breaks_num=breaks_num,
        break_duration=break_duration,
        hours=hours,
        minutes=minutes,
        preferences=preferences,
        priority_subjects=priority_subjects,
        goals=goals,
    )
    # Retrieve generated schedule in JSON format
    response = get_completion(prompt)
    try:
        schedule_dict = json.loads(response)
        print(schedule_dict)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
    # Plot study schedule
    create_schedule(
        schedule_dict=schedule_dict,
        start_hr=start_hr,
        start_min=start_min,
        end_hr=end_hr,
        end_min=end_min,
        name=name,
        title=title,
        days=days,
        colors=colors
    )


if __name__ == "__main__":
    main()















