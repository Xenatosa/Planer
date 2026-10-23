# Epodarien – Questreihe Epoche 1, Kapitel 1–3 (v2)
**Status: Entwurf für Fabian** · 23.10.2026 · Basis: Romanfassung v2 (Prolog, Kap. 1–3), Storybuch E1–E3, Bestiarium Buch 1, Bossentwürfe Buch 1, Kampagnen-Struktur 45 Stufen (K1: 1–15, K2: 16–30, K3: 31–45).

**Struktur:** Jede der 45 Kampagnen-Stufen hat eine Quest. Der Hauptquest-Faden läuft durch alle 45; Sidequests und Baukunst docken an. Zieltypen: `quest-system-v2.md`. `[Ergänzung]` = über der Lore, `[Annahme]` = Zahl per Config.

**Gegnertypen Epoche 1 (7):** Klammbeißer, Frostkrähe, Höhlenhyäne `[Ergänzung]`, Eisluchs `[Ergänzung]`, Eisfuchs, Kundschafter, Schneehasen-Zug `[Ergänzung]`, Frostwolf, Kristallwelpe.
**Mini-Bosse:** K1: Schattenpfote (Luchs, S5), Die Meute (Hyänen, S10) · K2: Der wartende Bock (Eisfuchs, S20), Die Weißgewandete (Kundschafterin, S25) · K3: Die Schattenwölfin (Frostwolf, S35), Die Wadenbeißer-Brut (Kristallwelpen, S40).
**Endbosse:** K1 Knirsch (S15), K2 Vask der Stumme (S30), K3 Eisfang (S45).

---

## Teil A — Hauptquest (45 Quests, eine je Stufe)

### Kapitel 1: Der rohe Stein (Q_MAIN_K1_001–015)

### Q_MAIN_K1_001 „Rauch über dem Tal"
- Prequest: Tutorial-Abschluss (Q_TUT_019)
- Aufgabe: `campaign_cleared` | k1_s1 | 1
- Belohnung: `hero_xp;brakka` / 50
- Text: Zwei Klammbeißer folgten dem Rauch. Olm stellte die Reihe, bevor jemand den Befehl brauchte. Brakka zählte danach: niemand fehlte.

### Q_MAIN_K1_002 „Hungrige Nachbarn"
- Prequest: Q_MAIN_K1_001
- Aufgabe: `campaign_cleared` | k1_s2 | 1
- Belohnung: `res_wood` / 100
- Text: Die Krähen griffen nicht an. Sie warteten, bis jemand die Vorratspfosten verließ, und trugen weg, was sie tragen konnten. „Der Speer hat einen Nachbarn oder er hat nichts", sagte Olm.

### Q_MAIN_K1_003 „Die Jäger vom Fluss"
- Prequest: Q_MAIN_K1_002
- Aufgabe: `campaign_cleared` | k1_s3 | 1
- Belohnung: `hero_xp;olm` / 80
- Text: Am Fluss standen drei Klammbeißer zwischen den Jägern und dem Wasser. Olm baute die Reihe am Pfosten auf: beide Hände, das Ende am Oberschenkel.

### Q_MAIN_K1_004 „Fährten im Neuschnee"
- Prequest: Q_MAIN_K1_003
- Aufgabe: `campaign_cleared` | k1_s4 | 1
- Belohnung: `hero_xp;tala` / 80
- Text: Tala fand die Fährte zuerst: eine verrenkte Spur, die dort endete, wo der Schnee wieder anfing. „Da lauert etwas", sagte sie. Niemand sah es. Am Abend griff es an.

### Q_MAIN_K1_005 „Schattenpfote" *(Mini-Boss)*
- Prequest: Q_MAIN_K1_004
- Aufgabe: `campaign_cleared` | k1_s5 | 1
- Belohnung: `hero_xp;tala;cur_gems_free` / 100;3
- Text: Ein alter Eisluchs, so grau, dass er mit dem Schnee verschwamm. Er wartete, bis die hintere Reihe ging, und sprang. Wer hinten niemanden ließ, verlor die Augen.

