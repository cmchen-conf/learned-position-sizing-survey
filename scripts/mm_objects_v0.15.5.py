"""Counts for Table `tab:mm` (money-management decisions against the corpus), v0.15.5.

Source table : ../coding_v0.8.csv, rows whose `final_decision` starts with "include" (95 studies).
Fields used  : `sizing_decision_primary` (one value per study; the primary sized object),
               `sizing_decision`         (semicolon list; primary and secondary objects),
               `taxonomy_branch`         (first letter A, B, C or D).

Row rule (every study falls in exactly one row, by `sizing_decision_primary`):
  position : "share quantity" or "position fraction"
  exposure : "portfolio weight incl. cash/short", "cash ratio" or "leverage"
  budget   : "risk budget"
  exit     : "stop/take-profit level"
  unstated : any value that starts with "other" (unit or form of the size not stated)
Scale-in and scale-out steps have no value in either field, so the script prints no count for them.

Secondary counts (printed, used in the text only):
  exit_secondary     : "stop/take-profit level" in `sizing_decision` and not the primary object
  leverage_secondary : "leverage" in `sizing_decision` and not the primary object (equals \\nLevSec)

Checks: the row totals are compared with the macros already printed in the paper (numbers.tex:
\\nPShare, \\nPFrac, \\nPWeight, \\nPCash, \\nPLev, \\nPBudget, \\nPStop, \\nPOther, \\nLevSec,
\\nBrA..\\nBrD, \\nN); the script stops on any mismatch.

Table rows: the four coded rows; the `unstated` count is printed in the caption.

Usage: python3 mm_objects_v0.15.5.py            (run inside scripts/; writes ../tables/tab_mm.tex
                                                 and mm_objects_v0.15.5.csv, prints the counts)
"""
import csv
import re
import collections

CODING = '../coding_v0.8.csv'
NUMBERS = '../numbers.tex'
OUT_TEX = '../tables/tab_mm.tex'
OUT_CSV = 'mm_objects_v0.15.5.csv'

ROWS = collections.OrderedDict([
    ('position', ('share quantity', 'position fraction')),
    ('exposure', ('portfolio weight incl. cash/short', 'cash ratio', 'leverage')),
    ('budget', ('risk budget',)),
    ('exit', ('stop/take-profit level',)),
    ('unstated', ('other',)),
])


def row_of(primary: str) -> str:
    """Return the table row of a study from its primary sized object."""
    key = 'other' if primary.startswith('other') else primary
    for name, values in ROWS.items():
        if key in values:
            return name
    raise ValueError(f'unmapped primary object: {primary}')


def macro(text: str, name: str) -> int:
    """Read the integer value of \\newcommand{\\<name>}{...} from numbers.tex."""
    return int(re.search(r'\\newcommand\{\\' + name + r'\}\{(\d+)\}', text).group(1))


