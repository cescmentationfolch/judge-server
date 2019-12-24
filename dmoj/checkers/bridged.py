import os
import subprocess

from dmoj.judgeenv import env, get_problem_root
from dmoj.result import CheckerResult
from dmoj.utils.aux_files import check_aux_file_result, compile_with_auxiliary_files, mktemp
from dmoj.utils.unicode import utf8text

executor = None


def get_executor(files, lang, compiler_time_limit, problem_id):
    global executor

    if executor is None:
        if not isinstance(files, list):
            files = [files]
        filenames = [os.path.join(get_problem_root(problem_id), f) for f in files]
        executor = compile_with_auxiliary_files(filenames, lang, compiler_time_limit)

    return executor


def check(process_output, judge_output, judge_input, problem_id,
          files, lang, time_limit=env['generator_time_limit'], memory_limit=env['generator_memory_limit'],
          compiler_time_limit=env['generator_compiler_limit'], feedback=True,
          point_value=None, **kwargs) -> CheckerResult:
    executor = get_executor(files, lang, compiler_time_limit, problem_id)

    with mktemp(judge_input) as input_file, mktemp(process_output) as output_file, mktemp(judge_output) as judge_file:
        process = executor.launch(input_file.name, output_file.name, judge_file.name, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, memory=memory_limit, time=time_limit)

        proc_output, error = map(utf8text, process.communicate())

        return check_aux_file_result(process, executor, point_value, time_limit, memory_limit,
                                     feedback=utf8text(proc_output) if feedback else None, name='checker', stderr=error)
