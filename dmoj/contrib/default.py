from dmoj.result import CheckerResult
from dmoj.utils.aux_files import check_aux_file_error


class ContribModule:
    AC = 0
    WA = 1

    def parse_return_code(proc, executor, point_value, time_limit, memory_limit, feedback, name, stderr):
        if proc.returncode == self.AC:
            return CheckerResult(True, point_value, feedback=feedback)
        elif proc.returncode == self.WA:
            return CheckerResult(False, point_value, feedback=feedback)
        else:
            check_aux_file_error(proc, executor, name, stderr, time_limit, memory_limit)