def main() -> None:
    """Count the studies per row and branch, check them against numbers.tex and write the table."""
    rows = [x for x in csv.DictReader(open(CODING)) if x['final_decision'].strip().lower().startswith('include')]
    cnt = collections.Counter()          # (row, branch) -> studies
    prim = collections.Counter()         # primary object -> studies
    members = collections.defaultdict(list)
    for x in rows:
        p, b = x['sizing_decision_primary'], x['taxonomy_branch'][0]
        r = row_of(p)
        cnt[(r, b)] += 1
        prim['other' if p.startswith('other') else p] += 1
        members[r].append(x['rid'])
    listed = lambda x, v: v in [s.strip() for s in x['sizing_decision'].split(';')]
    exit_sec = sorted(x['rid'] for x in rows if listed(x, 'stop/take-profit level')
                      and x['sizing_decision_primary'] != 'stop/take-profit level')
    lev_sec = sorted(x['rid'] for x in rows if listed(x, 'leverage') and x['sizing_decision_primary'] != 'leverage')
    tot = {r: sum(cnt[(r, b)] for b in 'ABCD') for r in ROWS}
    by_branch = {b: sum(cnt[(r, b)] for r in ROWS) for b in 'ABCD'}

    # ---- checks against numbers already printed in the paper
    t = open(NUMBERS).read()
    assert len(rows) == macro(t, 'nN') == sum(tot.values())
    assert prim['share quantity'] == macro(t, 'nPShare') and prim['position fraction'] == macro(t, 'nPFrac')
    assert prim['portfolio weight incl. cash/short'] == macro(t, 'nPWeight')
    assert prim['cash ratio'] == macro(t, 'nPCash') and prim['leverage'] == macro(t, 'nPLev')
    assert prim['risk budget'] == macro(t, 'nPBudget') == macro(t, 'nScopeTwo')
    assert prim['stop/take-profit level'] == macro(t, 'nPStop') == macro(t, 'nScopeThree')
    assert prim['other'] == macro(t, 'nPOther') and len(lev_sec) == macro(t, 'nLevSec')
    assert tot['position'] + tot['exposure'] + tot['unstated'] == macro(t, 'nScopeOne')
    for b in 'ABCD':
        assert by_branch[b] == macro(t, 'nBr' + b)

    # ---- print and save
    print('studies:', len(rows))
    print('primary object:', dict(prim))
    for r in ROWS:
        print(f'{r:9s} total {tot[r]:2d}  A/B/C/D = ' + '/'.join(str(cnt[(r, b)]) for b in 'ABCD'))
    print('all       total', sum(tot.values()), ' A/B/C/D = ' + '/'.join(str(by_branch[b]) for b in 'ABCD'))
    print('exit level as a secondary object:', len(exit_sec), exit_sec)
    print('leverage as a secondary object  :', len(lev_sec), lev_sec)
    print('all checks against numbers.tex passed')
    with open(OUT_CSV, 'w', newline='') as f:
        w = csv.writer(f)
        w.writerow(['row', 'total', 'A', 'B', 'C', 'D', 'rids'])
        for r in ROWS:
            w.writerow([r, tot[r]] + [cnt[(r, b)] for b in 'ABCD'] + [' '.join(sorted(members[r]))])
        w.writerow(['exit_secondary', len(exit_sec), '', '', '', '', ' '.join(exit_sec)])
        w.writerow(['leverage_secondary', len(lev_sec), '', '', '', '', ' '.join(lev_sec)])

    cell = lambda r: f'{tot[r]} & ' + '/'.join(str(cnt[(r, b)]) for b in 'ABCD')
    tex = r"""\begin{table}[t]
\caption{Money-management decisions, their classical rules and their learned counterparts. $n$: studies by primary
sized object and by branch (A/B/C/D); in """ + str(tot['unstated']) + r""" further studies (""" + '/'.join(str(cnt[('unstated', b)]) for b in 'ABCD') + r""") the unit of the size is not stated. Scale-in steps are not coded.}
\label{tab:mm}
\footnotesize
\setlength{\tabcolsep}{3pt}
\begin{tabular}{@{}>{\raggedright\arraybackslash}p{2.75cm} >{\raggedright\arraybackslash}p{3.75cm} >{\raggedright\arraybackslash}p{4.85cm} r l@{}}
\toprule
Decision & Classical rules & Learned counterpart (branch) & $n$ & A/B/C/D\\
\midrule
Size of one position (quantity, fraction) & fixed amount; fixed fraction; fixed risk $f=\ell/d$; Kelly,
fractional Kelly & forecasts feed the Kelly rule (A); a network outputs the fraction (B); RL action (C) & """ + cell('position') + r"""\\
Total exposure (leverage, cash or short leg) & constant leverage; volatility targeting; drawdown control & a forecast
scales the exposure (A); network (B); RL action (C); language model (D) & """ + cell('exposure') + r"""\\
Risk shares across assets (risk budget) & risk parity; risk budgeting; hierarchical risk parity & forecasts or
clusters feed the rule (A); network (B); language model (D) & """ + cell('budget') + r"""\\
Exit (stop-loss, take-profit level) & fixed stop; trailing stop; profit target & a classifier selects the level
(A); network (B); RL action (C) & """ + cell('exit') + r"""\\
Scale-in, scale-out steps & pyramiding; partial exits & successive RL actions build the holding (C) & -- & --\\
\bottomrule
\end{tabular}
\end{table}
"""
    open(OUT_TEX, 'w').write(tex)
    print('wrote', OUT_TEX, 'and', OUT_CSV)


if __name__ == '__main__':
    main()
