"""Epodarien – F2P-Simulation mit Ausrüstung v1.7.3.
python3 sim_f2p.py [seed] [tage]   (Standard: Seed 1, 21 Tage)
ANNAHMEN (explizit):
- Sessions: 4/Tag um 08:00, 12:30, 18:00, 22:00 à ~5 min; Install Tag 1 um 18:00 (Tag 1 = 2 Sessions).
- Gieriger, aber planender Spieler: Häuptlingsfeuer > Lager (falls Engpass) > Hütte > Produktion > Rest; spart aufs Feuer, wenn es die
  Kampagne blockiert. Truppen nur bis 1,3x Empfehlung (Keule/Schleuder-Mix). Missionen nur bei Kampfkraft >= Empfehlung und genug Proviant.
- Kampf: Verluste 35 % (knapp) / 15 % (>=1,3x = 3 Sterne). Kampfkraft = Truppen x (1 + Ø Führung %) x 1,05 Epochenbonus + Σ Heldenkraft
  (power_l1 x Levelfaktor), max. 6 Helden.
- Helden: Bako Start, Gorm/Mira/Tala per Kampagne, Ruka per Tutorial-Beschwörung (nach Tutorial-Quest q19). Heldenlevel ab e1_camp_11
  (feature_hero_level_gold): Gold + Heldenerfahrung laut hero_levels.csv, Cap 20; Gold-Reserve = Goldkosten des nächsten Feuers.
- Trainingsmanöver (game_config): wenn Nahrung > 70 % Lager und Gold über Reserve: Nahrung+Gold -> Heldenerfahrung.
- Produktion offline bis Lagerlimit, max. offline_max_hours; Starthilfe; Winter 3 h/1 h (−30 % Nahrung); Unterhalt laut units.csv.
- Kristalle/Tickets: f2p_income + Kampagnenbelohnungen; Ausgabe: Anfänger-Banner (100) dann Standard (150) bzw. Tickets.
"""
import csv,random,sys,os
D=os.path.dirname(os.path.abspath(__file__))
GDD=os.path.join(D,'data')  # versionierter GDD-Snapshot; lauffähig aus jedem Arbeitsverzeichnis
GEAR_DIR=os.path.abspath(os.path.join(D,'..'))
GEAR_FILES={'equipment.csv','artifacts.csv','gear_slots.csv','gear_rarities.csv','gear_sets.csv','gear_upgrade_costs.csv','stat_definitions.csv','game_config_ausruestung.csv'}
def R(n):
    root=GEAR_DIR if n in GEAR_FILES else GDD
    return list(csv.DictReader(open(os.path.join(root,n),encoding='utf-8')))
B={b['building_id']:b for b in R('buildings.csv')}
LV={(x['building_id'],int(x['level'])):x for x in R('building_levels.csv')}
U={u['unit_id']:u for u in R('units.csv')}
C=R('campaign_levels.csv');INC={i['income_id']:i for i in R('f2p_income.csv')}
RATES={(r['banner_id'],r['rarity']):r for r in R('summon_rates.csv')}
RS={r['resource_id']:r for r in R('resources.csv')};CFG={r['key']:r['value'] for r in R('game_config.csv')}
HEROES={h['hero_id']:h for h in R('heroes.csv')};HLV={int(x['hero_level']):x for x in R('hero_levels.csv')}
QUESTS=R('tutorial_quests.csv')
KEYS={'res_food':'food','res_wood':'wood','res_stone':'stone','res_gold':'gold','res_knowledge':'knowledge'}
CIDX=lambda cid:int(cid[-2:])
INSTALL=18.0;SAVE=True
SESSION_MISSION_MIN=4.0;FIRST_SESSION_MIN=16.0  # v0.7: Minuten für Missionen je 5-min-Session; Install-Session = erste Stunde (sim_first60)
MIN_PER_CH={1:1.5,2:2.0,3:2.5}  # game_config mission_minutes_ch* (Wellen/Kampfdauer je Kapitel)
SIM_CAL=0.92  # v0.7: echte Schwelle = 0,92 x Empfehlung (Dev-Kampfsim L30: 0,84 mit alter Mira; Mira-Nerf → 0,92 [Annahme, Dev prüft])
GEAR_FIRST='--gear-first' in sys.argv  # v0.9 Worst Case: Spieler ignoriert forge_reserve_warning und rüstet vor allem anderen auf
GEAR=True  # v0.8: Ausrüstung (Schmiede-Tab ab feature_forge L14)
EQ_UP={}
for x in R('gear_upgrade_costs.csv'):
    if x['from_level'].isdigit():
        EQ_UP[(x['gear_rarity_id'],int(x['from_level']))]=(float(x['cost_gold']),float(x['cost_stone']),float(x['cost_wood']))
    elif x['gear_rarity_id'] in ('refine_common_to_fine','refine_fine_to_master'):
        EQ_UP[x['gear_rarity_id']]=(float(x['cost_gold']),float(x['cost_stone']),float(x['cost_wood']))
