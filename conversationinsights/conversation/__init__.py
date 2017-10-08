from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from typing import List
from typing import Text

from conversationinsights.events import Event


class Dialogue(object):
    """A dialogue comprises a list of Turn objects"""

    def __init__(self, name, events):
        # type: (Text, List[Event]) -> None

        self.name = name
        self.events = events

    def __str__(self):
        return "Dialogue with name '{}' and turns:\n{}".format(self.name,
                                                               "\n\n".join(["\t{}".format(t) for t in self.events]))


class Topic(object):
    """topic of conversation"""

    def __init__(self, name):
        self.name = name