### Q_MAIN_K1_006 „Der Kreis am Fels"
- Prequest: Q_MAIN_K1_005
- Aufgabe: `campaign_cleared` | k1_s6 | 1
- Belohnung: `hero_xp;tala;echosplitter` / 80;5
- Text: Tala malte den Kreis auf den Fels am Südausgang. Die Krähen mieden die Stelle danach. „Sie lesen es", sagte sie. Bako lachte. Es war nicht zum Lachen.

### Q_MAIN_K1_007 „Schnee-Brecher"
- Prequest: Q_MAIN_K1_006
- Aufgabe: `campaign_cleared` | k1_s7 | 1
- Belohnung: `res_stone` / 100
- Text: Zwei Klammbeißer brachen durch den Zaun, während die Hyänen kreisten und warteten, wo die Reihe dünner wurde. Olm schob die Mitte nach. Es reichte.

### Q_MAIN_K1_008 „Nächte des Diebstahls"
- Prequest: Q_MAIN_K1_007
- Aufgabe: `campaign_cleared` | k1_s8 | 1
- Belohnung: `hero_xp;gorm` / 80
- Text: Vier Nächte, vier Krähen, eine Hyäne, die den Blick ablenkte. Gorm stand am Pfosten und sah in alle Richtungen gleich lange. „Das reicht nicht, wenn etwas wartet, bis du wegschaust."

### Q_MAIN_K1_009 „Am Eisbach"
- Prequest: Q_MAIN_K1_008
- Aufgabe: `campaign_cleared` | k1_s9 | 1
- Belohnung: `res_food` / 150
- Text: Am Eisbach kamen sie von drei Seiten: Beißer vorne, Hyänen in der Mitte, der Luchs hinten. Die Reihe hielt. Die Mitte drehte. Und hinten war jemand.

### Q_MAIN_K1_010 „Die Meute" *(Mini-Boss)*
- Prequest: Q_MAIN_K1_009
- Aufgabe: `campaign_cleared` | k1_s10 | 1
- Belohnung: `hero_xp;olm;cur_gems_free` / 120;5
- Text: Die Hyänen-Anführerin kannte die Reihenfolge des Lagers besser als jeder Jäger. Sie kreiste mit ihrer Meute und drückte genau da, wo niemand stand. Die Front fängt ab. Die Mitte dreht.

### Q_MAIN_K1_011 „Kalte Fährten"
- Prequest: Q_MAIN_K1_010
- Aufgabe: `campaign_cleared` | k1_s11 | 1
- Belohnung: `hero_xp;brakka` / 80
- Text: Die Fährten wurden breiter und tiefer. Etwas Schweres ging nun voran, und der Rest folgte in seinem Tritt. Brakka sagte nichts. Sie zählte.

### Q_MAIN_K1_012 „Eisbach-Furt"
- Prequest: Q_MAIN_K1_011
- Aufgabe: `campaign_cleared` | k1_s12 | 1
- Belohnung: `res_wood;res_stone` / 100;100
- Text: An der Furt kreuzten sich die Wege: Beißer, Krähen, eine Hyäne. Wer die Furt hielt, hielt das Tal. Die Reihe stand zum dritten Mal ohne Olms Anweisung.

### Q_MAIN_K1_013 „Der Asche-Fels"
- Prequest: Q_MAIN_K1_012
- Aufgabe: `campaign_cleared` | k1_s13 | 1
- Belohnung: `hero_xp;bako` / 80
- Text: Am Asche-Fels prallten vier Klammbeißer gegen die Reihe, während der Luchs von hinten kam. Bako hatte die Leine der Vorräte festgemacht. Die Leine hielt.

### Q_MAIN_K1_014 „Nacht des Bären"
- Prequest: Q_MAIN_K1_013
- Aufgabe: `campaign_cleared` | k1_s14 | 1
- Belohnung: `hero_xp;brakka;nara` / 100;100
- Text: Am Morgen lag eine Fährte im Schnee, doppelt so breit wie alles andere, was die Senke kannte. Vereiste Fellplatten schlugen an den Graten gegeneinander. „Er ist da", sagte Nara. Brakka zählte die Speere.

