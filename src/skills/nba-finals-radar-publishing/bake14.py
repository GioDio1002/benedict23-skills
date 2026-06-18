import re, os, math
REPO='/Users/benedict/Documents/benedict23-skills/benedict23-skills-repo/docs'

PAGES=[]
for sub,lang in [('zh/articles','zh'),('articles','en')]:
    for team in ('knicks','spurs'):
        for n in (1,2,3):
            PAGES.append((f'{REPO}/{sub}/2026-nba-finals-{team}-radars/page-{n}.html', lang))

CN =['真实命中率','使用率','助攻率','队内得分占比','篮板率','护球率','正负值','防守压制','犯规节制','PIE','封盖率','抢断率','迫使失误率','对位压制']
SUB=['TS%','USG%','AST%','Team Score Share','REB%','Security','+/-','Stops','Discipline','PIE','BLK%','STL%','Forced TOV%','Matchup']
EN =SUB
N=14
CX=CY=250.0; R=150.0

def num(s):
    s=s.strip().replace('%','').replace('+','')
    try: return float(s)
    except: return 0.0

ROW=re.compile(r'<td class="metric-cell">[^<]+</td><td class="value-cell">([^<]+)</td><td class="value-cell">([^<]+)</td><td class="value-cell">([^<]+)</td>')

def parse(sec):
    rows=ROW.findall(sec)[:N]
    if len(rows)<N: return None
    fin=[num(r[0]) for r in rows]; pl=[num(r[1]) for r in rows]; tm=[num(r[2]) for r in rows]
    return fin,pl,tm

# pass 1: global min/max per axis across all players x 3 baselines (numbers lang-independent)
mn=[1e9]*N; mx=[-1e9]*N
seen=set()
for fp,lang in PAGES:
    if lang!='en' or not os.path.exists(fp): continue
    h=open(fp).read()
    for sec in re.findall(r'<section class="player-section">.*?</section>', h, re.S):
        pr=parse(sec)
        if not pr: continue
        for arr in pr:
            for i,v in enumerate(arr):
                mn[i]=min(mn[i],v); mx[i]=max(mx[i],v)

def pt(i,r):
    a=-math.pi/2+i*2*math.pi/N
    return CX+math.cos(a)*r, CY+math.sin(a)*r

def norm(v,i):
    d=mx[i]-mn[i]
    return 0.0 if d==0 else max(0.0,min(1.0,(v-mn[i])/d))

def poly(arr,color,width,dash,fill):
    d=''
    for i in range(N):
        x,y=pt(i,norm(arr[i],i)*R)
        d+=('L' if i else 'M')+f'{x:.1f} {y:.1f} '
    dd=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}Z" fill="{fill}" stroke="{color}" stroke-width="{width}" stroke-linejoin="round"{dd}/>'

def dots(arr,color):
    s=''
    for i in range(N):
        x,y=pt(i,norm(arr[i],i)*R)
        s+=f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{color}" stroke="white" stroke-width="2"/>'
    return s

def grid():
    g='<g opacity="0.5">'
    for k in range(1,6):
        rr=R*k/5; ring=''
        for i in range(N):
            x,y=pt(i,rr); ring+=('L' if i else 'M')+f'{x:.1f} {y:.1f} '
        g+=f'<path d="{ring}Z" fill="none" stroke="#E2D9CC" stroke-width="1"/>'
    for i in range(N):
        x,y=pt(i,R); g+=f'<line x1="{CX}" y1="{CY}" x2="{x:.1f}" y2="{y:.1f}" stroke="#E2D9CC" stroke-width="1"/>'
    g+='</g>'
    return g

def labels(lang):
    s=''
    for i in range(N):
        lx,ly=pt(i,R+30)
        an='middle'
        if lx>CX+8: an='start'
        elif lx<CX-8: an='end'
        if lang=='zh':
            s+=f'<text x="{lx:.1f}" y="{ly-6:.1f}" text-anchor="{an}" font-size="12" font-weight="600" fill="#333">{CN[i]}</text>'
            s+=f'<text x="{lx:.1f}" y="{ly+8:.1f}" text-anchor="{an}" font-size="10" fill="#888">{SUB[i]}</text>'
        else:
            s+=f'<text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{an}" font-size="11" font-weight="600" fill="#555">{EN[i]}</text>'
    return s

def svg(fin,pl,tm,lang):
    body=grid()
    body+=poly(pl,'#6C757D',1.5,'4,4','rgba(108,117,125,0.06)')
    body+=poly(tm,'#2563EB',2,'6,4','rgba(37,99,235,0.06)')
    body+=poly(fin,'#111827',3.5,'','rgba(17,24,39,0.10)')
    body+=dots(fin,'#111827')
    body+=labels(lang)
    return f'<svg viewBox="0 0 500 540" width="500" height="540">{body}</svg>'

cnt=0
for fp,lang in PAGES:
    if not os.path.exists(fp): continue
    h=open(fp).read()
    def per(m):
        global cnt
        sec=m.group(0); pr=parse(sec)
        if not pr: return sec
        new=svg(*pr,lang)
        sec2=re.sub(r'<svg viewBox.*?</svg>', new, sec, count=1, flags=re.S)
        cnt+=1; return sec2
    h=re.sub(r'<section class="player-section">.*?</section>', per, h, flags=re.S)
    with open(fp,'w') as f: f.write(h)
print('mn',[round(x,1) for x in mn]); print('mx',[round(x,1) for x in mx])
print('rebaked sections:',cnt)
