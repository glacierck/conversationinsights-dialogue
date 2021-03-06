from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import logging
from builtins import str

from conversationinsights.agent import Agent
from conversationinsights.policies.keras_policy import KerasPolicy
from conversationinsights.policies.memoization import MemoizationPolicy


def create_argument_parser():
    parser = argparse.ArgumentParser(
            description='trains a dialogue model')
    parser.add_argument(
            '-s', '--stories',
            type=str,
            required=True,
            help="file that contains the stories to train on")
    parser.add_argument(
            '-o', '--out',
            type=str,
            required=True,
            help="directory to persist the trained model in")
    parser.add_argument(
            '-d', '--domain',
            type=str,
            required=True,
            help="domain specification yaml file")
    parser.add_argument(
            '-v', '--verbose',
            default=True,
            help="use verbose logging")
    parser.add_argument(
            '--history',
            default=3,
            help="max history to use of a story")
    parser.add_argument(
            '--epochs',
            default=100,
            help="number of epochs to train the model")
    parser.add_argument(
            '--batch_size',
            default=20,
            help="number of training samples to put into one training batch")
    parser.add_argument(
            '--augmentation',
            default=50,
            help="how much data augmentation to use during training")

    return parser


def train_dialogue_model(domain_file, stories_file, output_path, kwargs):
    agent = Agent(domain_file, policies=[MemoizationPolicy(), KerasPolicy()])

    agent.train(
            stories_file,
            validation_split=0.1,
            **kwargs
    )

    agent.persist(output_path)


if __name__ == '__main__':

    # Running as standalone python application
    arg_parser = create_argument_parser()
    cmdline_args = arg_parser.parse_args()

    logging.basicConfig(level="DEBUG" if cmdline_args.verbose else "INFO")

    additional_arguments = {
        "max_history": cmdline_args.history,
        "epochs": cmdline_args.epochs,
        "batch_size": cmdline_args.batch_size,
        "augmentation_factor": cmdline_args.augmentation
    }

    train_dialogue_model(cmdline_args.domain,
                         cmdline_args.stories,
                         cmdline_args.out,
                         additional_arguments)