### Q_MAIN_K1_015 „Der Lehrboss" *(Endboss: Knirsch)*
- Prequest: Q_MAIN_K1_014
- Aufgabe: `campaign_cleared` | k1_s15 | 1
- Belohnung: `hero_xp;brakka;cur_tickets` / 200;1
- Text: Ein ausgemergelter Frost-Höhlenbär folgte nur noch der Wärme. Er war langsam, laut und telegrafierte jeden Schritt. Olm stellte die Reihe in die markierte Spalte: „Springt er, trifft er den Speer deines Nachbarn." Bei vierzig Prozent blieb er stehen. Er war erschöpft. Er war es immer gewesen — nur hatte es niemand so lange gesehen.

---

### Kapitel 2: Die Asche-Markierungen (Q_MAIN_K2_016–030)

### Q_MAIN_K2_016 „Naras Paste"
- Prequest: Q_MAIN_K1_015
- Aufgabe: `campaign_cleared` | k2_s16 | 1
- Belohnung: `hero_xp;nara` / 80
- Text: Nara mischte Asche mit Tierfett. Die Paste blieb auf Wangen und Ohren haften. Im Vorwinter hatten vier Menschen Finger verloren. Diesmal bekam niemand solche Stellen.

### Q_MAIN_K2_017 „Der Handabdruck"
- Prequest: Q_MAIN_K2_016
- Aufgabe: `campaign_cleared` | k2_s17 | 1
- Belohnung: `hero_xp;bako;echosplitter` / 80;5
- Text: Bako wischte sich die Hände an einem flachen Stein ab, und ein dunkler Handabdruck blieb. Am nächsten Tag war er noch da. Am Tag danach auch. Tala stand davor und sagte: „Das bleibt, auch wenn derjenige weg ist, der es gemacht hat."

### Q_MAIN_K2_018 „Hasenspur"
- Prequest: Q_MAIN_K2_017
- Aufgabe: `campaign_cleared` | k2_s18 | 1
- Belohnung: `res_food` / 150
- Text: Die Hasenzüge fressen die Nahrungsfelder leer und verschwinden, bevor jemand sie sieht. Schnelle Beine, keine Gnade. Brakka ließ die Felder drehen: „Wo sie gefressen haben, fressen sie nicht wieder."

### Q_MAIN_K2_019 „Der beobachtete Rückweg"
- Prequest: Q_MAIN_K2_018
- Aufgabe: `campaign_cleared` | k2_s19 | 1
- Belohnung: `hero_xp;tala` / 80
- Text: Einer lief mit, ohne zu kämpfen: weiß gekalkt, keine Last, kein Laut. Er merkte sich alles. „Stopp ihn, bevor er berichtet", sagte Brakka. „Was er weiß, weiß wer anderes."

### Q_MAIN_K2_020 „Der wartende Bock" *(Mini-Boss)*
- Prequest: Q_MAIN_K2_019
- Aufgabe: `campaign_cleared` | k2_s20 | 1
- Belohnung: `hero_xp;gorm;cur_gems_free` / 120;5
- Text: Ein alter Eisfuchs hatte gelernt zu warten. Er griff erst an, wenn eine Zone unbewacht war, und er wartete lange. „Keine Zone leer", sagte Brakka. „Egal wie sicher sie wirkt."

### Q_MAIN_K2_021 „Drei am Kamm"
- Prequest: Q_MAIN_K2_020
- Aufgabe: `campaign_cleared` | k2_s21 | 1
- Belohnung: `hero_xp;tala;cur_gems_free` / 100;5
- Text: Auf dem gegenüberliegenden Kamm standen drei Gestalten, so weiß, dass Tala sie für Steine hielt. Sie richteten ihre Köpfe nicht auf den Weg, sondern auf das Feuer. Tala begann zu zählen. Bei hundertsiebzig drehten sie sich um.

### Q_MAIN_K2_022 „Zeichen im Schnee"
- Prequest: Q_MAIN_K2_021
- Aufgabe: `campaign_cleared` | k2_s22 | 1
- Belohnung: `hero_xp;tala;echosplitter` / 100;5
- Text: Im Schnee lagen Asche-Zeichen, die niemand aus dem Stamm gemalt hatte. Dieselbe Grammatik wie Talas. Eine fremde Hand. „Wer es gelesen hat", sagte Tala, „hat es auch geschrieben."

