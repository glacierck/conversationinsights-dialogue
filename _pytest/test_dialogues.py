from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import glob
import json

import io
import jsonpickle
import pytest as pytest

from conversationinsights.actions import QuestionTopic
from conversationinsights.domain import TemplateDomain
from conversationinsights.tracker_store import InMemoryTrackerStore
from utilities import tracker_from_dialogue_file


@pytest.mark.parametrize("filename", glob.glob('data/test_dialogues/*json'))
def test_dialogue_serialisation(filename):
    print("testing file: {0}".format(filename))
    with io.open(filename, "r") as f:
        dialogue_json = f.read()
    restored = json.loads(dialogue_json)
    tracker = tracker_from_dialogue_file(filename)
    en_de_coded = json.loads(jsonpickle.encode(tracker.as_dialogue()))
    assert restored == en_de_coded


@pytest.mark.parametrize("filename", glob.glob('data/test_dialogues/*json'))
def test_inmemory_tracker_store(filename):
    domain = TemplateDomain.load("data/test_domains/default_with_topic.yml")
    tracker = tracker_from_dialogue_file(filename, domain)
    tracker_store = InMemoryTrackerStore(domain)
    tracker_store.save(tracker)
    restored = tracker_store.retrieve(tracker.sender_id)
    assert restored == tracker


def test_tracker_restaurant():
    domain = TemplateDomain.load("data/test_domains/default_with_slots.yml")
    filename = 'data/test_dialogues/restaurant_search.json'
    tracker = tracker_from_dialogue_file(filename, domain)
    assert tracker.get_slot("cuisine") == "indian"
    assert tracker.get_slot("location") == "central"


def test_topic_question():
    filename = 'data/test_dialogues/topic_question.json'
    tracker = tracker_from_dialogue_file(filename, TemplateDomain.load("data/test_domains/default_with_topic.yml"))
    question_topic = QuestionTopic
    assert tracker.topic_stack.top.name == question_topic.name
