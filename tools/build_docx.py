# Team-doc publishing: md -> scrubs -> diagram swap -> pandoc docx (run make_reference_docx.py + render_diagrams.py first)
import re, os, subprocess
os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DGDIR = 'tracks/c-usdc-vasp-privy/research/diagrams/'
OUT = '.build/docx'
os.makedirs(OUT, exist_ok=True)

# team scrubs (same intent as before: no internal-workflow language, repo-path refs made team-friendly)
def scrubs_for(name):
    common = []
    if name == 'prd':
        return [
          (re.compile(r'\*\*Surfaces:\*\*.*?\n'), '*Team copy, published from the working draft. Comment here or ping Steve; canonical status lives in the working draft.*\n'),
          (re.compile(r'Working copy: Claude Doc \(claude\.ai[^)]*\) · team snapshots: Google Docs · repo mirror: this file'), 'This folder (team copy) · engineering mirror in the project repo'),
          (re.compile(r'Claude Doc: claude\.ai/code/artifact/[a-z0-9-]+'), 'shared separately when finalized'),
          (re.compile(r'`research/([a-z-]+\.md)`'), r'"\1" — this folder / project repo'),
          (re.compile(r'`\.\./\.\./([A-Za-z.-]+\.md)`'), r'"\1" (project repo)'),
          (re.compile(r'`\.\./TRACKS\.md` \(internal\)'), 'project repo (internal)'),
          (re.compile(r' \(no cross-track framing, per Steve 9/23\)'), ''),
        ]
    if name == 'coinsph':
        return [
          (re.compile(r'now in `inbox/processed/`'), 'archived'),
          (re.compile(r'\(Slack file F0C2DP9PM4N[^)]*\)'), '(received via Slack)'),
          (re.compile(r'permalink in `SOURCES\.md`'), 'permalink in the project bibliography'),
        ]
    if name == 'ledger':
        return [(re.compile(r'\(Notion, fetched 9/23 → SOURCES\.md\)'), '(Notion)')]
    if name == 'privyearn':
        return [
          (re.compile(r'links via Pete, eng — Slack DM 8/24'), 'links via engineering'),
          (re.compile(r'`inbox/processed/[^`]*`'), 'project archive'),
        ]
    if name == 'tracker':
        return [
          (re.compile(r'; original in `inbox/processed/`'), ''),
          (re.compile(r'\(`tracks/c-usdc-vasp-privy/prd\.md` §6\)'), '(the USDC Dollar Wallet PRD §6 — this folder)'),
        ]
    return common

docs = [
 ('tracks/c-usdc-vasp-privy/prd.md', 'prd', 'USDC Dollar Wallet — PRD', [DGDIR+'fundsflow.png']),
 ('tracks/c-usdc-vasp-privy/research/coinsph-integration.md', 'coinsph', 'Coins.ph Integration — Technical Doc', [DGDIR+'onramp-seq.png']),
 ('tracks/c-usdc-vasp-privy/research/php-ledger-design.md', 'ledger', 'PHP Ledger Design (Unconverted Balances)', [DGDIR+'ledger-postings.png', DGDIR+'order-lifecycle.png']),
 ('tracks/c-usdc-vasp-privy/research/privy-earn.md', 'privyearn', 'Privy Earn — How It Works', [DGDIR+'earn-flow.png']),
 ('tracks/c-usdc-vasp-privy/research/privy-tech-docs.md', 'privytech', 'Privy Platform — Technical Digest', []),
 ('counterparty-counsel-tracker.md', 'tracker', 'Counterparty & Counsel Tracker', []),
]

for src, name, title, pngs in docs:
    md = open(src).read()
    for pat, rep in scrubs_for(name):
        md = pat.sub(rep, md)
    # replace nth mermaid fence with an image reference pandoc will embed
    idx = [0]
    def repl(m):
        i = idx[0]; idx[0] += 1
        if i < len(pngs):
            return f'\n![]({os.path.abspath(pngs[i])})\n\n'
        return ''
    md = re.sub(r'```mermaid\n.*?\n```\n?', repl, md, flags=re.S)
    tmp = f'{OUT}/{name}.md'
    open(tmp, 'w').write(md)
    outp = f'{OUT}/{title}.docx'
    r = subprocess.run(['pandoc', tmp, '-f', 'gfm', '-t', 'docx',
                        '--reference-doc=.build/reference.docx', '-o', outp],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(name, 'PANDOC ERROR:', r.stderr[:300])
    else:
        print(f'{title}.docx', os.path.getsize(outp))