### Q_MAIN_K2_023 „Der gemusterte Weg"
- Prequest: Q_MAIN_K2_022
- Aufgabe: `campaign_cleared` | k2_s23 | 1
- Belohnung: `hero_xp;brakka` / 80
- Text: Die Kundschafter notierten die Routen des Stammes: wo das Holz herkommt, wer wann geht. Brakka ließ die Wege wechseln. „Ein Weg ist eine Einladung. Ein Muster ist ein Zeitplan."

### Q_MAIN_K2_024 „Kalter Vorstoß"
- Prequest: Q_MAIN_K2_023
- Aufgabe: `campaign_cleared` | k2_s24 | 1
- Belohnung: `res_food;res_stone` / 100;100
- Text: Die Beobachtung wurde Druck: Sie griffen jetzt da an, wo die Aufzeichnungen eine Lücke zeigten. Es war keine Zufälligkeit mehr. Es war Planung.

### Q_MAIN_K2_025 „Die Weißgewandete" *(Mini-Boss)*
- Prequest: Q_MAIN_K2_024
- Aufgabe: `campaign_cleared` | k2_s25 | 1
- Belohnung: `hero_xp;tala;cur_tickets` / 120;1
- Text: Eine Kundschafterin, größer als die anderen, mit Knoten in ihrem Riemen: Sie zählte das Feuer des Dorfes so wie Brakka die Bündel zählte. „Beobachter zuerst", sagte Brakka. „Bevor der Zähler fertig ist."

### Q_MAIN_K2_026 „Nebel am Südhang"
- Prequest: Q_MAIN_K2_025
- Aufgabe: `campaign_cleared` | k2_s26 | 1
- Belohnung: `hero_xp;tala` / 80
- Text: Der Nebel kam nicht mit dem Wind. Er kam, wo die Feuer schwächer wurden, und die Reichweite der Schleuderer schrumpfte. „Fernkampf braucht Sicht", sagte Olm. „Wer ihn hinten stehen lässt, verliert ihn."

### Q_MAIN_K2_027 „Gelöschte Glut"
- Prequest: Q_MAIN_K2_026
- Aufgabe: `campaign_cleared` | k2_s27 | 1
- Belohnung: `hero_xp;kiko` / 100
- Text: Ein Randfeuer war aus, als der Morgen kam. Keine Brandspur von Fremden, kein Diebstahl — nur Kälte. Kiko baute die Windsteine höher. „Sie probieren", sagte er. „Das war nicht das letzte."

### Q_MAIN_K2_028 „Die Spur des Stillen"
- Prequest: Q_MAIN_K2_027
- Aufgabe: `campaign_cleared` | k2_s28 | 1
- Belohnung: `hero_xp;brakka;res_wood` / 100;100
- Text: Der Stille prüfte die Abwehr, bevor er selbst kam: Rufer, Hasen, Füchse — alles gleichzeitig, alles nach Plan. Brakka sah es und sagte nur: „Er kommt."

### Q_MAIN_K2_029 „An der Felskante"
- Prequest: Q_MAIN_K2_028
- Aufgabe: `campaign_cleared` | k2_s29 | 1
- Belohnung: `res_stone;hero_xp;olm` / 100;80
- Text: An der Felskante gab es keinen Ort mehr, an dem er unbemerkt hätte stehen können. Er kam trotzdem, und er kam nicht allein.

### Q_MAIN_K2_030 „Der Stumme" *(Endboss: Vask)*
- Prequest: Q_MAIN_K2_029
- Aufgabe: `campaign_cleared` | k2_s30 | 1
- Belohnung: `hero_xp;tala;cur_tickets;echosplitter` / 200;1;10
- Text: Er sagte kein Wort, auch als er getroffen wurde. Er löscht reihum die drei Randfeuer, und mit jedem wird der Nebel dichter. Bei der Hälfte geht er durch den eigenen Nebel auf die hinterste Einheit. Wer hinten niemanden gelassen hat, verliert die Artillerie. Er schleppt sich davon. Und er lässt Asche-Zeichen zurück, die niemand aus dem Stamm gemalt hat.

