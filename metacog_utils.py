from __future__ import division
from __future__ import unicode_literals

import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import norm


def add_sdt_utils(df, confidence_col='Wager', response_col='Response'):
    """It sdds signal detection theory usful measures."""
    ind = df[confidence_col].map(lambda x: x is not np.nan)
    conf = df.loc[ind, confidence_col].astype(bool)
    df.loc[ind, 'hit'] = df.loc[ind, response_col].astype(bool) & conf
    df.loc[ind, 'fa'] = ~df.loc[ind, response_col].astype(bool) & conf
    df.loc[ind, 'miss'] = df.loc[ind, response_col].astype(bool) & ~conf
    df.loc[ind, 'cr'] = ~df.loc[ind, response_col].astype(bool) & ~conf
    df.loc[ind, 'right'] = df.loc[ind, response_col].astype(bool)
    df.loc[ind, 'wrong'] = ~df.loc[ind, response_col].astype(bool)
    df.loc[ind, 'high'] = conf
    df.loc[ind, 'low'] = ~conf
    return df


def metacog_dfs(df, subjec_col='Name', wage_col='Wager',
                               confidence_col='Confidence',
                               response_col='Response',
                               signal_col='Signal',
                               correct_saturation=False):
    """
    It returns four interesting data frames:  means, counts, proba and mecog.
    """
    means = pd.pivot_table(df, index=[subjec_col],
                           values=[wage_col, confidence_col, response_col,
                                   signal_col],
                           aggfunc=lambda x: np.mean(x[x.notnull()]))
    counts = pd.pivot_table(df, index=[subjec_col],
                            values=['right', 'wrong', 'hit', 'fa', 'miss',
                                    'cr', 'high', 'low'],
                            aggfunc=lambda x: sum(x[x.notnull()]))

    if correct_saturation:
        #d1 = counts['wrong'] / (counts['wrong'] + counts['right'])
        #d2 = counts['right'] / (counts['wrong'] + counts['right'])
        #counts['cr'] += d1
        #counts['fa'] += d1
        #counts['miss'] += d2
        #counts['hit'] += d2
        """
        ind = counts['cr'] == 0
        counts.loc[ind, 'cr'] += 1
        ind = counts['fa'] == 0
        counts.loc[ind, 'fa'] += 1
        ind = counts['miss'] == 0
        counts.loc[ind, 'miss'] += 1
        ind = counts['hit'] == 0
        counts.loc[ind, 'hit'] += 1
        ind = counts['low'] == 0
        counts.loc[ind, 'low'] = 0.5
        ind = counts['high'] == 0
        counts.loc[ind, 'high'] = 0.5
        """
        counts['cr'] += 1
        counts['fa'] += 1
        counts['miss'] += 1
        counts['hit'] += 1
        counts['low'] = 0.5
        counts['high'] = 0.5

    proba = pd.DataFrame(index=means.index)
    proba['hit'] = counts['hit'] / (counts['hit'] + counts['miss'])
    proba['fa'] = counts['fa'] / (counts['fa'] + counts['cr'])

    alpha = 3
    beta = -3
    gamma = 1
    delta = 1
    f = (gamma - beta) / (alpha - delta)
    norm01 = norm(0, 1)
    mecog = pd.DataFrame(index=means.index)
    mecog['c'] = -(norm01.ppf(proba['hit']) + norm01.ppf(proba['fa']))/2
    mecog['dprime'] = norm01.ppf(proba['hit']) - norm01.ppf(proba['fa'])
    mecog['c_opt'] = np.log(f * counts.wrong / counts.right) / (4*mecog.dprime)
    mecog['c-c_opt'] = mecog['c'] - mecog['c_opt']
    mecog['gamma'] = counts.eval('(cr*hit - fa*miss) / (cr*hit + fa*miss)')
    mecog['phi'] = counts.eval('(cr*hit-fa*miss)/(wrong*right*low*high)**0.5')
    return means, counts, proba, mecog


def jointplot_group(df, xname, yname, groupby, xlabel=None, ylabel=None,
                    joint_kws={}, **kwargs):
    """
    df is a dataframe with groups in a hierarchical index. this function is
    an extension of seaborn jointplot function.
    """

    palette = sns.color_palette()
    if type(groupby) is list:
        groups = groupby
    else:
        groups = df.index.get_level_values(df.index.names.index(groupby)).unique()
    markers = ['o', 'D', 's' ,'<', 'v']
    kws_args = {'linewidth': 3}
    g = sns.jointplot(xname, yname, data=df.loc[groups[0]], ratio=2, size=8.4,
                      color=palette[0], label=groups[0], stat_func=None,
                      marginal_kws={'hist': False, 'kde': True, 'kde_kws': kws_args},
                      marker=markers[0], joint_kws=joint_kws, **kwargs)
    for group, c, m in zip(groups[1:], palette[1:], markers[1:]):
        sns.kdeplot(df.loc[group, xname], ax=g.ax_marg_x, legend=False,
                    color=c, **kws_args)
        sns.kdeplot(df.loc[group, yname], ax=g.ax_marg_y, vertical=True,
                    legend=False, color=c, **kws_args)
        g.ax_joint.plot(df.loc[group, xname], df.loc[group, yname], "o", ms=5,
                        color=c, label=group, marker=m)
    g.set_axis_labels(xlabel, ylabel, fontsize=14)
    g.ax_joint.legend(prop={'size': 14})
    return g


def jackknife(data, fun):

    """
    jackknife method for estimating a statistic and its variance.
    """

    estimations = []
    for i in data.index.unique():
        sample = data.loc[data.index != i]
        estimations.append(fun(sample))
    return estimations


def stat_diff(df, independent, dependents, contrast, tests):
    """It Uses different tests to test df differences.

    It tests if there is significant differences between dependent variables
    for different groups in dependents contrasted with contrast.
    """
    df_contrast = df[df[independent] == contrast]
    gruped = df[df[independent] != contrast].groupby(independent)
    tests_names = [x.__name__ for x in tests]
    index = pd.MultiIndex.from_product([gruped.groups, tests_names,
                                       ['t-val', 'p-val']],
                                       names=['Group', 'Test', 'Value'])
    statdiff = pd.DataFrame(index=index, columns=dependents)
    for cond, group in gruped:
        for test in tests:
            for m in dependents:
                out = test(group[m], df_contrast[m])
                statdiff.loc[(cond, test.__name__), m] = out
    return statdiff