GRAR={x['gear_rarity_id']:x for x in R('gear_rarities.csv')};GSLOT={x['slot_id']:x for x in R('gear_slots.csv')}
STAT_SHORT={'stat_atk_pct':'atk','stat_hp_pct':'hp','stat_def_pct':'def'}
SLOTSTAT={x['slot_id']:STAT_SHORT[x['stat_main']] for x in GSLOT.values() if x['slot_group']!='artifact'}
EQ_ITEMS={(x['class_affinity'],x['slot_id'],x['gear_rarity_id']):x for x in R('equipment.csv')}
ARTIFACTS={x['artifact_id']:x for x in R('artifacts.csv')}
GEAR_SETS={x['set_id']:x for x in R('gear_sets.csv')}
ART_SLOTS={x['slot_id'] for x in GSLOT.values() if x['slot_group']=='artifact'}
GEAR_UNLOCK_CFG={x['key']:x['value'] for x in R('game_config_ausruestung.csv')}
GEAR_LEVEL_STEP=float(GEAR_UNLOCK_CFG['gear_stat_per_level_pct'])/100
MINIGAME=None  # v0.7: None = aus; sonst Liste (resource_id, Produktionsstunden/Tag) + hero_xp/Tag aus minigame_rewards.csv
GUILD=None  # v0.6: None = ohne Gilde; sonst dict(join_level=int, xp_per_day=int) -> guild_levels.csv
GL=R('guild_levels.csv')
# v1.2 Forschung (research_nodes/research_costs, 1 Slot)
RESEARCH=True;RESEARCH_FIRST=False;RESEARCH_UNLOCK_FIRE=int(CFG.get('research_unlock_fire',3));R_RES_ALL=False;RESEARCH_GATE=True;USE_GLUT=True
RN={x['node_id']:x for x in R('research_nodes.csv')};RCOST={(x['node_id'],int(x['level'])):x for x in R('research_costs.csv')}
# v1.6.13 Nr. 286: E2-Baum aus research_nodes_e2.csv/research_costs_e2.csv (Forschung E2 v1, Kap. 5) statt Platzhalter rs_e2; Kosten inkl. Wissen
RN2={x['node_id']:x for x in R('research_nodes_e2.csv')};RCOST2={(x['node_id'],int(x['level'])):x for x in R('research_costs_e2.csv')}
E2_GOLD_PRIORITY=False  # Nr. 290 Fabian: Standard aus – E2-Forschung offiziell goldgebunden (Baum Tag 19,5); True = Gold-Vorrang E2 vor Helden (Tag 16,5)
E2_SINKS=True  # Nr. 292: Stammesfest, Palisade/Vorratshöhle L11–15 (game_config, Aufbau-Delta)
TRADE_MODE=CFG.get('trade_mode','daily_fixed')  # Nr. 292: daily_fixed (~trade_daily_res/Tag) | overflow (bis trade_overflow_daily_cap_res)
if '--trade-overflow' in sys.argv: TRADE_MODE='overflow'
E2_BONUS='--no-e2-bonus' not in sys.argv  # Nr. 294 Q4: E2-Effekte in rb() (Truppen gedeckelt research_power_cap_pct_e2)
PAID_CLOCK_MIN=0  # v1.3: gekaufte Uhren-Minuten/Tag (Max-Zahler: 3 IAP-Pakete 390 + Kristall-Shop 2×60 = 510)
# v1.6.10: E2-Mindestwirtschaft + Uhren-Regeln aus game_config (quellen/balancing/epoch2_economy.csv). E2=False/CLOCK_RULES=False = Stand v1.6.9
E2=True;CLOCK_RULES=True;CLOCK_EXTRA=True;TRADE=('--no-trade' not in sys.argv)
IDEAS='--ideas' in sys.argv  # Nr. 312: Ideen-Module (Status Idee, Standard aus) testweise an
FEAST_LIMIT_ARG=next((int(a.split('=')[1]) for a in sys.argv if a.startswith('--feasts=')),None)  # Nr. 299: Override Feste/Tag (z. B. --feasts=4)
CMIN=lambda cid:int(''.join(ch for ch in cid.split('_')[-1] if ch.isdigit()))  # itm_clock_15m → 15
def _inc_min(i): return int(INC[i]['amount'])*CMIN(INC[i]['currency_id'])
def clock_income(day,new_levels=0,tree_open=True):  # v1.6.10: Quellen aus f2p_income inc_clock_* (vorher Literale)
    daily=_inc_min('inc_clock_daily')
    if CLOCK_RULES and not tree_open and CFG.get('clock_daily_reward_if_tree_done')=='alt_reward':
        daily=0;s.xp+=float(CFG['clock_daily_alt_reward'].split(':')[1]);s.alt_days+=1
    m=daily+_inc_min('inc_clock_center')*new_levels+(_inc_min('inc_clock_weekly') if day%7==0 else 0)+(_inc_min('inc_clock_login7') if day==7 else 0)+(_inc_min('inc_clock_tutorial') if day==1 else 0)
    if CLOCK_EXTRA and s.epoch_day and day>s.epoch_day and (tree_open or not CLOCK_RULES):
        x=int(CFG.get('clock_free_extra_min_day',0))
        if day<=28: x=max(0,min(x,int(CFG.get('clock_nonquest_first_window_min',10**9))-s.extra_clock))  # Nr. 291: erstes 28-T-Fenster gedeckelt (Erfolgs-Uhren im K-GD12-Budget)
        s.extra_clock+=x;m+=x  # K-GD12 (Gilde/Arena/Festmünzen/Würfel), Shop-Uhren nur bei offenem Knoten
    s.clock_in+=m
    return m+PAID_CLOCK_MIN
CRIT={('rs_e1_beeren',1),('rs_e1_steinaxt',1),('rs_e1_hebel',1),('rs_e1_muscheln',1),('rs_e1_muscheln',2),('rs_e1_muscheln',3),('rs_e1_felsritzung',1),('rs_e1_felsritzung',2),('rs_e1_felsritzung',3),('rs_e1_tauschkunde',1),('rs_e1_kampfrufe',1),('rs_e1_fellpanzer',1),('rs_e1_feldkueche',1),('rs_e1_feldkueche',2),('rs_e1_trockenfleisch',1),('rs_e1_sternkunde',1)}  # v1.2: kritischer Pfad Sternkunde (UI markiert ihn)
STERN_PATH={'rs_e1_sternkunde','rs_e1_felsritzung','rs_e1_tauschkunde','rs_e1_trockenfleisch','rs_e1_feldkueche','rs_e1_fellpanzer','rs_e1_kampfrufe','rs_e1_muscheln','rs_e1_hebel','rs_e1_steinaxt','rs_e1_beeren','rs_e1_jagdformation'}
class S:pass
s=S()
def reset():
    s.res={k:float(RS[k]['start_amount']) for k in KEYS};s.xp=0.0
    s.lvl={b:int(B[b]['start_level']) for b in B if int(B[b]['start_level'])}
    s.army={};s.camp=0;s.heroes={h:1 for h in HEROES if HEROES[h]['start_owned']=='1'}
    s.gems=0;s.tickets=0;s.starter=0;s.pity=0;s.srpity=0;s.spity=0;s.summons=0;s.ssr=0;s.qi=0
    s.guild_xp=None;s.gear={};s.artifacts={};s.gear_spent=[0,0,0];s.mg_res=0;s.losses=[];s.guild_coin=0;s.donated=0
    s.rlv={};s.rcur=None;s.runtil=0;s.rbank=0;s.rspent=[0,0,0,0];s.rdone_t={};s.storage_hits=0;s.gold_heroes=0;s.maneuvers=0;s.food_supply=0;s.epoch_day=None
    s.hitr={};s.ritual_day={};s.rituals=0;s.ahnen=0;s.ahnen_spent=[0,0,0,0];s.e2=False;s.ext={};s.ext_spent=[0,0];s.feast_until=0;s.feasts=0;s.feast_spent=[0,0,0,0];s.feast_day={};s.extra_clock=0;s.e2_spent=[0,0,0,0];s.e2_idle=0;s.e2_short_n={};s.ascend_stock=None;s.ascend_start=None;s.overflow={};s.alt_days=0;s.clock_in=0;s.traded=[0,0];s.bank_log={};s.gold_low_h=0;s.e2_done=None;s.e1_done=None;s.ovr={};s.stone_d8=None;s.idea_gold=0
