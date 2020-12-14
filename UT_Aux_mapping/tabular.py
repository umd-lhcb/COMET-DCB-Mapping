#!/usr/bin/env python
#
# Author: Yipeng Sun
# License: BSD 2-clause
# Last Change: Tue Dec 15, 2020 at 12:37 AM +0100

import tabulate as tabl

from functools import partial
from collections import defaultdict

latex_dep = defaultdict(list)
latex_dep['booktabs']
latex_dep['geometry'] = ['a4paper',
                         'left=1cm', 'right=1cm', 'top=1cm', 'bottom=1cm']
latex_dep['amssymb']


# LaTeX general ################################################################

# Don't escape '\'
tabl._table_formats["latex_booktabs_raw"] = tabl.TableFormat(
    lineabove=partial(tabl._latex_line_begin_tabular, booktabs=True),
    linebelowheader=tabl.Line("\\midrule", "", "", ""),
    linebetweenrows=None,
    linebelow=tabl.Line("\\bottomrule\n\\end{tabular}", "", "", ""),
    headerrow=partial(tabl._latex_row, escrules={r"_": r"\_"}),
    datarow=partial(tabl._latex_row, escrules={r"_": r"\_"}),
    padding=1,
    with_header_hide=None,
)


def latex_env(content, env,
              opts=None, tail_opts=None, required_opts=None, eol='\n'):
    dedupl = lambda x: list(set(x))

    if opts:
        opts = dedupl(opts)
        output = '\\' + env + '[' + ','.join(opts) + ']' + \
            '{' + content + '}'
    else:
        output = '\\' + env + '{' + content + '}'

    if tail_opts:
        tail_opts = dedupl(tail_opts)
        output += '[' + ','.join(tail_opts) + ']'

    if required_opts:
        required_opts = dedupl(required_opts)
        output += '{' + ','.join(required_opts) + '}'

    return output + eol


def latex_begin(content, env='document', **kwargs):
    output = latex_env(env, 'begin', **kwargs)
    output += content + '\n'
    output += latex_env(env, 'end')
    return output


def latex_packages(packages=latex_dep):
    output = ''

    for pkg, opts in packages.items():
        output += latex_env(pkg, 'usepackage', opts)

    return output


def latex_preamble(template='article', fontsize='10pt'):
    output = latex_env(template, 'documentclass', [fontsize])
    output += latex_packages()

    return output


# Text styles ##################################################################

def monospace(text):
    return latex_env(text, 'texttt', eol='')


def bold(text):
    return latex_env(text, 'textbf', eol='')


def strikethrough(text):
    latex_dep['ulem'] += ['normalem']
    return latex_env(text, 'sout', eol='')


# Special LaTeX environment ####################################################

def node(content,
         opts=['inner sep=0pt', 'outer sep=0pt'],
         width=r'0.22\textwidth',
         align='none,below left', xshift=r'0.3\textwidth',
         yshift='-10em', anchor='frame.north east'):
    return r'\node[' + ','.join(opts +
                                ['text width='+width, 'align='+align]) + ']' + \
        ' at ' + \
        '([' + ','.join(['xshift='+xshift, 'yshift='+yshift]) + ']' + \
        anchor + ')' + '\n' + \
        '{' + '\n' + content + '\n' + '}' + '\n'


def tcolorbox(left, right,
              left_width=r'0.7\textwidth',
              right_width=r'0.3\textwidth', width=r'\textwidth'):

    latex_dep['tcolorbox'] += ['skins', 'breakable']
    overlay = latex_env(node(right)+';', 'overlay unbroken and first=')[1:]
    return latex_begin(
        left, 'tcolorbox',
        tail_opts=['blanker', 'breakable', 'width='+left_width,
                   'enlarge right by='+right_width, overlay])


# Special output ###############################################################

def tabular_ppp(data, headers, color,
                align=['left']*3+['right']+['center']*3,
                sort=lambda x: int(x[3:])):
    reformatted = defaultdict(list)
    # 'PPP', 'P2B2', 'netname', 'netname (PPP)', 'Depop?', 'Length (appx)'
    counter = defaultdict(lambda: 0)

    for row in data:
        jpu, _ = row[1].split(' - ')
        reformatted_row = [monospace(c) for c in row[0:2]]

        # No need for strikethrough
        # if row[4]:
        #     netname_formatter = lambda x: strikethrough(monospace(x))
        # else:
        netname_formatter = lambda x: monospace(x)

        reformatted_row += [netname_formatter(c) for c in row[2:3]]
        reformatted_row.append(row[5])
        counter[row[5]] += 1
        reformatted_row += [r'$\square$'] * 3

        reformatted[jpu].append(reformatted_row)

    left_output = ''
    for jpu in sorted(reformatted.keys(), key=sort):
        data = reformatted[jpu]

        left_output += latex_env(monospace(jpu), 'subsection*')
        left_output += tabl.tabulate(
            data, headers=headers, tablefmt='latex_booktabs_raw',
            colalign=align
        )
        left_output += '\n'

    counter_data = []
    for length, number in counter.items():
        counter_data.append([length, number/2, number/2])
    right_output = tabl.tabulate(
        counter_data, headers=['Length', 'Black', color],
        tablefmt='latex_booktabs_raw')
    right_output += '\n'

    return left_output, right_output, counter


# Output #######################################################################

def write_to_latex_ppp(output_file, title, data, headers, color,
                       msg='Double check wire lengths before proceed!'):
    content = latex_env('empty', 'pagestyle')
    content += bold(title) + '\n'
    content += latex_env('1em', 'vspace')
    content += r'\noindent'
    content += '\n'

    left_output = right_output = r'\small' + '\n'
    left_table, right_table, _ = tabular_ppp(data,  headers, color)
    left_output += left_table
    right_output += right_table
    right_output += '\n' + r'\vspace{1em}' + msg

    content += tcolorbox(left_output, right_output)

    output = latex_preamble()
    output += latex_begin(content)

    with open(output_file, 'w') as f:
        f.write(output)
