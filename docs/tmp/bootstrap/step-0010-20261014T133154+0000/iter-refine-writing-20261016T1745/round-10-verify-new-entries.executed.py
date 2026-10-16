import runpy,sys
script='/workspaces/.agent-state/codex/skills/check-paper-citations/scripts/verify_bib.py'
mod=runpy.run_path(script)
original=mod['parse_bib_entries']
keys={'autoverusArtifact','cudaProgrammingGuide'}
actual=original(open('/workspaces/repository/docs/paper/references.bib').read())
assert {x['key'] for x in actual if x['key'] in keys}==keys
mod['main'].__globals__['parse_bib_entries']=lambda text:[e for e in original(text) if e['key'] in keys]
sys.argv=[script,'/workspaces/repository/docs/paper/references.bib']
mod['main']()
