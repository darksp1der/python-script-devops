import datetime
from datetime import datetime

def count_logs(logs):
    log_count = {}

    for log in logs:
        parts = log.split(" - ")

        log_level = parts[1].strip("[]")
        app_type = parts[2].split(" ")[0]

        if app_type not in log_count:
            log_count[app_type] = {"INFO": 0, "DEBUG": 0, "ERROR": 0}

        if log_level == "INFO":
            log_count[app_type][log_level] += 0.5
        else:
            log_count[app_type][log_level] += 1

    for app in log_count:
        log_count[app]["INFO"] = round(log_count[app]["INFO"])

    return log_count

def calculate_average_run_time(logs):
    total_run_time = {}
    run_count = {}

    for log in logs:
        parts = log.split(" - ")
        if 'successfully' not in log:
            continue

        app_type = parts[2].split(" ")[0]
        if app_type == 'SYSTEM':
            continue

        time_info = parts[2].split("in ")
        time_ms_str = time_info[1].split("ms")[0]

        if time_ms_str.isdigit():
            time_ms = int(time_ms_str)
            total_run_time.setdefault(app_type, 0)
            run_count.setdefault(app_type, 0)
            total_run_time[app_type] += time_ms
            run_count[app_type] += 1

    average_run_time = {}
    for app in total_run_time:
        average_run_time[app] = round(total_run_time[app] / run_count[app], 2) if run_count[app] > 0 else 0

    return average_run_time

def count_failures(logs):
    failure_count = {}

    for log in logs:
        parts = log.split(" - ")

        log_level = parts[1].strip("[]")
        if log_level != "ERROR":
            continue

        app_type = parts[2].split(" ")[0]
        failure_count.setdefault(app_type, 0)
        failure_count[app_type] += 1

    return failure_count

def app_with_most_failures(failure_counts):
    if not failure_counts:
        return "No application has failed", 0

    max_app = max(failure_counts, key=failure_counts.get)
    max_failures = failure_counts[max_app]

    return max_app, max_failures

def app_with_most_successful_runs(log_counts):
    max_info = 0
    max_app = "None"

    for app, counts in log_counts.items():
        if counts["INFO"] > max_info:
            max_info = counts["INFO"]
            max_app = app

    return max_app, max_info

def time_period_with_most_failures(logs):
    failure_counts = {'00:00:00 - 07:59:59': 0, '08:00:00 - 15:59:59': 0, '16:00:00 - 23:59:59': 0}

    for log in logs:
        parts = log.split(" - ")

        log_level = parts[1].strip("[]")
        if log_level != "ERROR":
            continue

        timestamp = parts[0]
        time = datetime.strptime(timestamp, "%H:%M:%S").time()

        if time < datetime.strptime("08:00:00", "%H:%M:%S").time():
            failure_counts['00:00:00 - 07:59:59'] += 1
        elif time < datetime.strptime("16:00:00", "%H:%M:%S").time():
            failure_counts['08:00:00 - 15:59:59'] += 1
        else:
            failure_counts['16:00:00 - 23:59:59'] += 1

    most_failures_period = max(failure_counts, key=failure_counts.get)
    return most_failures_period, failure_counts[most_failures_period]

def calculate_longest_shortest_run_times_per_app(logs):
    run_times = {}

    for log in logs:
        parts = log.split(" - ")
        if 'successfully' not in log:
            continue

        timestamp = parts[0]
        app_info = parts[2].split(" ")
        app_type = app_info[0]

        if app_type == 'SYSTEM':
            continue

        time_info = parts[2].split("in ")
        time_ms_str = time_info[1].split("ms")[0]

        if not time_ms_str.isdigit():
            continue

        time_ms = int(time_ms_str)

        if app_type not in run_times:
            run_times[app_type] = {'min_time': float('inf'), 'max_time': 0, 'min_timestamp': None, 'max_timestamp': None}

        if time_ms < run_times[app_type]['min_time']:
            run_times[app_type]['min_time'] = time_ms
            run_times[app_type]['min_timestamp'] = timestamp

        if time_ms > run_times[app_type]['max_time']:
            run_times[app_type]['max_time'] = time_ms
            run_times[app_type]['max_timestamp'] = timestamp

    return run_times

def most_active_hour_per_app(logs):
    activity_count = {}

    for log in logs:
        parts = log.split(" - ")

        timestamp = parts[0]
        hour = timestamp.split(":")[0]
        app_type = parts[2].split(" ")[0]

        if app_type not in activity_count:
            activity_count[app_type] = {f"{hour}:00:00 - {hour}:59:59": 1}
        else:
            if f"{hour}:00:00 - {hour}:59:59" in activity_count[app_type]:
                activity_count[app_type][f"{hour}:00:00 - {hour}:59:59"] += 1
            else:
                activity_count[app_type][f"{hour}:00:00 - {hour}:59:59"] = 1

    most_active_hours = {}
    for app, hours in activity_count.items():
        most_active_hour = max(hours, key=hours.get)
        most_active_hours[app] = most_active_hour

    return most_active_hours

def calculate_failure_rate(log_counts, failure_counts):
    failure_rate = {}

    for app_type, counts in log_counts.items():
        total_logs = sum(counts.values())
        error_logs = failure_counts.get(app_type, 0)
        if total_logs > 0:
            failure_rate[app_type] = (error_logs / total_logs) * 100
        else:
            failure_rate[app_type] = 0

    return failure_rate

file_path = r'C:\Users\mauro\PycharmProjects\python-script\logs.txt'
with open(file_path, 'r') as file:
    log_data = file.readlines()

log_counts = count_logs(log_data)
average_run_times = calculate_average_run_time(log_data)
failure_counts = count_failures(log_data)
app_most_failures, max_failures = app_with_most_failures(failure_counts)
app_most_success, max_successes = app_with_most_successful_runs(log_counts)
most_failures_period, period_failure_count = time_period_with_most_failures(log_data)
longest_shortest_run_times = calculate_longest_shortest_run_times_per_app(log_data)
most_active_hours = most_active_hour_per_app(log_data)
failure_rates = calculate_failure_rate(log_counts, failure_counts)

print("Log Counts:", log_counts, end='\n\n')
print("Average Run Times:", average_run_times, end='\n\n')
print("Failure Counts:", failure_counts, end='\n\n')
print(f"Application with the most failures (ERROR): {app_most_failures}: {max_failures}", end='\n\n')
print(f"Application with the most successful runs (INFO): {app_most_success}: {max_successes}", end='\n\n')
print(f"Time interval with the most failed runs: {most_failures_period} ({period_failure_count} failures)", end='\n\n')

for app_type, times_info in longest_shortest_run_times.items():
    print(f"App Type: {app_type}")
    print(f"Longest Run Time: {times_info['max_time']} ms at {times_info['max_timestamp']}")
    print(f"Shortest Run Time: {times_info['min_time']} ms at {times_info['min_timestamp']}")
    print("----------------------------------------")

print("\nMost Active Hours Per App Type:")
for app_type, active_hour in most_active_hours.items():
    print(f"{app_type}: {active_hour}")

print("\nFailure Rates Per App Type:")
for app_type, rate in failure_rates.items():
    print(f"{app_type}: {rate:.2f}%")
