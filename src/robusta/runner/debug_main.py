#!/usr/bin/env python3
#cp -r  /usr/local/lib/python3.9/site-packages/robusta/ /workspaces/robusta/src/
import logging
import os
import os.path
from inspect import getmembers

from src.robusta.core.reporting.blocks import DividerBlock, Enrichment, FileBlock
from src.robusta.core.sinks.sink_config import SinkConfigBase

os.chdir('/app/robusta/runner')

from ..core.reporting.blocks import Finding, MarkdownBlock
from ..core.sinks.msteams.msteams_sink import MsTeamsSink,MsTeamsSinkConfig


print('*** running ***')



def main():

    finding = Finding('some title')
    finding.title = 'test'
    finding.description = 'this is a short desc\n\nanother line'
    markdown = MarkdownBlock('markdown text\n\n11111\n\n2222')
    markdown2 = MarkdownBlock('3333\n444444')    
    #divider = DividerBlock()
    with open('/workspaces/robusta/1.jpg', 'rb') as f:
        bytes = f.read()
    jpg_file = FileBlock('image.jpg', bytes)
    with open('/workspaces/robusta/2.jpg', 'rb') as f:
        bytes = f.read()
    jpg_file2 = FileBlock('image.jpg', bytes)
    with open('/workspaces/robusta/3.svg', 'rb') as f:
        bytes = f.read()
    svg_file1 = FileBlock('image.svg', bytes)

    enrichment = Enrichment([markdown,markdown2, jpg_file, jpg_file2, svg_file1])
    finding.enrichments.append(enrichment)
    '''

    markdown = MarkdownBlock('markdown text 22222<br><br>11111\n2222')    
    enrichment = Enrichment([markdown])
    finding.enrichments.append(enrichment) '''    
    hook_url = "https://robusta650.webhook.office.com/webhookb2/b8b2b92a-02e9-4f5b-9c6f-3b77010d9cc6@34408606-07e6-4a82-98ac-c3668f4e57f5/IncomingWebhook/5479ec3149a34b99a0c7bca141787950/82e528f7-78de-4ded-9b84-0c6eb2c4883a"
    MsTeamsSink.write_finding_debug(hook_url, finding)
    print('*** done222 ***')

main()