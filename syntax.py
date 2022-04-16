CMD_RE = r'^\s*(?P<cmd>[a-z]{2,})'

OPTS_RE = r'(?:\s(--\w[\w-]+|-\w))'
OPTS_WITH_ARGS_RE = r'(\s(--\w[\w-]+|-\w)=([a-zA-Z]|[0-9]+))'

QUOTED_ARGS_RE = r'(?:\s"(.*?)")'
ARGS_RE = r'(?:\s(\w+))'

CORRECT_SYNTAX = overall = f'{CMD_RE}({OPTS_RE}|{OPTS_WITH_ARGS_RE})*({QUOTED_ARGS_RE}|{ARGS_RE})*\s*$'