reset()
random.seed(int(sys.argv[1]) if len(sys.argv)>1 and sys.argv[1].isdigit() else 1)
eff=lambda b:float(LV[(b,s.lvl[b])]['effect_value']) if s.lvl.get(b,0)>0 else 0
def rb(k): return (sum(float(RN[n]['effect_per_level'])*l for n,l in s.rlv.items() if n in RN and RN[n]['effect_key']==k)+(sum(float(RN2[n]['effect_per_level'])*l for n,l in s.rlv.items() if n in RN2 and RN2[n]['effect_key']==k) if E2_BONUS else 0)) if RESEARCH else 0
def cap(r): return (eff('bld_storage')*float(RS[r]['storage_cap_factor']) if s.lvl.get('bld_storage') else float(RS[r]['base_storage_cap']))*(1+rb('storage_pct')/100)*(float(CFG['e2_storage_cap_mult']) if s.e2 else 1)*(1+float(CFG.get('e2_storage_ext_effect_pct_per_level',0))/100*s.ext.get('bld_storage',0))
def pop_cap(): return float(CFG['base_population'])+eff('bld_hut')
def workers(): return sum(int(LV[(b,s.lvl[b])]['workers_total']) for b in s.lvl if s.lvl[b])
def army_pop(): return sum(n*int(U[u]['pop_cost']) for u,n in s.army.items())
def army_cap(): return eff('bld_barracks') if s.lvl.get('bld_barracks') else float(CFG['army_cap_without_barracks'])
def rbt(k): return min(rb(k),float(CFG.get('research_power_cap_pct_e2' if s.e2 else 'research_power_cap_pct',99)))
def upow(u):u=U[u];return float(u['hp'])/10*(1+rbt('troop_hp_pct')/100)+2*float(u['atk'])*(1+rbt('troop_atk_pct')/100)+float(u['def'])*(1+rbt('troop_def_pct')/100)
def feature(f): return any(f in c['features'].split(';') for c in C[:s.camp])
def unlocked(t): return any(t in c['unlocks'].split(';') for c in C[:s.camp])
def hero_power():
    top=sorted(s.heroes.items(),key=lambda kv:-float(HEROES[kv[0]]['power_l1'])*(1+0.08*(kv[1]-1)))[:6]
    hp=sum(float(HEROES[h]['power_l1'])*(1+0.08*(l-1)) for h,l in top)
    lead=sum(float(HEROES[h]['lead_bonus_pct'])+0.2*(l-1) for h,l in top)/max(1,len(top))
    return hp,lead
def gear_pct(h,st):
    cls=HEROES[h].get('leads_unit_class','')
    values={'atk':0.0,'hp':0.0,'def':0.0};set_counts={}
    for (hh,sl),(rarity,level) in s.gear.items():
        if hh!=h: continue
        item=EQ_ITEMS.get((cls,sl,rarity))
        if not item: continue
        stat=STAT_SHORT.get(item['main_stat_id'])
        if stat: values[stat]+=float(item['main_stat_base_pct'])*float(GRAR[rarity]['stat_mult_pct'])/100*(1+GEAR_LEVEL_STEP*(level-1))
        if item['set_id']: set_counts[item['set_id']]=set_counts.get(item['set_id'],0)+1
    for set_id,count in set_counts.items():
        row=GEAR_SETS[set_id]
        for pieces in (2,4,6):
            if count<pieces: continue
            for suffix in ('','_2'):
                stat=STAT_SHORT.get(row.get(f'bonus_{pieces}_stat{suffix}',''))
                if stat: values[stat]+=float(row[f'bonus_{pieces}_value{suffix}'])
    epoch='epoch_2' if s.e2 else 'epoch_1'
    for (hh,_slot),artifact_id in s.artifacts.items():
        if hh!=h: continue
        art=ARTIFACTS[artifact_id];stat=STAT_SHORT.get(art['effect_stat_id'])
        if not stat: continue
        role_match=art['signature_type']=='role' and art['signature_value']==HEROES[h].get('hero_class','')
        epoch_match=art['signature_type']=='epoch' and art['signature_value']==epoch
        signature=1+float(art['signature_bonus_rel_pct'])/100 if role_match or epoch_match else 1
        values[stat]+=float(art['effect_value_l1'])*signature
    return values[st]
def gear_factor():  # Kampfkraft-Wirkung: ATK zählt doppelt (upow = HP/10 + 2 ATK + DEF)
    hs=list(s.heroes)[:6]
    if not hs: return 1
    return 1+sum(0.5*gear_pct(h,'atk')+0.25*gear_pct(h,'hp')+0.25*gear_pct(h,'def') for h in hs)/len(hs)/100
def power():
    hp,lead=hero_power()
    return sum(n*upow(u) for u,n in s.army.items())*(1+lead/100)*(1+float(CFG['epoch_bonus_pct'])/100)+hp*gear_factor()  # v0.9: Ausrüstung nur auf Helden
def bld_ok(b): x=B[b];return int(x['unlock_center_level'])<=s.lvl['bld_center'] and (x['unlock_campaign_level']=='' or s.camp>=CIDX(x['unlock_campaign_level']))
def winter_h(a,b):
    n=int((b-a)*60);return sum(1 for i in range(n) if ((a+i/60)%4)>=3)/60
def qdone(q):
    t,tg,v=q['condition_type'],q['condition_target'],int(q['condition_value'])
    if t=='building_level': return s.lvl.get(tg,0)>=v
    if t=='campaign_cleared': return s.camp>=CIDX(tg)
    if t=='army_pop': return army_pop()>=v
def quests():
    while s.qi<len(QUESTS) and qdone(QUESTS[s.qi]):
        q=QUESTS[s.qi]
        for r,k in KEYS.items():
            if 'reward_'+k in q: s.res[r]=min(cap(r),s.res[r]+float(q['reward_'+k] or 0))
        s.gems+=int(q.get('reward_gems') or 0);s.qi+=1
        if QUESTS[s.qi-1]['quest_id']==CFG.get('ruka_tutorial_after_quest','q19') and 'hero_ruka' not in s.heroes: s.heroes['hero_ruka']=1;s.ssr+=1  # Tutorial-Beschwörung (banner_tutorial)
