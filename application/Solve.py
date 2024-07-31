from ImportLogs import file
from datetime import datetime

ct_info_Frontend = 0
ct_debug_Frontend = 0
ct_error_Frontend = 0
ct_info_Backend = 0
ct_debug_Backend = 0
ct_error_Backend = 0
ct_info_API = 0
ct_debug_API = 0
ct_error_API = 0
ct_info_SYSTEM = 0
ct_debug_SYSTEM = 0
ct_error_SYSTEM = 0

consecutive_info_count = 0

total_runtime_Frontend = 0
total_runtime_Backend = 0
total_runtime_API = 0

timestamp1 = "00:00:00"
timestamp2 = "07:59:59"
timestamp3 = "08:00:00"
timestamp4 = "15:59:59"
timestamp5 = "16:00:00"
timestamp6 = "23:59:59"

timestamp1 = datetime.strptime(timestamp1, "%H:%M:%S").time()
timestamp2 = datetime.strptime(timestamp2, "%H:%M:%S").time()
timestamp3 = datetime.strptime(timestamp3, "%H:%M:%S").time()
timestamp4 = datetime.strptime(timestamp4, "%H:%M:%S").time()
timestamp5 = datetime.strptime(timestamp5, "%H:%M:%S").time()
timestamp6 = datetime.strptime(timestamp6, "%H:%M:%S").time()

firstIntervalOfDay = 0
secondIntervalOfDay = 0
thirdIntervalOfDay = 0

errors_per_day = {'Frontend': {}, 'Backend': {}, 'API': {}, 'SYSTEM': {}}
total_logs_per_day = {'Frontend': {}, 'Backend': {}, 'API': {}, 'SYSTEM': {}}

