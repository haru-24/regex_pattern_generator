#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""utterance pattern generator."""
import json
import re
import itertools
import argparse


def main(input_path: str, output_path: str = ""):
    """Utterance pattern generator main function."""
    json_open = open(input_path, 'r')
    intent_name = ""
    utterance_pattern_dict: dict[str, list[str]] = json.load(json_open)
    utterance_pattern_list: list[str] = []
    replace_utterance = ""

    for key in utterance_pattern_dict.keys():
        intent_name = key

    for values in utterance_pattern_dict.values():
        for rep_str in values:
            replace_str = rep_str.strip("^$")
            utterance_pattern_list.append(replace_str)

    for utterance_pattern in utterance_pattern_list:
        multi_puttern_utterance_list: list[str] = re.findall(
            r"\(.*?\)", utterance_pattern)

        replace_utterance = utterance_pattern
        sampling_utterance_list: list[list[str]] = []

        for i, multi_puttern_utterance in enumerate(multi_puttern_utterance_list):

            replace_utterance = replace_utterance.replace(
                multi_puttern_utterance, f"({str(i)})")

            split_list = multi_puttern_utterance[1:-1].split("|")
            sampling_utterance_list.append(split_list)

        utterance_combinations = list(
            itertools.product(*sampling_utterance_list))

        for utterance_combination in utterance_combinations:
            result = replace_utterance
            for j, utterance in enumerate(utterance_combination):
                result = result.replace(f"({str(j)})", utterance)

            print(result)
            if output_path:
                file = open(output_path, 'a')
                file.write(f"{result}\n")
            else:
                file = open(
                    f"{intent_name}_pattern.txt", 'a')
                file.write(f"{result}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path",
                        required=True,
                        help="")

    parser.add_argument("--output_path",
                        required=False,
                        help="")
    args = parser.parse_args()
    main(input_path=args.input_path, output_path=args.output_path)
