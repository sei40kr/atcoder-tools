#!/usr/bin/python3

import argparse
import os
import shutil
from atcodertools.common.judgetype import ErrorType, NormalJudge, DecimalJudge, MultiSolutionJudge, InteractiveJudge, JudgeType, NoJudgeTypeException, DEFAULT_EPS
from atcodertools.tools.models.metadata import Metadata
from atcodertools.common.language import Language, ALL_LANGUAGES
from atcodertools.tools.templates import get_default_judge_template_path


def main(prog, args):
    if len(args) == 0:
        print("Usage: atcoder tools set [options]")
        return
    new_judge_type = args[0]

    metadata = Metadata.load_from("./metadata.json")
    old_judge_type = metadata.judge_method.judge_type.value

    parser = argparse.ArgumentParser(
        prog=prog,
        formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('--error-value', '-v',
                        help='error value for decimal number judge:'
                             ' [Default] ' + str(DEFAULT_EPS),
                        type=float,
                        default=None)

    parser.add_argument('--error-type', '-t',
                        help='error type'
                             ' must be one of [{}]'.format(
                                 ', '.join([x.value for x in list(ErrorType)])),
                        type=str,
                        default=None)

    parser.add_argument("--lang",
                        help="Programming language of your template code, {}.\n".format(
                            " or ".join([lang.name for lang in ALL_LANGUAGES])),
                        default=None)

    args = parser.parse_args(args[1:])

    if new_judge_type != old_judge_type:
        if new_judge_type == JudgeType.Normal.value:
            metadata.judge_method = NormalJudge()
        elif new_judge_type == JudgeType.Decimal.value:
            metadata.judge_method = DecimalJudge()
        elif new_judge_type == JudgeType.MultiSolution.value:
            metadata.judge_method = MultiSolutionJudge()
        elif new_judge_type == JudgeType.Interactive.value:
            metadata.judge_method = InteractiveJudge()
        else:
            raise NoJudgeTypeException()

    if new_judge_type == JudgeType.Decimal.value:
        if args.error_value is not None:
            metadata.judge_method.diff = args.error_value
        if args.error_type is not None:
            metadata.judge_method.error_type = args.error_type
    elif new_judge_type == JudgeType.MultiSolution.value:
        if not os.path.exists("./judge.cpp"):
            print("touch ./judge.cpp (multi sotlution)")
            judge_template_path = get_default_judge_template_path('cpp')
            shutil.copy(judge_template_path, "./judge.cpp")
        else:
            print("Judge Code exists")
    elif new_judge_type == JudgeType.Interactive.value:
        if not os.path.exists("/judge.cpp"):
            print("touch ./judge.cpp (interactive)")
            judge_template_path = get_default_judge_template_path('cpp')
            shutil.copy(judge_template_path, "./judge.cpp")
        else:
            print("Judge Code exists")
    if args.lang is not None:
        if args.lang != metadata.lang.name:
            metadata.lang = Language.from_name(args.lang)
            # TODO: generate code
    metadata.save_to("./metadata.json")
