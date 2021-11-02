
import re
class MsTeamsMarkDOwnFixUrl:

    PRE_LINK_HEADER = '(<http'
    MIDDLE_SEPARATOR = '|'
    POST_LINK_HEADER = '>)'
    ESCAPE_CHAR = '\\'

    @staticmethod
    def fix_text(text: str):
        
        pattern = re.compile(r'\(<http.*\|.*>\)')

        new_text = text
        for bad_url in re.findall(r'<http.*\|.*>', text):
            good_url = MsTeamsMarkDOwnFixUrl.__fix_url(bad_url)
            new_text = new_text.replace(bad_url, good_url)
        return new_text
    @staticmethod
    def __fix_url(bad_url : str):
        parts = bad_url.replace('<', '').replace('>','').split('|')
        url = '(' + parts[0] + ')'
        description = '[' + parts[1] + ']'

        return description + url