def produce(h,t0):
    if h<=0: return
    h=min(h,float(CFG['offline_max_hours']))
    boost=float(CFG['early_production_mult']) if t0-INSTALL<float(CFG['early_production_hours']) else 1
    taper=float(CFG.get('early_production_taper_mult',1)) if float(CFG['early_production_hours'])<=t0-INSTALL<float(CFG['early_production_hours'])+float(CFG.get('early_production_taper_minutes',0))/60 else 1  # Nr. 295 Starthilfe-Auslauf
    TAPER_RES=CFG.get('early_production_taper_resources','').split(';')
    wf=max(0.0,min(1,pop_cap()/max(1,workers())))
    for b in s.lvl:
        r=B[b]['effect_resource_id']
        if B[b]['effect_type']=='production_per_hour' and s.lvl[b]:
            amt=eff(b)*h*wf*(boost if boost>1 else (taper if r in TAPER_RES else 1))*(1+FEAST_PCT/100*max(0,min(t0+h,s.feast_until)-t0)/h)*(1+guild_bonus('production_bonus_pct')/100)*(1+rb('prod_'+KEYS.get(r,'x')+'_pct')/100)
            if r=='res_food': amt*=1-max(0,(1-float(CFG['winter_food_production_mult']))+rb('winter_penalty_pp')/100)*winter_h(t0,t0+h)/h
            s.res[r]+=amt
    s.res['res_food']=max(0,s.res['res_food']-sum(n*float(U[u]['upkeep_food_per_hour']) for u,n in s.army.items())*h*(1+rb('upkeep_pct')/100))
    for r in s.res:
        if s.res[r]>=cap(r):
            if r in ('res_wood','res_stone'): d=int(t0//24)+1;s.overflow[d]=s.overflow.get(d,0)+s.res[r]-cap(r)
            if r!='res_knowledge': s.ovr[r]=s.ovr.get(r,0)+s.res[r]-cap(r)  # Nr. 305: Überlauf je Rohstoff
            if r=='res_knowledge': s.res[r]=cap(r); continue  # Nr. 305: Wissen zählt nicht als Lagertreffer
            s.res[r]=cap(r); s.storage_hits+=1; d=int(t0//24)+1; s.hitr.setdefault(d,{}); s.hitr[d][r]=s.hitr[d].get(r,0)+1
def prod_rate(r):
    return sum(eff(b) for b in s.lvl if s.lvl[b] and B[b]['effect_type']=='production_per_hour' and B[b]['effect_resource_id']==r)
def minigame_day():
    if not MINIGAME: return
    for r,h in MINIGAME['res']: s.res[r]=min(cap(r),s.res[r]+prod_rate(r)*h);s.mg_res+=prod_rate(r)*h
    s.xp+=MINIGAME.get('hero_xp',0)
def guild_level():
    if s.guild_xp is None: return 0
    return max(int(x['guild_level']) for x in GL if int(x['guild_xp_total'])<=s.guild_xp)
def guild_bonus(k):
    L=guild_level();return float(GL[L-1][k]) if L else 0
def guild_day():
    if GUILD is None: return
    if s.guild_xp is None:
        if s.lvl['bld_center']<int(CFG['guild_unlock'].split(':')[1]): return
        s.guild_xp=float(GL[GUILD['join_level']-1]['guild_xp_total'])
    s.guild_xp+=GUILD['xp_per_day']
    r=max(('res_food','res_wood','res_stone'),key=lambda k:s.res[k]/cap(k));d=float(CFG['guild_donation_cost_res'])
    if s.res[r]>=d+0.3*cap(r): s.res[r]-=d;s.donated+=d;s.guild_coin+=int(INC['inc_guild_coin']['amount'])
    while s.guild_coin>=80: s.guild_coin-=80;s.xp+=1000  # Gilden-Shop: Heldenerfahrung (Limit 5/Woche ~ 0,7/Tag)
def cost(b,L): x=LV[(b,L)];return {r:float(x['cost_'+KEYS[r]]) for r in KEYS}
def afford(c): return all(s.res[r]>=v for r,v in c.items())
def pay(c):
    for r,v in c.items(): s.res[r]-=v
ORDER=['bld_center','bld_storage','bld_hut','bld_gatherer','bld_woodcutter','bld_barracks','bld_quarry','bld_shell_beach','bld_hunter','bld_shaman_hut','bld_trader','bld_palisade']
def center_blocks():
    return s.camp<len(C) and int(C[s.camp]['req_center_level'])>s.lvl['bld_center']
def try_upgrade():
    did=True
    while did:
        did=False
        for b in ORDER:
            L=s.lvl.get(b,0)+1
            if L>int(B[b]['max_level']) or not bld_ok(b): continue
            if b!='bld_center' and L>s.lvl['bld_center']: continue
            if SAVE and center_blocks() and b in ('bld_trader','bld_palisade'): continue
            x=LV[(b,L)]
            if x['req_campaign_level'] and s.camp<CIDX(x['req_campaign_level']): continue
            c=cost(b,L)
            if any(v>cap(r) for r,v in c.items()) and b!='bld_storage': continue
            if afford(c):
                pay(c);s.lvl[b]=L;did=True
                if b=='bld_center': s.gems+=int(INC['inc_center_levelup']['amount'])
                break
def gold_reserve():
    L=s.lvl['bld_center']+1
    if L<=10: return cost('bld_center',L)['res_gold']
    if E2_GOLD_PRIORITY and s.e2:  # v1.6.13 Nr. 286: E2-Forschung vor Heldenlevel/Manöver/Schmiede – Gold der nächsten E2-Stufe bleibt reserviert
        nx=[float(RCOST2[(n,s.rlv.get(n,0)+1)]['gold']) for n,x in RN2.items() if s.rlv.get(n,0)<int(x['max_level']) and all(s.rlv.get(p.split(':')[0],0)>=int(p.split(':')[1]) for p in x['prereqs'].split(';') if p)]
        return min(nx) if nx else 0
    return 0
def heroes_and_sinks():
    if not feature('feature_hero_level_gold'): return
    # Trainingsmanöver = Nahrungssenke
    mf,mg,mx=float(CFG['maneuver_food']),float(CFG['maneuver_gold']),float(CFG['maneuver_hero_xp'])
    while s.res['res_food']>0.7*cap('res_food')+mf*0 and s.res['res_food']>=mf and s.res['res_gold']-mg>=gold_reserve():
        s.res['res_food']-=mf;s.res['res_gold']-=mg;s.xp+=mx*(1+guild_bonus('maneuver_xp_bonus_pct')/100);s.maneuvers+=1
    # Heldenlevel = Gold-Hauptsenke (niedrigster Held zuerst)
    cap_l=int(CFG['hero_level_cap_epoch_1'])
    while True:
        cand=[h for h,l in s.heroes.items() if l<cap_l]
        if not cand: break
        h=min(cand,key=lambda x:s.heroes[x]);l=s.heroes[h]
        xc,gc=float(HLV[l]['xp_cost_to_next']),float(HLV[l]['gold_cost_to_next'])
        if s.xp>=xc and s.res['res_gold']-gc>=gold_reserve():
            s.xp-=xc;s.res['res_gold']-=gc;s.heroes[h]+=1;s.gold_heroes+=gc
        else: break
def gear_day():
    return
def gear_level_cap():  # v0.9: Ausrüstungsstufe <= Häuptlingsfeuer-Stufe (game_config gear_level_cap_rule)
    cap=s.lvl['bld_center']-1
    if s.e2: cap=min(cap,int(GEAR_UNLOCK_CFG['e2_center_max_level'])-1)
    return cap
def gear():
    if not GEAR or not feature('feature_forge'): return
    for h in list(s.heroes)[:1]:
        for sl in SLOTSTAT:
            if (h,sl) not in s.gear and s.camp>=CIDX(GSLOT[sl]['unlock']): s.gear[(h,sl)]=('gr_common',1)
        for sl in ART_SLOTS:
            if (h,sl) in s.artifacts: continue
            if sl=='slot_artifact_1' and s.camp>=CIDX(GEAR_UNLOCK_CFG['gear_unlock_slot_artifact_1']):
                s.artifacts[(h,sl)]=GEAR_UNLOCK_CFG['gear_start_artifact_1']
            elif sl=='slot_artifact_2' and s.e2:
                s.artifacts[(h,sl)]=GEAR_UNLOCK_CFG['gear_start_artifact_2']
    nc=s.lvl['bld_center']+1;res_c=cost('bld_center',nc) if nc<=10 else {r:0 for r in KEYS}
    if 'ascend_reserve' in CFG.get('forge_reserve_warning_scope','') and s.lvl['bld_center']<10:  # Nr. 305: Warnung schützt auch Gold/Stein für Feuer 10 (gilt auch für Schmiede-zuerst: Warnung wird befolgt)
        c10=cost('bld_center',10);res_c={r:max(res_c.get(r,0),c10.get(r,0)) for r in set(res_c)|set(c10)}
        if s.res['res_gold']<c10.get('res_gold',0): return
    while True:
        best=None
        for k,(r,l) in s.gear.items():
            mx=int(GRAR[r]['max_upgrade_level'])
            if l<mx and l<gear_level_cap(): c=EQ_UP[(r,l)];key=(l,0)
            elif l<mx: continue
            elif r!='gr_master':
                refine='refine_common_to_fine' if r=='gr_common' else 'refine_fine_to_master'
                c=EQ_UP[refine];key=(l,1)
            else: continue
            if best is None or key<best[0]: best=(key,k,c)
        if not best: return
        _,k,(g,st,wd)=best
        if GEAR_FIRST:
            if s.res['res_gold']<g or s.res['res_stone']<st or s.res['res_wood']<wd: return
            if 'ascend_reserve' in CFG.get('forge_reserve_warning_scope','') and s.lvl['bld_center']<10 and (s.res['res_stone']-st<res_c.get('res_stone',0) or s.res['res_gold']-g<res_c.get('res_gold',0)): return
        elif s.res['res_gold']-g<gold_reserve() or s.res['res_stone']-st<res_c['res_stone'] or s.res['res_wood']-wd<res_c['res_wood']: return
        s.res['res_gold']-=g;s.res['res_stone']-=st;s.res['res_wood']-=wd;s.gear_spent=[s.gear_spent[0]+g,s.gear_spent[1]+st,s.gear_spent[2]+wd]
        r,l=s.gear[k]
        if l<int(GRAR[r]['max_upgrade_level']): s.gear[k]=(r,l+1)
        else: s.gear[k]=({'gr_common':'gr_fine','gr_fine':'gr_master'}[r],l)
def train():
    target=1.3*float(C[s.camp]['recommended_power']) if s.camp<len(C) else 0
    types=['unit_club']+(['unit_sling'] if unlocked('unit_sling') else []);i=0
    while army_pop()<army_cap() and power()<target:
        u=types[i%len(types)];i+=1
        c={'res_food':float(U[u]['cost_food']),'res_wood':float(U[u]['cost_wood']),'res_stone':float(U[u]['cost_stone']),'res_gold':float(U[u]['cost_gold']),'res_knowledge':0}
        if not afford(c) or army_pop()+int(U[u]['pop_cost'])>army_cap(): break
        pay(c);s.army[u]=s.army.get(u,0)+1
def fight(max_n=99):
    n=0
    while s.camp<len(C) and n<max_n:
        c=C[s.camp]
        if int(c['req_center_level'])>s.lvl['bld_center']: break
        rec=float(c['recommended_power']);p=power();sup=float(c['supply_food_cost'])*(1+rb('supply_cost_pct')/100)
        if p<rec or s.res['res_food']<sup: break
        mm=MIN_PER_CH[int(c['chapter'])]
        if getattr(s,'budget',99)<mm: break
        s.budget=getattr(s,'budget',99)-mm
        s.res['res_food']-=sup;s.food_supply+=sup
        x=p/(SIM_CAL*rec)  # kalibriert gegen Dev-Ganzzahl-Kampfsim (v0.7)
        loss=0 if x>=1.2 else max(0,min(0.6,0.25+(1.0-x)*1.25))
        s.losses.append((c['campaign_level_id'],round(loss,2)))
        for u in s.army: s.army[u]=int(s.army[u]*(1-loss))
        for r,k in KEYS.items(): s.res[r]=min(cap(r),s.res[r]+float(c['reward_'+k]))
        s.xp+=float(c['reward_hero_xp']);s.gems+=int(c['reward_gems']);s.tickets+=int(c['reward_tickets'])
        if p>=1.3*rec: s.gems+=int(INC['inc_campaign_3star']['amount'])
        s.camp+=1;n+=1
        for t in c['unlocks'].split(';'):
            if t.startswith('hero_'): s.heroes.setdefault(t,1)
        train()
    return n
def pull(banner):
    rs=RATES[(banner,'SSR')];s.pity+=1;s.srpity+=1;p=float(rs['base_rate_pct'])
    if int(rs['soft_pity_start']) and s.pity>=int(rs['soft_pity_start']): p+=float(rs['soft_pity_increment_pct'])*(s.pity-int(rs['soft_pity_start'])+1)
    if (int(rs['hard_pity']) and s.pity>=int(rs['hard_pity'])) or random.random()*100<p: s.pity=0;s.ssr+=1;s.srpity=0;return
    if s.srpity>=10 or random.random()*100<float(RATES[(banner,'SR')]['base_rate_pct']): s.srpity=0
def starter_pull():
    s.spity+=1
    if s.spity>=20 or random.random()*100<float(RATES[('banner_starter','SSR')]['base_rate_pct']): s.ssr+=1;s.spity=-999
def summon():
    while s.starter<20 and s.gems>=100: s.gems-=100;s.starter+=1;s.summons+=1;starter_pull()
    while s.tickets>0: s.tickets-=1;s.summons+=1;pull('banner_standard')
    while s.gems>=150 and s.starter>=20: s.gems-=150;s.summons+=1;pull('banner_standard')
def epoch_ready():
    return s.camp>=len(C) and s.lvl['bld_center']>=10 and s.res['res_knowledge']>=2000 and (not (RESEARCH and RESEARCH_GATE) or s.rlv.get('rs_e1_sternkunde',0)>=1)
def r_free_s(): return float(CFG.get('research_free_finish_s',180))+rb('free_finish_s')
def r_reserve():
    L=s.lvl['bld_center']+1
    return cost('bld_center',L) if L<=10 and not RESEARCH_FIRST else {}
def research(now):
    if not RESEARCH or s.lvl['bld_center']<RESEARCH_UNLOCK_FIRE: return
    if s.rcur:
        rem=(s.runtil-now)*3600
        if rem>r_free_s() and USE_GLUT and s.rbank>0: u=min(s.rbank,rem-r_free_s());s.rbank-=u;s.runtil-=u/3600;rem-=u
        if rem<=r_free_s(): n,l=s.rcur;s.rlv[n]=l;s.rdone_t[(n,l)]=now;s.rcur=None
        else: return
    cand=[]
    if s.e2:  # v1.6.13 Nr. 286: E2-Knoten mit Voraussetzungen + Kosten aus research_costs_e2.csv (Wissen = Hauptkosten)
        short=set()
        for n,x in RN2.items():
            l=s.rlv.get(n,0)+1
            if l>int(x['max_level']): continue
            if any(s.rlv.get(p.split(':')[0],0)<int(p.split(':')[1]) for p in x['prereqs'].split(';') if p): continue
            rc=RCOST2[(n,l)];c={'res_food':float(rc['food']),'res_wood':float(rc['wood']),'res_stone':float(rc['stone']),'res_gold':float(rc['gold']),'res_knowledge':float(rc['knowledge'])}
            if afford(c): cand.append((4,float(rc['time_s']),n,l,c))
            else: short|={r for r,v in c.items() if s.res[r]<v}
        s.e2_short=short
    for n,x in RN.items():
        l=s.rlv.get(n,0)+1
        if l>int(x['max_level']): continue
        rc=RCOST[(n,l)]
        if int(rc['fire_req'])>s.lvl['bld_center']: continue
        if any(s.rlv.get(p.split(':')[0],0)<int(p.split(':')[1]) for p in x['prereqs'].split(';') if p): continue
        c={'res_food':float(rc['food']),'res_wood':float(rc['wood']),'res_stone':float(rc['stone']),'res_gold':float(rc['gold'])}
        res=r_reserve() if (n not in STERN_PATH or R_RES_ALL) else {}  # v1.2: Reserve-Warnung nur für reine Wirtschaftsknoten
        if not all(s.res[r]-v>=(res.get(r,0) if r!='res_food' else 0) for r,v in c.items()): continue
        cand.append(((0 if (n,l) in CRIT else 1 if RN[n]['branch']=='militaer' else 2 if n in STERN_PATH else 3),float(rc['time_s']),n,l,c))
    if not cand: return
    _,ts,n,l,c=min(cand);pay(c)
    if n in RN and (n,l) not in CRIT and RN[n]['branch']!='militaer': ts*=float(CFG.get('research_time_mult_offpath','1'))  # v1.6.10 Uhren-Überhang: Nebenpfad-Stufen (nicht Aufstieg/Militär) langsamer
    for i,r in enumerate(('res_food','res_wood','res_stone','res_gold')): s.rspent[i]+=c[r]
    if n in RN2: s.e2_spent=[a+c.get(r,0) for a,r in zip(s.e2_spent,('res_wood','res_stone','res_gold','res_knowledge'))]
    s.rlast=(n,l)
    mult=float(CFG.get('research_first_hour_speed_mult',4)) if now-INSTALL<1 else 1
    s.rcur=(n,l);s.runtil=now+ts/mult/3600
    if ts/mult<=r_free_s(): s.rlv[n]=l;s.rdone_t[(n,l)]=now;s.rcur=None
def tree_open():  # gibt es noch einen Forschungsknoten (E1 bzw. E2)?
    e1=any(s.rlv.get(n,0)<int(x['max_level']) for n,x in RN.items());e2=s.e2 and any(s.rlv.get(n,0)<int(x['max_level']) for n,x in RN2.items())
    return bool(s.rcur) or e1 or e2
def trade_day():  # v1.6.10 Tauschplatz-Überschuss → Gold; Nr. 292: Standard ~trade_daily_res/Tag, Überlauf-Tausch als Option
    if not (TRADE and E2) or CFG.get('trade_overflow_enabled')!='1' or not s.lvl.get('bld_trader'): return
    left=float(CFG['trade_overflow_daily_cap_res'] if TRADE_MODE=='overflow' else CFG.get('trade_daily_res',400));rate=eff('bld_trader')/100*float(CFG['trade_gold_per_res']);th=float(CFG['trade_overflow_threshold_pct'])/100
    for r in sorted(('res_wood','res_stone'),key=lambda r:-(s.res[r]/cap(r))):
        x=min(left,max(0,s.res[r]-th*cap(r)));s.res[r]-=x;left-=x;g=x*rate;s.res['res_gold']=min(cap('res_gold'),s.res['res_gold']+g);s.traded[0]+=x;s.traded[1]+=g
FEAST_PCT=float(dict(x.split(':') for x in CFG.get('tribal_feast_buff','production_pct:0;duration_h:0').split(';'))['production_pct'])
FEAST_H=float(dict(x.split(':') for x in CFG.get('tribal_feast_buff','production_pct:0;duration_h:0').split(';'))['duration_h'])
FEAST_C={k:float(v) for k,v in (x.split(':') for x in CFG.get('tribal_feast_cost','res_wood:0').split(';'))}
def _ext_cost(b,L):  # Nr. 292: Palisade/Vorratshöhle L11–15 = Kosten L10 × growth^(L−10), auf 5 gerundet, ohne Gold
    g=float(CFG['e2_palisade_ext_cost_growth' if b=='bld_palisade' else 'e2_storage_ext_cost_growth']);c=cost(b,10)
    return {r:(5*round(c[r]*g**(L-10)/5) if r in ('res_wood','res_stone') else 0.0) for r in c}
def _e2_next_cost():
    nx=[RCOST2[(n,s.rlv.get(n,0)+1)] for n,x in RN2.items() if s.rlv.get(n,0)<int(x['max_level']) and all(s.rlv.get(p.split(':')[0],0)>=int(p.split(':')[1]) for p in x['prereqs'].split(';') if p)]
    return {'res_wood':min((float(x['wood']) for x in nx),default=0),'res_stone':min((float(x['stone']) for x in nx),default=0)}
def e2_sinks(now,day):  # Nr. 292: Senken nur in E2, nach der Forschung; nächste E2-Stufe (Holz/Stein) bleibt reserviert
    if not (E2_SINKS and s.e2): return
    rsv=_e2_next_cost();lo,hi=CFG['e2_palisade_ext_levels'].split('-')
    for b in ('bld_storage','bld_palisade'):
        L=10+s.ext.get(b,0)+1
        if L>int(hi) or s.lvl.get(b,0)<10: continue
        c=_ext_cost(b,L)
        if all(s.res[r]-c[r]>=rsv.get(r,0) for r in ('res_wood','res_stone')):
            for r in ('res_wood','res_stone'): s.res[r]-=c[r]
            s.ext[b]=s.ext.get(b,0)+1;s.ext_spent[0]+=c['res_wood'];s.ext_spent[1]+=c['res_stone']
    kc=float(CFG.get('ahnen_ritual_knowledge',0));kl=int(CFG.get('ahnen_ritual_daily_limit',0)) if CFG.get('ancestor_ritual_enabled','no')=='yes' else 0  # Nr. 300 Ahnenritual (per Key)
    while kc and s.ritual_day.get(day,0)<kl and s.res['res_knowledge']-kc>=float(CFG.get('ahnen_ritual_keep_knowledge',0)) and s.res['res_knowledge']/cap('res_knowledge')>float(CFG.get('ahnen_ritual_trigger_pct',50))/100:
        s.res['res_knowledge']-=kc;s.xp+=float(CFG.get('ahnen_ritual_hero_xp',0));s.ritual_day[day]=s.ritual_day.get(day,0)+1;s.rituals+=1
    AL=int(CFG.get('ahnen_site_levels',0))  # Nr. 299 Ahnenstätte (Holz/Stein/Wissen/Gold, Kurve ×1,25)
    while s.ahnen<AL:
        g=float(CFG.get('ahnen_site_cost_growth',1.25));L=s.ahnen+1
        c={k:5*round(float(v)*g**(L-1)/5) for k,v in (x.split(':') for x in CFG['ahnen_site_cost_l1'].split(';'))}
        if any(c[r]>cap(r) for r in c): break
        ok=all(s.res[r]-v>=(rsv.get(r,0) if r!='res_gold' else gold_reserve()) for r,v in c.items())
        trig=max(s.res['res_wood']/cap('res_wood'),s.res['res_stone']/cap('res_stone'),s.res['res_knowledge']/cap('res_knowledge'))>float(CFG.get('ahnen_site_trigger_pct',0))/100
        if not (ok and trig): break
        for r,v in c.items(): s.res[r]-=v
        for i_,r in enumerate(('res_wood','res_stone','res_knowledge','res_gold')): s.ahnen_spent[i_]+=c.get(r,0)
        s.ahnen+=1
    lim=FEAST_LIMIT_ARG if FEAST_LIMIT_ARG is not None else int(CFG.get('tribal_feast_daily_limit',0));tap=max(1,int(CFG.get('feast_multi_tap',1)))
    def _trig():
        w_,s_,k_=s.res['res_wood']/cap('res_wood'),s.res['res_stone']/cap('res_stone'),s.res['res_knowledge']/cap('res_knowledge')
        return (max(w_,s_,k_) if CFG.get('tribal_feast_trigger','both')=='either' else min(w_,s_))>float(CFG.get('tribal_feast_trigger_pct',CFG['trade_overflow_threshold_pct']))/100
    while s.feast_day.get(day,0)<lim and _trig():
        n=tap if s.feast_day.get(day,0)+tap<=lim and all(s.res[r]-tap*v>=(rsv.get(r,0) if r!='res_gold' else gold_reserve()) for r,v in FEAST_C.items()) else 1  # Nr. 299 Button „Fest ×2“: ein Tippen = feast_multi_tap Feste
        if not all(s.res[r]-n*v>=(rsv.get(r,0) if r!='res_gold' else gold_reserve()) for r,v in FEAST_C.items()): break
        for r,v in FEAST_C.items(): s.res[r]-=n*v
        for i_,r in enumerate(('res_wood','res_stone','res_food','res_gold')): s.feast_spent[i_]+=n*FEAST_C.get(r,0)
        s.feast_day[day]=s.feast_day.get(day,0)+n;s.feasts+=n;s.feast_until=max(now,s.feast_until)+n*FEAST_H
def ascend():  # v1.6.10 Aufstieg in E2-Übergangswirtschaft; v1.6.13 Nr. 286: Rest-Wissen-Übertrag + Aufstiegsgeschenk (delta-e2-uebergang)
    s.ascend_stock={r:int(v) for r,v in s.res.items()}  # Bestand am Aufstiegstag vor Übertrag
    s.e2=True;s.res['res_knowledge']=(s.res['res_knowledge']-float(CFG['epoch_ascend_knowledge_cost']))*float(CFG.get('ascend_knowledge_carryover_pct',100))/100
    for r in ('res_food','res_wood','res_stone','res_gold'): s.res[r]*=float(CFG['epoch_ascend_resource_carry_pct'])/100
    s.res['res_gold']+=float(CFG.get('e2_ascend_grant_gold',0));s.res['res_knowledge']+=float(CFG.get('e2_ascend_grant_knowledge',0))
    s.ascend_start={r:int(v) for r,v in s.res.items()}
def run(days=21):
    reset();rows=[];t=INSTALL
    for day in range(1,days+1):
        h0=s.storage_hits;g0=s.gold_heroes;m0=s.maneuvers;f0=s.food_supply
        s.gems+=int(INC['inc_login']['amount'])+int(INC['inc_daily_quests']['amount'])
        if day%7==0: s.gems+=int(INC['inc_weekly_quests']['amount']);s.tickets+=int(INC['inc_weekly_ticket']['amount'])
        if day==7: s.tickets+=int(INC['inc_login_7day']['amount'])
        if E2 and s.epoch_day and not s.e2: ascend()
        guild_day();minigame_day();gear_day();trade_day();s.rbank+=clock_income(day,s.lvl['bld_center']-getattr(s,'_cl',1),tree_open())*60 if USE_GLUT else 0;s._cl=s.lvl['bld_center']
        for st in [8,12.5,18,22]:
            now=(day-1)*24+st
            if now<INSTALL: continue
            produce(now-t,t);t=now
            s.budget=FIRST_SESSION_MIN if now==INSTALL else SESSION_MISSION_MIN  # v0.7: Missionen kosten Zeit
            for _ in range(3 if now>INSTALL else 12):
                (gear() if GEAR_FIRST else None);(research(now) if RESEARCH_FIRST else None);try_upgrade();train();fight();quests();heroes_and_sinks();gear();research(now);e2_sinks(now,day)
            summon()
            if s.epoch_day is None and epoch_ready(): s.epoch_day=day
            if s.res['res_gold']<200: s.gold_low_h+=1  # je Session-Stichprobe
            if s.e1_done is None and all(s.rlv.get(n,0)>=int(x['max_level']) for n,x in RN.items()): s.e1_done=now/24
            if s.e2 and s.e2_done is None and all(s.rlv.get(n,0)>=int(x['max_level']) for n,x in RN2.items()): s.e2_done=now/24
            if s.e2 and s.e2_done is None and not s.rcur: s.e2_idle+=1;[s.e2_short_n.__setitem__(r,s.e2_short_n.get(r,0)+1) for r in getattr(s,'e2_short',())]  # Leerlauf-Session: welcher Rohstoff fehlt
        if day==8: s.stone_d8=int(s.res['res_stone'])  # Nr. 305: Stein Ende Tag 8 (eindeutig, getrennt vom Aufstiegsmorgen)
        if IDEAS and s.e2:  # Nr. 312: Ideen-Module als Gold-Senken (nur mit --ideas)
            dd=day-(s.epoch_day+1)+1
            for need,cost_ in ((dd>=int(CFG.get('arrival_path_gold_task_from_chapter',12)),float(CFG.get('arrival_path_gold_task_cost',1000))),
                               (s.e2_done is not None,float(CFG.get('heropath_gold_stake_per_fight',200))*int(CFG.get('heropath_free_fights_daily',5))),
                               (s.e2_done is not None,float(CFG.get('guild_board_gold_daily_cap_per_member',1500)))):
                if need and s.res['res_gold']>=cost_: s.res['res_gold']-=cost_;s.idea_gold+=cost_
        s.bank_log[day]=s.rbank/3600;s.gold_log=getattr(s,'gold_log',{});s.gold_log[day]=int(s.res['res_gold'])
        hl=sorted(s.heroes.values(),reverse=True)
        rows.append(dict(day=day,center=s.lvl['bld_center'],camp=s.camp,power=int(power()),rec_next=C[s.camp]['recommended_power'] if s.camp<len(C) else '-',
            food=int(s.res['res_food']),wood=int(s.res['res_wood']),gold=int(s.res['res_gold']),know=int(s.res['res_knowledge']),storage=int(cap('res_wood')),
            limit_hits_day=s.storage_hits-h0,gold_to_heroes_day=int(s.gold_heroes-g0),maneuvers_day=s.maneuvers-m0,supply_food_day=int(s.food_supply-f0),
            heroes=len(s.heroes),hero_lv='/'.join(map(str,hl)),stone=int(s.res['res_stone']),clock_bank_h=round(s.rbank/3600,1),armycap=int(army_cap()),gems=s.gems,summons=s.summons,ssr=s.ssr,epoch2_ready='ja' if s.epoch_day else '-'))
    return rows
if __name__=='__main__':
    days=int(sys.argv[2]) if len(sys.argv)>2 else 21  # v1.6.13 Nr. 286: Standard 21 Tage (E2-Baum)
    rows=run(days)
    print('|'+'|'.join(rows[0])+'|');print('|'+'---|'*len(rows[0]))
    for r in rows: print('|'+'|'.join(str(v) for v in r.values())+'|')
    print(f'\nEpoche-2-Bereitschaft (L30 + Feuer 10 + 2.000 Wissen): Tag {s.epoch_day}' if s.epoch_day else '\nEpoche-2-Bereitschaft: nicht in diesem Zeitraum')
    if s.ascend_stock:
        a,b=s.ascend_stock,s.ascend_start
        print(f"Aufstieg (Übergang aktiv) Tag {s.epoch_day+1}: Bestand vorher N {a['res_food']} / H {a['res_wood']} / S {a['res_stone']} / G {a['res_gold']} / W {a['res_knowledge']} → E2-Start N {b['res_food']} / H {b['res_wood']} / S {b['res_stone']} / G {b['res_gold']} / W {b['res_knowledge']}")
    print(f"E1-Baum fertig: Tag {s.e1_done:.1f}" if s.e1_done else "E1-Baum: nicht fertig")
    print(f"E2-Baum fertig: Tag {s.e2_done:.1f}" if s.e2_done else "E2-Baum: nicht fertig", f"| E2 bezahlt H/S/G/W {[int(x) for x in s.e2_spent]} | Leerlauf-Sessions E2 {s.e2_idle}, fehlender Rohstoff {s.e2_short_n} | Uhrenvorrat Ende {s.rbank/3600:.1f} h")
    hits=[r['limit_hits_day'] for r in rows]
    rng=lambda a,b:[hits[d-1] for d in range(a,min(b,len(hits))+1)]
    print(f"Lagertreffer/Tag T9–19 Ø {sum(rng(9,19))/max(1,len(rng(9,19))):.1f} · T19–21 Ø {sum(rng(19,21))/max(1,len(rng(19,21))):.1f} · T9–{len(hits)} Ø {sum(rng(9,len(hits)))/max(1,len(rng(9,len(hits)))):.1f} · max {max(rng(9,len(hits)) or [0])}")
    print('Überlauf Holz+Stein (verfallen) je Tag: '+', '.join(f"T{d} {int(v)}" for d,v in sorted(s.overflow.items()) if d>=9))
    print(f"E2-Senken: Stammesfeste {s.feasts} (H/S/N/G {[int(x) for x in s.feast_spent]}), Ausbau {s.ext} (H/S {[int(x) for x in s.ext_spent]}), Lager Holz Ende {int(cap('res_wood'))}")
    print(f"Tausch-Modus {TRADE_MODE} (Tag-Menge {CFG['trade_overflow_daily_cap_res'] if TRADE_MODE=='overflow' else CFG.get('trade_daily_res')}): {int(s.traded[0])} Holz/Stein → {int(s.traded[1])} Gold")
    print(f"Ahnenstätte Stufe {s.ahnen} (H/S/W/G {[int(x) for x in s.ahnen_spent]}), Ahnenrituale {s.rituals}, Gold Ende Tag {len(rows)}: {rows[-1]['gold']}")
    print(f"Stein Ende Tag 8: {s.stone_d8} · Stein am Aufstiegsmorgen (Tag {s.epoch_day+1 if s.epoch_day else '-'}, vor Übertrag): {s.ascend_stock['res_stone'] if s.ascend_stock else '-'}")
    print('Überlauf je Rohstoff gesamt (ohne Wissen): '+', '.join(f"{k} {int(v)}" for k,v in sorted(s.ovr.items())))
    print(f"Lagertreffer gesamt (ohne Wissen): {s.storage_hits} · Ideen-Module {'AN' if IDEAS else 'aus'}, Gold in Ideen-Senken {int(s.idea_gold)}")
    print('Treffer je Rohstoff ab T9: '+str({d:v for d,v in sorted(s.hitr.items()) if d>=9}))
