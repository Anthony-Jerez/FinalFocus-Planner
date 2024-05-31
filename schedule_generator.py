import matplotlib.pyplot as plt


def create_schedule(schedule_dict, start_hr, start_min, end_hr, end_min, name, title, days, colors):
    week_schedule = []
    # Format schedule to be a list of lists
    for day in range(1, 6):  # 1 to 5 for Monday to Friday
        day_activities = schedule_dict.get(str(day), [])
        week_schedule.append(day_activities)
    # Plot schedule
    fig, ax = plt.subplots(figsize=(10, 5.89))
    # For each day
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
            ax.text(day + 0.02, start + 0.05, '{0}:{1:0>2}'.format(int(start_hour), int(start_minute)), va='bottom',
                    fontsize=6)
            # Plot the subject name
            ax.text(day + 0.48, (start + end) * 0.5, event, ha='center', va='center', fontsize=7)
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
    print(f"{name}'s study plan was successfully created.")