with open(file, 'r') as f:
    for line in f:
        parts = line.split('-')
        log_type = parts[1].strip()

        has_ms = 'ms' in parts[-1] and 'INFO' in log_type
        runtime_parts = parts[-1].split('ms')
        runtime = int(runtime_parts[0].split()[-1].strip()) if has_ms else 0

        log_timestamp = line.split(' - ')[0]
        log_datetime = datetime.strptime(log_timestamp, '%H:%M:%S')
        log_date = log_datetime.date()
        log_time = log_datetime.time()

        total_logs_per_day.setdefault('Frontend', {}).setdefault(log_date, 0)
        total_logs_per_day['Frontend'][log_date] += 1

        total_logs_per_day.setdefault('Backend', {}).setdefault(log_date, 0)
        total_logs_per_day['Backend'][log_date] += 1

        total_logs_per_day.setdefault('API', {}).setdefault(log_date, 0)
        total_logs_per_day['API'][log_date] += 1

        total_logs_per_day.setdefault('SYSTEM', {}).setdefault(log_date, 0)
        total_logs_per_day['SYSTEM'][log_date] += 1

        if 'INFO' in log_type and 'Frontend' in line:
            if consecutive_info_count == 0:
                ct_info_Frontend += 1
                consecutive_info_count += 1
            else:
                consecutive_info_count = 0
                total_runtime_Frontend += runtime
        elif 'DEBUG' in log_type and 'Frontend' in line:
            ct_debug_Frontend += 1
        elif 'ERROR' in log_type and 'Frontend' in line:
            ct_error_Frontend += 1

            errors_per_day.setdefault('Frontend', {}).setdefault(log_date, 0)
            errors_per_day['Frontend'][log_date] += 1

        elif 'INFO' in log_type and 'Backend' in line:
            if consecutive_info_count == 0:
                ct_info_Backend += 1
                consecutive_info_count += 1
            else:
                consecutive_info_count = 0
                total_runtime_Backend += runtime
        elif 'DEBUG' in log_type and 'Backend' in line:
            ct_debug_Backend += 1
        elif 'ERROR' in log_type and 'Backend' in line:
            ct_error_Backend += 1

            errors_per_day.setdefault('Backend', {}).setdefault(log_date, 0)
            errors_per_day['Backend'][log_date] += 1

        elif 'INFO' in log_type and 'API' in line:
            if consecutive_info_count == 0:
                ct_info_API += 1
                consecutive_info_count += 1
            else:
                consecutive_info_count = 0
                total_runtime_API += runtime
        elif 'DEBUG' in log_type and 'API' in line:
            ct_debug_API += 1
        elif 'ERROR' in log_type and 'API' in line:
            ct_error_API += 1

            errors_per_day.setdefault('API', {}).setdefault(log_date, 0)
            errors_per_day['API'][log_date] += 1

        elif 'INFO' in log_type and 'SYSTEM' in line:
            if consecutive_info_count == 0:
                ct_info_SYSTEM += 1
                consecutive_info_count += 1
            else:
                consecutive_info_count = 0
        elif 'DEBUG' in log_type and 'SYSTEM' in line:
            ct_debug_SYSTEM += 1
        elif 'ERROR' in log_type and 'SYSTEM' in line:
            ct_error_SYSTEM += 1

            errors_per_day.setdefault('SYSTEM', {}).setdefault(log_date, 0)
            errors_per_day['SYSTEM'][log_date] += 1

        # 6
        if 'ERROR' in log_type:
            if timestamp1 < log_time < timestamp2:
                firstIntervalOfDay += 1
            elif timestamp3 < log_time < timestamp4:
                secondIntervalOfDay += 1
            elif timestamp5 < log_time < timestamp6:
                thirdIntervalOfDay += 1

    # 1
    print('Frontend:', 'Info', ct_info_Frontend, 'Debug', ct_debug_Frontend, 'Error', ct_error_Frontend)
    print('Backend:', 'Info', ct_info_Backend, 'Debug', ct_debug_Backend, 'Error', ct_error_Backend)
    print('API:', 'Info', ct_info_API, 'Debug', ct_debug_API, 'Error', ct_error_API)
    print('System:', 'Info ', ct_info_SYSTEM, 'Debug', ct_debug_SYSTEM, 'Error', ct_error_SYSTEM)
    print()

    # 2
    avg_runtime_Frontend = round(total_runtime_Frontend / ct_info_Frontend, 2)
    print('Average Frontend Successful Run Time:', avg_runtime_Frontend, 'ms')
    avg_runtime_Backend = round(total_runtime_Backend / ct_info_Backend, 2)
    print('Average Backend Successful Run Time:', avg_runtime_Backend, 'ms')
    avg_runtime_API = round(total_runtime_API / ct_info_API, 2)
    print('Average API Successful Run Time:', avg_runtime_API, 'ms')
    print()

    # 3
    for app in ['Frontend', 'Backend', 'API', 'SYSTEM']:
        errors = errors_per_day.get(app, {})
        total_logs = total_logs_per_day.get(app, {})
        print(f'{app} Errors per Day: {", ".join([f"{errors.get(date, 0) / max(total_logs.get(date, 1), 1):.3f}" for date in total_logs])}')

    # 4
    print()
    failed_runs = {app: sum(errors.values()) for app, errors in errors_per_day.items()}
    max_failed_app = max(failed_runs, key=failed_runs.get)
    max_failed_runs = failed_runs[max_failed_app]
    print("App with the most failed runs:", max_failed_app, "with", max_failed_runs, "failed runs")

    # 5
    print()
    max_successful_app = ''
    max_successful_runs = 0

    successful_runs = {
        'Frontend': ct_info_Frontend,
        'Backend': ct_info_Backend,
        'API': ct_info_API,
        'SYSTEM': ct_info_SYSTEM
    }

    for app, successful_count in successful_runs.items():
        if successful_count > max_successful_runs:
            max_successful_runs = successful_count
            max_successful_app = app

    print("App with the most successful runs (INFO):", max_successful_app, "with", max_successful_runs, "successful runs")

    # 6
    print()
    max_errors = max(firstIntervalOfDay, secondIntervalOfDay, thirdIntervalOfDay)
    if max_errors == firstIntervalOfDay:
        print(f"The third of the day with the most failed runs (ERROR logs) is: {timestamp1} - {timestamp2}")
    elif max_errors == secondIntervalOfDay:
        print(f"The third of the day with the most failed runs (ERROR logs) is: {timestamp3} - {timestamp4}")
    elif max_errors == thirdIntervalOfDay:
        print(f"The third of the day with the most failed runs (ERROR logs) is: {timestamp5} - {timestamp6}")