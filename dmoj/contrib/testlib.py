from dmoj.contrib.default import ContribModule as BaseContribModule


class ContribModule:
    AC = 0
    WA = 1
    PE = 2
    IE = 3

    def parse_return_code(proc, executor, point_value, time_limit, memory_limit, feedback, name, stderr):
        if proc.returncode == AC:
            return CheckerResult(True, point_value, feedback=feedback)
        elif proc.returncode == WA:
            return CheckerResult(False, 0, feedback=feedback)
        elif proc.returncode == PE:
            return CheckerResult(False, 0, feedback=feedback or 'Presentation Error')
        elif proc.returncode == IE:
            raise InternalError('%s failed assertion with message %s' % (name, feedback))
        else:
            check_aux_file_error(proc, executor, name, stderr, time_limit, memory_limit)