---

### Kapitel 3: Das Jaulen im Eis (Q_MAIN_K3_031–045)

### Q_MAIN_K3_031 „Das erste Jaulen"
- Prequest: Q_MAIN_K2_030
- Aufgabe: `campaign_cleared` | k3_s31 | 1
- Belohnung: `hero_xp;brakka` / 80
- Text: Es war nicht das Heulen von Tieren, die Hunger haben. Es war eine Abstimmung. Drei Wölfe, lautlos, und die Fackeln halfen ihnen nicht mehr.

### Q_MAIN_K3_032 „Verlorene Beutel"
- Prequest: Q_MAIN_K3_031
- Aufgabe: `campaign_cleared` | k3_s32 | 1
- Belohnung: `res_food` / 150
- Text: Zwei Nächte, zwei Beutel. Der Riemen war nicht zerrissen; der Knoten war gelöst. Vierzig Schritte weiter lagen sie aufgeschlitzt, und der Wind hatte frischen Schnee darübergetrieben.

### Q_MAIN_K3_033 „Die durchgebissene Leine"
- Prequest: Q_MAIN_K3_032
- Aufgabe: `campaign_cleared` | k3_s33 | 1
- Belohnung: `hero_xp;gorm` / 80
- Text: „Das kann nicht sein", sagte Gorm. „Wir haben die ganze Nacht davorgestanden." — „Du hast in alle Richtungen geschaut", sagte Brakka. „Dann hast du überall gleich lange hingesehen."

### Q_MAIN_K3_034 „Knochenspitzen"
- Prequest: Q_MAIN_K3_033
- Aufgabe: `campaign_cleared` | k3_s34 | 1
- Belohnung: `hero_xp;olm;res_stone` / 100;100
- Text: Olm lehrte die tiefe Haltung: beide Hände am Schaft, das Ende am Oberschenkel, damit der Boden einen Teil des Stoßes trägt. Und wenn das Tier zur Seite ausweicht: Deshalb steht ihr nie allein.

### Q_MAIN_K3_035 „Die Schattenwölfin" *(Mini-Boss)*
- Prequest: Q_MAIN_K3_034
- Aufgabe: `campaign_cleared` | k3_s35 | 1
- Belohnung: `hero_xp;ruka_pre;cur_gems_free` / 120;5
- Text: Sie jagte geräuschlos und markierte das Ziel, bevor das Rudel kam. Wer den Rufenden zuerst traf, hatte Zeit. Wer auf die Welle wartete, hatte keine.

### Q_MAIN_K3_036 „Die Dunkle auf dem Grat"
- Prequest: Q_MAIN_K3_035
- Aufgabe: `campaign_cleared` | k3_s36 | 1
- Belohnung: `hero_xp;tala;cur_gems_free` / 100;5
- Text: „Eine Gestalt", sagte Tala. „Dunkel. Klein." Sie hielt die Hand auf Schulterhöhe. „Und ein Wolf. Groß, grau, mit dem Gang eines Wolfs." Kein Weiß. Kein Kult. Brakka ließ sie beobachten, statt sie zu jagen.

### Q_MAIN_K3_037 „Der Hase am Fels"
- Prequest: Q_MAIN_K3_036
- Aufgabe: `campaign_cleared` | k3_s37 | 1
- Belohnung: `hero_xp;ruka_pre;res_food` / 100;100
- Text: Auf dem flachen Asche-Felsen lag ein ausgenommener Schneehase, genau dort, wo Talas Kreis den Weg zum Wasser anzeigte. „Wir essen ihn", entschied Brakka. „Wenn jemand dafür etwas will, reden wir dann."

### Q_MAIN_K3_038 „Wo der Geruch hingeht"
- Prequest: Q_MAIN_K3_037
- Aufgabe: `campaign_cleared` | k3_s38 | 1
- Belohnung: `building_upgrade` | slot4_jagdplatz | 1
- Belohnung: `hero_xp;ruka_pre;res_wood` / 100;100
- Text: Ruka zeigte Olm, wo die Gerüste stehen mussten: „Der Wind trägt den Geruch meistens vom Feuer weg. Und der Platz liegt weit genug entfernt, dass die Spuren der Jagd nicht bis zu den Vorräten führen." Olm prüfte den Wind und baute an derselben Stelle.

