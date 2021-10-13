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

  @staticmethod
  def __markdown_block(card: pymsteams.connectorcard, block: BaseBlock):
      if not block.text:
          return []
      return [
          {
              "type": "section",
              "text": {
                  "type": "mrkdwn",
                  "text": MsTeamsImplementation.__apply_length_limit(block.text),
              },
          }
      ]

  @staticmethod
  def __divider_block(card: pymsteams.connectorcard, block: BaseBlock):
      return [{"type": "divider"}]

  @staticmethod
  def __header_block(card: pymsteams.connectorcard, block: BaseBlock):
      return [
          {
              "type": "header",
              "text": {
                  "type": "plain_text",
                  "text": MsTeamsImplementation.__apply_length_limit(block.text, 150),
              },
          }
      ]

  @staticmethod
  def __get_action_block_for_choices(card: pymsteams.connectorcard, choices: Dict[str, Callable] = None, context=""):
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

  @staticmethod
  def __apply_length_limit(msg: str, max_length: int = 3000):
      if len(msg) <= max_length:
          return msg
      truncator = "..."
      return msg[: max_length - len(truncator)] + truncator

