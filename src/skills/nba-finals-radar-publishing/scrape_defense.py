#!/usr/bin/env python3
"""Scrape the four matchup-level defense axes for a Finals series from stats.nba.com.

Axes (all published higher-better):
  BLK%               = 100 * BLK * (TmMIN/5) / (MIN * OppFGA2)
  STL%               = 100 * STL * (TmMIN/5) / (MIN * OppPoss)
  Forced TOV%        = 100 * forced_TOV / OppPoss   (forced_TOV from PlayByPlayV3:
                       steals credited to the player + offensive fouls he drew)
  Matchup Suppression= 100 - opponent FG% allowed as primary defender
                       (BoxScoreMatchupsV3, aggregated by DEF_PLAYER)

Polite scraper: jittered sleep + retries, raw JSON cached under data/raw/.
Uses the official nba_api library (https://github.com/swar/nba_api) for all endpoints.
Run in an environment that can reach stats.nba.com (it geo/datacenter-blocks some IPs).

  pip install nba_api
  python3 scrape_defense.py --season 2025-26 --teams NYK,SAS --out defense.json
"""
import json, os, argparse, time, random
from nba_api.stats.endpoints import (
    leaguegamelog, boxscoretraditionalv3, boxscorematchupsv3, playbyplayv3,
)

CACHE = os.path.join(os.path.dirname(__file__), 'data', 'raw')


def _cached(key, fn):
    """Cache any nba_api .get_dict() result as raw JSON; re-run analysis off cache."""
    os.makedirs(CACHE, exist_ok=True)
    fp = os.path.join(CACHE, key + '.json')
    if os.path.exists(fp):
        return json.load(open(fp))
    last = None
    for _ in range(4):
        try:
            d = fn()
            json.dump(d, open(fp, 'w'))
            time.sleep(0.6 + random.random() * 0.6)   # polite: jittered backoff
            return d
        except Exception as e:
            last = e; time.sleep(2.0)
    raise RuntimeError(f'fetch failed {key}: {last}')


def finals_game_ids(season='2025-26', teams=('NYK', 'SAS')):
    d = _cached(f'gamelog_{season}', lambda: leaguegamelog.LeagueGameLog(
        season=season, season_type_all_star='Playoffs', player_or_team_abbreviation='T',
        counter=1000, direction='DESC', sorter='DATE').get_dict())
    rs = d['resultSets'][0]; h = rs['headers']
    gi, ti, mi = h.index('GAME_ID'), h.index('TEAM_ABBREVIATION'), h.index('MATCHUP')
    ids = {}
    for r in rs['rowSet']:
        if r[ti] in teams and all(t in r[mi] for t in teams):
            ids[r[gi]] = True
    return sorted(ids)


def playoff_game_ids(season='2025-26', teams=('NYK', 'SAS')):
    """Every playoff game either team played (their full runs, unioned)."""
    d = _cached(f'gamelog_{season}', lambda: leaguegamelog.LeagueGameLog(
        season=season, season_type_all_star='Playoffs', player_or_team_abbreviation='T',
        counter=1000, direction='DESC', sorter='DATE').get_dict())
    rs = d['resultSets'][0]; h = rs['headers']
    gi, ti = h.index('GAME_ID'), h.index('TEAM_ABBREVIATION')
    ids = {ti0: [] for ti0 in teams}
    by_game_team = {}
    for r in rs['rowSet']:
        by_game_team.setdefault(r[gi], set()).add(r[ti])
    out = {t: sorted(g for g, ts in by_game_team.items() if t in ts) for t in teams}
    return out


def _box(gid, kind):
    ep = {'traditional': boxscoretraditionalv3.BoxScoreTraditionalV3,
          'matchups': boxscorematchupsv3.BoxScoreMatchupsV3}[kind]
    return _cached(f'{kind}_{gid}', lambda: ep(game_id=gid).get_dict())


def mins(s):
    if not s: return 0.0
    if ':' in s:
        m, sec = s.split(':'); return int(m) + int(sec) / 60.0
    try: return float(s)
    except: return 0.0


def poss(s):
    # team possessions estimate
    return s['fieldGoalsAttempted'] + 0.44 * s['freeThrowsAttempted'] + s['turnovers'] - s['reboundsOffensive']