### Q_MAIN_K3_039 „Erste Zusammenarbeit"
- Prequest: Q_MAIN_K3_038
- Aufgabe: `campaign_cleared` | k3_s39 | 1
- Belohnung: `hero_xp;ruka_pre;olm` / 100;100
- Text: Das Rudel testete die neue Reihe. Beim letzten Angriff standen die beiden Reihen auf, ohne dass Olm etwas gesagt hätte. Der Kampf endete, bevor Kiko bemerkte, dass die Wölfe die Senke erreicht hatten.

### Q_MAIN_K3_040 „Die Wadenbeißer-Brut" *(Mini-Boss)*
- Prequest: Q_MAIN_K3_039
- Aufgabe: `campaign_cleared` | k3_s40 | 1
- Belohnung: `hero_xp;ruka_pre;cur_tickets` / 120;1
- Text: Der Schwarm kam von beiden Flanken, viele, schwach, schnell. Einzelstöße trafen nichts. Flächenschaden traf alles. „Die Brut ist die Welle", sagte Ruka. „Wo ist die Quelle?"

### Q_MAIN_K3_041 „Rudelruf in der Ferne"
- Prequest: Q_MAIN_K3_040
- Aufgabe: `campaign_cleared` | k3_s41 | 1
- Belohnung: `hero_xp;brakka` / 80
- Text: Das Heulen klang zweistimmig. Es sammelte sich, statt zu verteilen. „Sie wählen einen Führer", sagte Ruka. „Das ist schlecht für uns. Und gut: Ein Führer ist ein Ziel."

### Q_MAIN_K3_042 „Die Umzingelung"
- Prequest: Q_MAIN_K3_041
- Aufgabe: `campaign_cleared` | k3_s42 | 1
- Belohnung: `res_food;res_wood` / 150;150
- Text: Drei Angriffsrichtungen, eine Nacht. Die Krähen nutzten die Wölfe als Deckung, die Füchse jagten im Rudel-Takt. Die Reihen hielten. Es war keine Beute mehr, die sie suchten.

### Q_MAIN_K3_043 „Kristalle im Fell"
- Prequest: Q_MAIN_K3_042
- Aufgabe: `campaign_cleared` | k3_s43 | 1
- Belohnung: `hero_xp;nara;echosplitter` / 100;5
- Text: An den Flanken der Wölfe wuchsen Kristallreihen, und die Welpen trugen sie schon an den Schultern. Nara legte die Hand an das Fell eines toten Welpen und zog sie zurück. „Es summt", sagte sie. Diesmal glaubte jemand.

### Q_MAIN_K3_044 „Vor dem Sturm"
- Prequest: Q_MAIN_K3_043
- Aufgabe: `campaign_cleared` | k3_s44 | 1
- Belohnung: `res_wood;res_stone;res_food` / 100;100;100
- Text: Letzte ruhige Nächte. Die Reihen standen doppelt, die Vorräte lagen innen, und das Heulen klang von einem Ort: oben, am Grat. Sie führen jemand. Und der jemand führt sie.

### Q_MAIN_K3_045 „Die Leitwölfin" *(Endboss: Eisfang)*
- Prequest: Q_MAIN_K3_044
- Aufgabe: `campaign_cleared` | k3_s45 | 1
- Belohnung: `hero_xp;ruka;cur_tickets;title` / 300;1;k1_rudelfreund
- Text: Sie trat nie zuerst an. Alle fünfzehn Ticks heulte sie, und an beiden Flanken erschien ein Rufer, der Wölfe nachschob. Die Rufer zuerst — sonst hört P1 nie auf. Bei der Hälfte griff sie selbst an, immer die hinterste Einheit. Am Ende trieb Ruka sie ab, statt sie zu töten. „Sieben Winter verrückt", sagte Brakka. „Zu satt zum Denken", sagte Ruka. Beide behalten recht und bleiben.

---

## Teil B — Sidequests (6 Ketten, 18 Quests, an die neuen Stufen angedockt)

