from pydantic.main import BaseModel

from ..sink_config import SinkConfigBase
from ....integrations.msteams import MsTeamskSender
from ...reporting.blocks import Finding
from ..sink_base import SinkBase


class MsTeamsSinkConfig(BaseModel):
    msteams_hookurl: str

class MsTeamsSink(SinkBase):
    def __init__(self, sink_config: SinkConfigBase):
        super().__init__(sink_config)
        config = MsTeamsSinkConfig(**sink_config.params)
        self.msteams_hookurl = config.msteams_hookurl
        self.sink_name = 'MsTeams'

    def write_finding(self, finding: Finding):
        msTeamskSender = MsTeamskSender(self.msteams_hookurl)
        msTeamskSender.send_finding_to_msteams(finding)