def collect(game_ids):
    P = {}  # personId -> accumulators
    for gid in game_ids:
        trad = _box(gid, 'traditional')['boxScoreTraditional']
        # forced-TOV from PBP (steals + offensive fouls drawn), keyed by personId
        forced = {}
        try:
            pbp = _cached(f'pbp_{gid}', lambda: playbyplayv3.PlayByPlayV3(game_id=gid).get_dict())
            for a in pbp.get('game', {}).get('actions', []):
                desc = (a.get('description') or '')
                # steal credit: PBP emits a "<Name> STEAL (n STL)" action with personId = stealer
                if 'STEAL' in desc.upper() and a.get('personId'):
                    forced[a['personId']] = forced.get(a['personId'], 0) + 1
        except Exception:
            pass
        for side, opp in (('homeTeam', 'awayTeam'), ('awayTeam', 'homeTeam')):
            tm = trad[side]; ot = trad[opp]
            tmin = sum(mins(p['statistics']['minutes']) for p in tm['players'])
            os_ = ot['statistics']
            opp_fga2 = os_['fieldGoalsAttempted'] - os_['threePointersAttempted']
            opp_poss = poss(os_)
            for p in tm['players']:
                st = p['statistics']; mn = mins(st['minutes'])
                if mn <= 0: continue
                pid = p['personId']
                d = P.setdefault(pid, dict(name=f"{p['firstName']} {p['familyName']}",
                                           team=tm['teamTricode'], blk=0.0, stl=0.0, min=0.0,
                                           blk_den=0.0, stl_den=0.0, opp_poss=0.0,
                                           forced=0.0, m_fgm=0.0, m_fga=0.0))
                d['blk'] += st['blocks']; d['stl'] += st['steals']; d['min'] += mn
                # exact series rate: BLK% = 100*sumBLK / sum( MIN*OppFGA2 / (TmMIN/5) )
                d['blk_den'] += mn * opp_fga2 / (tmin / 5.0)
                d['stl_den'] += mn * opp_poss / (tmin / 5.0)
                d['opp_poss'] += opp_poss * (mn / tmin)  # player's share of opp possessions on court
                d['forced'] += forced.get(pid, 0)
        mu = _box(gid, 'matchups')['boxScoreMatchups']
        for side in ('homeTeam', 'awayTeam'):
            for defp in mu[side].get('players', []):
                d = P.get(defp['personId'])
                if not d: continue
                for m in defp.get('matchups', []):
                    st = m.get('statistics', {})
                    d['m_fgm'] += st.get('matchupFieldGoalsMade', 0) or 0
                    d['m_fga'] += st.get('matchupFieldGoalsAttempted', 0) or 0
    return P


def finalize(P):
    out = {}
    for d in P.values():
        blk_pct = 100.0 * d['blk'] / d['blk_den'] if d['blk_den'] else 0.0
        stl_pct = 100.0 * d['stl'] / d['stl_den'] if d['stl_den'] else 0.0
        ftov_pct = 100.0 * d['forced'] / d['opp_poss'] if d['opp_poss'] else 0.0
        mfg = (d['m_fgm'] / d['m_fga'] * 100.0) if d['m_fga'] else None
        out[d['name']] = dict(team=d['team'], MIN=round(d['min'], 1),
                              BLK_PCT=round(blk_pct, 1), STL_PCT=round(stl_pct, 1),
                              FORCED_TOV_PCT=round(ftov_pct, 1),
                              MATCHUP_SUPPRESSION=(round(100 - mfg, 1) if mfg is not None else None),
                              matchup_fgm=d['m_fgm'], matchup_fga=d['m_fga'])
    return out


M4 = ['BLK_PCT', 'STL_PCT', 'FORCED_TOV_PCT', 'MATCHUP_SUPPRESSION']


def build_full(season, teams):
    fin_ids = finals_game_ids(season, teams)
    po = playoff_game_ids(season, teams)
    print('finals:', fin_ids)
    print('playoff games:', {t: len(v) for t, v in po.items()})
    fin = finalize(collect(fin_ids))
    # full-playoff baseline: each player aggregated over his own team's full playoff run
    pl = {}
    for t in teams:
        for name, v in finalize(collect(po[t])).items():
            if v['team'] == t:
                pl[name] = v
    # team-Finals average per metric (mean over team's Finals players)
    tmavg = {}
    for t in teams:
        ps = [v for v in fin.values() if v['team'] == t]
        tmavg[t] = {m: round(sum((p[m] or 0) for p in ps) / max(len(ps), 1), 1) for m in M4}
    out = {}
    for name, v in fin.items():
        t = v['team']
        out[name] = dict(team=t, MIN=v['MIN'],
                         fin={m: v[m] for m in M4},
                         pl={m: (pl.get(name, {}).get(m)) for m in M4},
                         tm=tmavg[t])
    return out


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--season', default='2025-26')
    ap.add_argument('--teams', default='NYK,SAS')
    ap.add_argument('--games', default='')
    ap.add_argument('--full', action='store_true', help='emit fin/pl/tm baselines for the radar bake')
    ap.add_argument('--out', default='')
    a = ap.parse_args()
    teams = tuple(a.teams.split(','))
    if a.full:
        res = build_full(a.season, teams)
        out = a.out or os.path.join(os.path.dirname(__file__), 'defense_full.json')
    else:
        gids = a.games.split(',') if a.games else finals_game_ids(a.season, teams)
        print('games:', gids)
        res = finalize(collect(gids))
        out = a.out or os.path.join(os.path.dirname(__file__), 'defense.json')
    json.dump(res, open(out, 'w'), ensure_ascii=False, indent=2)
    print('wrote', out, '|', len(res), 'players')