### Kette: Kiko, der Feuerwächter (wie v2, angepasst)
- Q_SIDE_B1_101 „Der Mann, der sich nicht ablösen lässt" – Prequest: Q_MAIN_K1_001 – Aufgabe: `login_days` / 3
- Q_SIDE_B1_102 „Der Rauch legt sich" – Prequest: _101 – Aufgabe: `nights_survived` / 5
- Q_SIDE_B1_103 „Drei Windsteine" – Prequest: _102 – Aufgabe: `building_upgrade` slot1_feuerstelle / 2

### Kette: Bako, der Baumeister (wie v2)
- Q_SIDE_B1_111 „Nasse Felle" – Prequest: Q_MAIN_K1_003 – Aufgabe: `collect_resource` res_wood / 300
- Q_SIDE_B1_112 „Eine Kuhle zur Probe" – Prequest: _111 – Aufgabe: `building_upgrade` slot3_wohnraum / 1
- Q_SIDE_B1_113 „Drei übrig" – Prequest: _112 – Aufgabe: `building_level` slot3_wohnraum / 3

### Kette: Talas Zeichen (an die neuen Stufen gedockt)
- Q_SIDE_B1_121 „Elf Zeichen" – Prequest: Q_MAIN_K1_006 (Der Kreis am Fels) – Aufgabe: `read_marker` any / 5
- Q_SIDE_B1_122 „Kikos Warnung" – Prequest: _121 – Aufgabe: `read_marker` b1_zeichen_gefahr / 1
- Q_SIDE_B1_123 „Ein fremder Kreis" – Prequest: _122 UND Q_MAIN_K2_022 (Zeichen im Schnee) – Aufgabe: `visit_landmark` b1_zeichenfels / 1

### Kette: Hulf und die Speere (an Olms Reihe gedockt)
- Q_SIDE_B1_131 „Der gebrochene Schaft" – Prequest: Q_MAIN_K1_003 – Aufgabe: `train_units` speertraeger / 5
- Q_SIDE_B1_132 „Beide Hände, tief gehalten" – Prequest: _131 UND Q_MAIN_K3_034 (Knochenspitzen) – Aufgabe: `campaign_play` any / 3
- Q_SIDE_B1_133 „Wieder eingesetzt" – Prequest: _132 – Aufgabe: `building_upgrade` slot4_jagdplatz / 1

### Kette: Gorm am Pfosten (neu, aus K1/K3-Zwischenmomenten)
- Q_SIDE_B1_141 „Alle Richtungen, gleich lange" – Prequest: Q_MAIN_K1_008 – Aufgabe: `campaign_play` any / 5
- Q_SIDE_B1_142 „Die falsche Richtung" – Prequest: _141 UND Q_MAIN_K3_033 – Aufgabe: `formation_active` any / 1
- Q_SIDE_B1_143 „Der Pfosten hält" – Prequest: _142 – Aufgabe: `campaign_win_stars` any / 2

### Kette: Asch (neu, zu Rukas Ankunft)
- Q_SIDE_B1_151 „Der Wolf, der den Plan kennt" – Prequest: Q_MAIN_K3_036 – Aufgabe: `hero_bond_level` ruka / 1
- Q_SIDE_B1_152 „Zwei Schritte hinter ihr" – Prequest: _151 UND Q_MAIN_K3_039 – Aufgabe: `campaign_cleared` any / 3
- Q_SIDE_B1_153 „Die kahle Narbe" – Prequest: _152 UND Q_MAIN_K3_045 – Aufgabe: `hero_bond_level` ruka / 3

---

## Teil C — Baukunst (Slot-Quests, 9 Einleitungen + 6 Ausbauten)

