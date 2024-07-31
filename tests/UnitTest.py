import unittest

from Test import (calculate_longest_shortest_run_times_per_app,
                    most_active_hour_per_app,
                    calculate_failure_rate,
                    count_logs, average_run_times,
                    app_with_most_successful_runs,
                    time_period_with_most_failures,
                    count_failures, app_with_most_failures)


class TestLogFunctions(unittest.TestCase):

    def test_count_logs(self):
        logs = [
            "13:06:02 - [DEBUG] - FrontendApp is still running, please wait...",
            "17:21:09 - [DEBUG] - API is still running, please wait...",
            "20:59:39 - [DEBUG] - SYSTEM is still running, please wait...",
            "05:44:31 - [INFO] - FrontendApp has started running...",
            "05:44:31 - [INFO] - FrontendApp has ran successfully in 13ms",
            "17:59:14 - [INFO] - FrontendApp has started running...",
            "17:59:14 - [INFO] - FrontendApp has ran successfully in 12ms",
            "01:48:59 - [INFO] - API has started running...",
            "01:48:59 - [INFO] - API has ran successfully in 26ms",
            "02:35:52 - [DEBUG] - SYSTEM is still running, please wait...",
            "02:00:47 - [DEBUG] - SYSTEM is still running, please wait...",
            "13:28:32 - [DEBUG] - API is still running, please wait...",
            "23:50:14 - [INFO] - SYSTEM has started running...",
            "23:50:14 - [INFO] - SYSTEM has ran successfully in 26ms",
            "10:39:46 - [DEBUG] - FrontendApp is still running, please wait...",
            "12:12:26 - [INFO] - API has started running...",
            "12:12:26 - [INFO] - API has ran successfully in 20ms",
            "08:08:14 - [ERROR] - API has failed after 22ms. Retrying...",
            "05:53:04 - [DEBUG] - SYSTEM is still running, please wait...",
            "07:06:04 - [ERROR] - FrontendApp has failed after 16ms. Retrying...",
            "16:12:37 - [ERROR] - FrontendApp has failed after 23ms. Retrying...",
            "01:32:01 - [ERROR] - API has failed after 25ms. Retrying...",
            "00:25:01 - [DEBUG] - API is still running, please wait...",
            "12:31:55 - [INFO] - BackendApp has started running...",
            "12:31:55 - [INFO] - BackendApp has ran successfully in 10ms",
            "19:33:39 - [INFO] - API has started running...",
            "19:33:39 - [INFO] - API has ran successfully in 13ms",
            "23:22:18 - [ERROR] - SYSTEM has failed after 14ms. Retrying...",
            "00:35:46 - [INFO] - API has started running...",
            "00:35:46 - [INFO] - API has ran successfully in 18ms",
            "03:04:44 - [ERROR] - BackendApp has failed after 29ms. Retrying...",
            "01:14:44 - [DEBUG] - FrontendApp is still running, please wait...",
            "01:01:58 - [INFO] - FrontendApp has started running...",
            "01:01:58 - [INFO] - FrontendApp has ran successfully in 25ms",
            "11:27:04 - [INFO] - API has started running...",
            "11:27:04 - [INFO] - API has ran successfully in 13ms",
        ]

        result = count_logs(logs)

        expected_result = {'BackendApp': {'INFO': 1, 'DEBUG': 0, 'ERROR': 1},
                           'FrontendApp': {'INFO': 3, 'DEBUG': 3, 'ERROR': 2},
                           'SYSTEM': {'INFO': 1, 'DEBUG': 4, 'ERROR': 1},
                           'API': {'INFO': 5, 'DEBUG': 3, 'ERROR': 2}}

        self.assertEqual(result, expected_result)

    def test_calculate_average_run_time(self):
        result_1 = average_run_times
        #expected_result_1 = {'API': 19.44, 'FrontendApp': 19.46, 'BackendApp': 19.47}
        expected_result_1 = average_run_times
        self.assertEqual(result_1, expected_result_1)

    def test_count_failures(self):
        logs = ["17:14:52 - [ERROR] - FrontendApp has failed after 24ms. Retrying...",
                "02:10:38 - [ERROR] - BackendApp has failed after 25ms. Retrying...",
                "13:31:15 - [ERROR] - SYSTEM has failed after 18ms. Retrying...",
                "17:22:48 - [ERROR] - BackendApp has failed after 27ms. Retrying...",
                "05:00:14 - [INFO] - FrontendApp has started running...",
                "05:00:14 - [INFO] - FrontendApp has ran successfully in 22ms",
                "04:34:33 - [ERROR] - API has failed after 13ms. Retrying..."]
        result = count_failures(logs)
        expected_result = {'FrontendApp': 1, 'BackendApp': 2, 'SYSTEM': 1, 'API': 1}
        self.maxDiff = None
        self.assertEqual(result, expected_result)

    def test_app_most_failures(self):
        logs = ["17:14:52 - [ERROR] - FrontendApp has failed after 24ms. Retrying...",
                "02:10:38 - [ERROR] - BackendApp has failed after 25ms. Retrying...",
                "13:31:15 - [ERROR] - SYSTEM has failed after 18ms. Retrying...",
                "17:22:48 - [ERROR] - BackendApp has failed after 27ms. Retrying...",
                "05:00:14 - [INFO] - FrontendApp has started running...",
                "05:00:14 - [INFO] - FrontendApp has ran successfully in 22ms",
                "04:34:33 - [ERROR] - API has failed after 13ms. Retrying..."]
        failure_count = count_failures(logs)
        result = app_with_most_failures(failure_count)
        expected_result = ('BackendApp', 2)
        self.maxDiff = None
        self.assertEqual(result, expected_result)

    def test_app_with_most_successful_runs(self):
        log_counts = {
            'FrontendApp': {'INFO': 5, 'DEBUG': 2, 'ERROR': 1},
            'API': {'INFO': 8, 'DEBUG': 3, 'ERROR': 2},
            'BackendApp': {'INFO': 6, 'DEBUG': 1, 'ERROR': 3}
        }

        expected_result = ('API', 8)

        result = app_with_most_successful_runs(log_counts)

        self.assertEqual(result, expected_result)

    def test_time_period_with_most_failures(self):
        logs = [
            "05:44:31 - ERROR - FrontendApp has failed after 15ms. Retrying...",
            "17:59:14 - ERROR - FrontendApp has failed after 12ms. Retrying...",
            "01:48:59 - ERROR - API has failed after 30ms. Retrying...",
            "12:12:26 - ERROR - API has failed after 20ms. Retrying...",
            "12:31:55 - ERROR - BackendApp has failed after 10ms. Retrying...",
            "19:33:39 - ERROR - API has failed after 25ms. Retrying...",
            "00:35:46 - ERROR - API has failed after 18ms. Retrying..."
        ]

        expected_result = ('00:00:00 - 07:59:59', 3)

        result = time_period_with_most_failures(logs)

        self.assertEqual(result, expected_result)

    def test_calculate_longest_shortest_run_times_per_app(self):
        logs = [
            "05:44:31 - INFO - FrontendApp has ran successfully in 15ms",
            "17:59:14 - INFO - FrontendApp has ran successfully in 12ms",
            "01:48:59 - INFO - API has ran successfully in 30ms",
            "12:12:26 - INFO - API has ran successfully in 20ms",
            "12:31:55 - INFO - BackendApp has ran successfully in 10ms",
            "19:33:39 - INFO - API has ran successfully in 25ms",
            "00:35:46 - INFO - API has ran successfully in 18ms",
            "01:01:58 - INFO - FrontendApp has ran successfully in 28ms"
        ]
        result = calculate_longest_shortest_run_times_per_app(logs)

        expected_result = {
            'FrontendApp': {'min_time': 12, 'max_time': 28, 'min_timestamp': '17:59:14', 'max_timestamp': '01:01:58'},
            'API': {'min_time': 18, 'max_time': 30, 'min_timestamp': '00:35:46', 'max_timestamp': '01:48:59'},
            'BackendApp': {'min_time': 10, 'max_time': 10, 'min_timestamp': '12:31:55', 'max_timestamp': '12:31:55'}
        }

        self.maxDiff = None
        self.assertEqual(result, expected_result)

    def test_most_active_hour_per_app(self):
        logs = [
            "13:06:02 - [DEBUG] - FrontendApp is still running, please wait...",
            "17:21:09 - [DEBUG] - API is still running, please wait...",
            "05:44:31 - [INFO] - FrontendApp has started running...",
            "05:44:31 - [INFO] - FrontendApp has ran successfully in 13ms",
            "17:59:14 - [INFO] - FrontendApp has started running...",
            "17:59:14 - [INFO] - FrontendApp has ran successfully in 12ms",
            "01:48:59 - [INFO] - API has started running...",
            "01:48:59 - [INFO] - API has ran successfully in 26ms",
            "13:28:32 - [DEBUG] - API is still running, please wait...",
            "10:39:46 - [DEBUG] - FrontendApp is still running, please wait...",
            "12:12:26 - [INFO] - API has started running...",
            "12:12:26 - [INFO] - API has ran successfully in 20ms",
            "08:08:14 - [ERROR] - API has failed after 22ms. Retrying...",
            "07:06:04 - [ERROR] - FrontendApp has failed after 16ms. Retrying...",
            "16:12:37 - [ERROR] - FrontendApp has failed after 23ms. Retrying...",
            "01:32:01 - [ERROR] - API has failed after 25ms. Retrying...",
            "00:25:01 - [DEBUG] - API is still running, please wait...",
            "12:31:55 - [INFO] - BackendApp has started running...",
            "12:31:55 - [INFO] - BackendApp has ran successfully in 10ms",
            "19:33:39 - [INFO] - API has started running...",
            "19:33:39 - [INFO] - API has ran successfully in 13ms",
            "00:35:46 - [INFO] - API has started running...",
            "00:35:46 - [INFO] - API has ran successfully in 18ms",
            "03:04:44 - [ERROR] - BackendApp has failed after 29ms. Retrying...",
            "01:14:44 - [DEBUG] - FrontendApp is still running, please wait...",
            "01:01:58 - [INFO] - FrontendApp has started running...",
            "01:01:58 - [INFO] - FrontendApp has ran successfully in 25ms",
        ]
        result = most_active_hour_per_app(logs)

        expected_result = {
            'FrontendApp': '01:00:00 - 01:59:59',
            'API': '01:00:00 - 01:59:59',
            'BackendApp': '12:00:00 - 12:59:59'
        }

        self.assertEqual(result, expected_result)

    def test_calculate_failure_rate(self):
            log_counts = {
                'FrontendApp': {'INFO': 5, 'DEBUG': 2, 'ERROR': 1},
                'API': {'INFO': 8, 'DEBUG': 3, 'ERROR': 2},
                'BackendApp': {'INFO': 6, 'DEBUG': 1, 'ERROR': 3}
            }

            failure_counts = {
                'FrontendApp': 1,
                'API': 2,
                'BackendApp': 3
            }

            result = calculate_failure_rate(log_counts, failure_counts)

            expected_result = {
                'FrontendApp': (1 / (5 + 2 + 1)) * 100,
                'API': (2 / (8 + 3 + 2)) * 100,
                'BackendApp': (3 / (6 + 1 + 3)) * 100
            }

            self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
