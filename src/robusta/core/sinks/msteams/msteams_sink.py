import traceback, sys
from pydantic.main import BaseModel

from ..sink_config import SinkConfigBase
from ....integrations.msteams import MsTeamskSender
from ....integrations.msteams import MsTeamsImplementation
from ...reporting.blocks import Finding
from ..sink_base import SinkBase
import logging


class MsTeamsSinkConfig(BaseModel):
    msteams_hookurl: str

class MsTeamsSink(SinkBase):
    def __init__(self, sink_config: SinkConfigBase):
        super().__init__(sink_config)
        config = MsTeamsSinkConfig(**sink_config.params)
        self.msteams_hookurl = config.msteams_hookurl
        self.sink_name = 'MsTeams'

    def write_finding(self, finding: Finding):
        MsTeamsSinkConfig.__send_to_msteams(self.msteams_hookurl, finding)

    @staticmethod
    def send_to_msteams(msteams_hookurl: str, finding: Finding):
        try:
            msteams_implementation = MsTeamsImplementation(msteams_hookurl, finding.title, finding.description)
            msTeamskSender = MsTeamskSender()
            msTeamskSender.send_finding_to_msteams(msteams_implementation, finding)
        except Exception as e:
            logging.error(f"error in MsTeams Channel: {e}\n\n" + traceback.format_exc())