### Einleitungen (Neubau, wie v2 — an neue Prequests gedockt)
- Q_BAU_001 „Winzige Feuerstelle" – Prequest: – – `building_level` slot1_feuerstelle / 1
- Q_BAU_002 „Reisig-Halde" – Prequest: – – `building_level` slot2_sammler / 1
- Q_BAU_003 „Schlafkuhlen" – Prequest: Q_BAU_001 – `building_level` slot3_wohnraum / 1 *(K2-Freischaltung: Slot 3 öffnet in E2)*
- Q_BAU_004 „Der Zeichenfels" – Prequest: Q_MAIN_K1_006 – `building_level` slot13_zeichenfels / 1
- Q_BAU_005 „Der Jagdplatz" – Prequest: Q_MAIN_K3_038 – `building_level` slot4_jagdplatz / 1 *(E3-Freischaltung, Rukas Windregel)*
- Q_BAU_006 „Der Werkplatz" – Prequest: Q_MAIN_K3_039 – `building_level` slot5_werkplatz / 1
- Q_BAU_007 „Der Asche-Totem" – Prequest: [E4+] *(öffnet nach der Epoche, Platzhalter)*
- Q_BAU_008 „Der Wall" – Prequest: [E4+] *(Platzhalter)*
- Q_BAU_009 „Die Kaserne" – Prequest: [E4+] *(Platzhalter)*

### Ausbauten (Stufe 2, wie v2.1)
- Q_BAU_011 „Feuer, das heller ruft" – slot1_feuerstelle St. 2 – Prequest: Q_BAU_001
- Q_BAU_012 „Die Halde trägt" – slot2_sammler St. 2 – Prequest: Q_BAU_002
- Q_BAU_013 „Kuhlen für drei" – slot3_wohnraum St. 2 – Prequest: Q_BAU_003
- Q_BAU_014 „Zeichen, die antworten" – slot13_zeichenfels St. 2 – Prequest: Q_BAU_004
- Q_BAU_015 „Der Platz, an dem gejagt wird" – slot4_jagdplatz St. 2 – Prequest: Q_BAU_005
- Q_BAU_016 „Werkzeug, das hält" – slot5_werkplatz St. 2 – Prequest: Q_BAU_006

---

## Teil D — Helden-Quests (8 Startquests, wie v2 — Prequests aktualisiert)

- Q_HERO_BRAKKA „Die, die zählt" – Prequest: – – `nights_survived` no_hunger / 2
- Q_HERO_NARA „Zweimal kam etwas" – Prequest: – – `hero_bond_level` nara / 2
- Q_HERO_KIKO „Feuerwache" – Prequest: Q_SIDE_B1_101 – `collect_action` any / 50
- Q_HERO_TALA „Die Stelle unter dem Westfeld" – Prequest: Q_MAIN_K2_021 – `visit_landmark` b1_westfeld / 1
- Q_HERO_RUKA „Asch" – Prequest: Q_MAIN_K3_037 – `hero_bond_level` ruka / 2
- Q_HERO_OLM „Die Reihe hält" – Prequest: Q_MAIN_K1_003 – `formation_win_types` – / 2
- Q_HERO_BAKO „Dreißig und drei" – Prequest: Q_SIDE_B1_113 – `building_all_min_level` epoch_1 / 2
- Q_HERO_MIRA „Die ohne Waffe" – [E4+ Platzhalter — Miras Debüt ist der Grauvater]

---

## Zusammenfassung

| Typ | Anzahl |
|---|---|
| Hauptquest (45 Stufen) | 45 |
| Sidequests (6 Ketten à 3) | 18 |
| Baukunst (9 Einleitungen + 6 Ausbauten) | 15 |
| Helden-Quests (6 scharf + 2 Platzhalter) | 8 |
| **Gesamt Epoche 1, Kapitel 1–3** | **86** |

**Offene Punkte für Fabian:**
1. Kampagnen-Level-IDs: Ich habe `k1_s1`–`k3_s45` als Platzhalter verwendet — die echten `e1_camp_NN`-IDs müssen zugeordnet werden (45 Stufen = Neubau der Kampagne, die jetzige hat 30 Level). Bedeutet: Kampagne von 30 auf 45 Level erweitern? Das ist ein Daten-Umbau in campaign_levels.csv/campaign_waves.csv.
2. Sidequest-Parallelität: 3 gleichzeitig (v1) oder 1 pro Kette?
3. Q_BAU_007–009 (Totem, Wall, Kaserne) gehören laut Lore in E5–E7 — sie bleiben Platzhalter, bis wir diese Kapitel questen.
