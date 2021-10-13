import json
import logging
import tempfile
import pymsteams

from hikaru import DiffType

from ...core.model.events import *
from ...core.reporting.blocks import *
from ...core.reporting.utils import add_pngs_for_all_svgs
from ...core.reporting.callbacks import PlaybookCallbackRequest
from ...core.reporting.consts import SlackAnnotations
from ...core.model.env_vars import TARGET_ID

ACTION_TRIGGER_PLAYBOOK = "trigger_playbook"
MsTeamsBlock = Dict[str, Any]

class MsTeamsImplementation:

    def __init__(self, msteams_hookurl: str, title: str, description: str):
        try:
            self.myTeamsMessage = pymsteams.connectorcard(msteams_hookurl)
            self.myTeamsMessage
        except Exception as e:
            logging.error(f"Cannot connect to MsTeams Channel: {e}")
            raise e

    def __markdown_block(self, card: pymsteams.connectorcard, block: BaseBlock):
      if not block.text:
          return []
      return [
          {
              "type": "section",
              "text": {
                  "type": "mrkdwn",
                  "text": self.__apply_length_limit(block.text),
              },
          }
      ]

    def __divider_block(self, card: pymsteams.connectorcard, block: BaseBlock):
      return [{"type": "divider"}]

    def __header_block(self, card: pymsteams.connectorcard, block: BaseBlock):
      return [
          {
              "type": "header",
              "text": {
                  "type": "plain_text",
                  "text": self.__apply_length_limit(block.text, 150),
              },
          }
      ]

    def __get_action_block_for_choices(self, card: pymsteams.connectorcard, choices: Dict[str, Callable] = None, context=""):
      if choices is None:
          return []

      buttons = []
      for (i, (text, callback)) in enumerate(choices.items()):
          buttons.append(
              {
                  "type": "button",
                  "text": {
                      "type": "plain_text",
                      "text": text,
                  },
                  "style": "primary",
                  "action_id": f"{ACTION_TRIGGER_PLAYBOOK}_{i}",
                  "value": PlaybookCallbackRequest.create_for_func(
                      callback, context, text
                  ).json(),
              }
          )

      return [{"type": "actions", "elements": buttons}]

    def __apply_length_limit(self, msg: str, max_length: int = 3000):
      if len(msg) <= max_length:
          return msg
      truncator = "..."
      return msg[: max_length - len(truncator)] + truncator

