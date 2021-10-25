#!/usr/bin/env python3
#cp -r  /usr/local/lib/python3.9/site-packages/robusta/ /workspaces/robusta/src/
import logging
import os
import os.path
from inspect import getmembers
from typing import Container

from hikaru.meta import DiffDetail, DiffType
from hikaru.model.rel_1_16.v1.v1 import Pod
from robusta.core import reporting

from src.robusta.core.reporting.blocks import DividerBlock, Enrichment, FileBlock, ListBlock, TableBlock, KubernetesDiffBlock
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

    with open('/workspaces/robusta/10.png', 'rb') as f:
        bytes = f.read()
    png_file1 = FileBlock('image.png', bytes)

    text_file = FileBlock('test.txt', b'asaf\n111\222')

    list_block = ListBlock(['item 1','item 2','item 3'])
    
    y1 = DiffDetail(DiffType.ADDED, Container.__class__,'diff in version',[], value='1', other_value='0', report='')
    y2 = DiffDetail(DiffType.ADDED, Container.__class__,'diff in version',[], value='1', other_value='0', report='')
    diff = KubernetesDiffBlock([y1, y2], None, None)
    
    table = TableBlock([['row11', 'row12','row13', 'row14'],['row21', 'row22','row231111111111111111111111111', 'row24']], ['header1', 'header2', 'header3', 'header4'])

    enrichment = Enrichment([diff, list_block, table, markdown,markdown2, jpg_file, jpg_file2, svg_file1, png_file1,text_file])
    finding.enrichments.append(enrichment)
    '''

    markdown = MarkdownBlock('markdown text 22222<br><br>11111\n2222')    
    enrichment = Enrichment([markdown])
    finding.enrichments.append(enrichment) '''    
    hook_url = "https://robusta650.webhook.office.com/webhookb2/b8b2b92a-02e9-4f5b-9c6f-3b77010d9cc6@34408606-07e6-4a82-98ac-c3668f4e57f5/IncomingWebhook/5479ec3149a34b99a0c7bca141787950/82e528f7-78de-4ded-9b84-0c6eb2c4883a"
    MsTeamsSink.write_finding_debug(hook_url, finding)
    print('*** done222 ***')

main()