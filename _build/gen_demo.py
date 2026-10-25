"""Demo chat data, rendered by Lumo's own code (bot repo at /workspace/aetherion-dev), for every site language.
Writes demo-data.json next to this file. python3 gen_demo.py"""
import sys,json,os; sys.path.insert(0,'/workspace/aetherion-dev/src')
from lumo import i18n
from lumo.starkeepers import engine
from lumo.discord import slash_sky as S
from lumo.discord import rank_card as rc
C=engine.C()
class M: id=1; display_name='Mira'; name='mira'; guild=None
PICK=['frost_flake','aurora_ribbon','tide_pearl']
E=lambda e:{'title':e.title,'desc':e.description,'foot':e.footer.text if e.footer else '','color':'#%06x'%e.color.value}
LOC='/workspace/aetherion-dev/src/lumo/i18n/locales/'
out={}
for lang in ['en','es','pt-BR','ja']:
    i18n._CURRENT.set(lang); d=json.load(open(LOC+lang+'.json')); t=lambda k,**kw:d[k].format(**kw)
    w=engine.Watch(night='x',phase='waxing_gibbous',stars=PICK,caught=[],next_cost=0,dust=340,level=3,streak={'n':4,'dust':20})
    o={'watch':E(S.watch_embed(M(),w)),'watch_btns':[S.c("sky.btn_catch",name=C.stars[s].name) for s in PICK],'details':S.c("sky.btn_details"),'catch':{},'after':{}}
    for s in PICK:
        o['catch'][s]=E(S.catch_embed(M(),engine.CatchResult(ok=True,star=C.stars[s],new=True,brightness=1,cost=0,dust=340)))
        w2=engine.Watch(night='x',phase='waxing_gibbous',stars=PICK,caught=[s],next_cost=25,dust=340,level=3,streak={'n':4,'dust':20})
        o['after'][s]={'embed':E(S.watch_embed(M(),w2)),'btns':[S.c("sky.btn_caught" if x==s else "sky.btn_catch",name=C.stars[x].name) for x in PICK]}
    o['stars']=PICK
    o['daily']={'title':t('daily.title'),'desc':t('daily.claimed',amount='✦ **2,300**',bonus=t('daily.bonus',bonus='✦ **300**'))+'\n**'+t('daily.streak_line',n=4)+'** '+t('daily.tomorrow')+'\n'+t('daily.wallet',wallet='✦ **12,450**'),'foot':'✦ Lumo · '+t('daily.foot'),'color':'#3d9b64'}
    o['vote']={'title':t('vote.title'),'desc':t('vote.body',coins='1,000',hours=12),'foot':'✦ Lumo · '+t('vote.footer'),'color':'#c9a227','btn':t('vote.button')}
    o['play']={'reply':t('mu.027',title='Outer Space Loop'),'title':t('mu.008'),'desc':'**Outer Space Loop** (1:35)\n'+t('mu.007'),'foot':'✦ Lumo · '+t('mu.011',source=t('mu.010')),'color':'#c9a227'}
    out[lang]=o
    i18n._CURRENT.set(lang); from PIL import Image; import io
    Image.open(io.BytesIO(rc.render_rank(rc.RankData(name='Mira',level=7,into=340,need=900,rank=3,xp=4140)))).save(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','assets','demo',f'rank-card-{lang.lower()}.webp'),quality=88)
json.dump(out,open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'demo-data.json'),'w'),ensure_ascii=False,indent=0)
print('ok')
