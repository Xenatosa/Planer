# Bericht · BAU-MENÜ D2 v1

**Status: DONE · 24.10.2026**

## Ausgabe

- vorschau_menu_bau_d2_v1.png — Übersicht mit Kategorie-Reitern und vier Wirtschaftskarten
- vorschau_menu_bau_d2_v1_detail.png — Detail-Sheet Waldhütte
- _src/menu_bau_d2_v1.html — Layout und Komponenten
- _src/render_vorschau_menu_bau_d2_v1.py — Renderer für beide Ansichten

Beide Vorschauen sind 1080×1920 px.

## Gestaltung und Inhalt

- Obsidian-&-Glut-Palette, Lilita One und Baloo 2, abgeleitet aus den freigegebenen Ressourcen-, Inventar- und Mail-Fenstern.
- Durchscheinender Scrim über den gesamten Screen einschließlich Ressourcen-HUD und Dock A; darüber ein fast bildschirmbreites Bau-Panel.
- Vier sichtbare Kategorien (Wirtschaft, Militär, Forschung, Deko) plus **+** zum Erweitern.
- Vier große Karten ohne Scrollen in der ersten Ansicht. Jede zeigt Gebäudebild, Name, Stufe, Holz-, Stein-, Nahrungs- und Muschelkosten sowie Bauzeit.
- Zustände: **BAUBAR**, **ZU WENIG RESSOURCEN** mit roten Fehlbeträgen, **Benötigt Rathaus Stufe 3** und **Bauplätze 2/3**.
- Bauschlange: Baumeister **1/2 belegt** mit **08:42** Restzeit und ein freier zweiter Baumeister.
- Detailsheet mit großem Gebäude, Beschreibung, Holzproduktion und Lagerkapazität **jetzt → nächste Stufe**, Kosten, Bauzeit, **BAUEN** und **SOFORT · 50 ZEITKRISTALLE**.
- Gold-Icon und Baukostenbezeichnung verwenden Muscheln.

## Gebäude-Assets

Der Gebäudeordner enthielt in diesem Checkout keine Bilddateien. Die vier für die Vorschau benötigten transparenten Gebäudeillustrationen wurden daher neu erstellt und ausschließlich unter team/art/gebaeude_neu_b/ abgelegt. Sie orientieren sich an der dort beschriebenen Variante B und sind als Vorschau-Konzeptgrafiken gekennzeichnet, nicht als separat freigegebene Produktionsgrafiken. Für die Screens werden keine Grafiken aus _alt/gebaeude_* verwendet.

Werkzeug: eingebautes ImageGen. Prompt-Set: vier einzelne transparente 3D-Gebäudeillustrationen — Waldhütte mit Sägewerk und Holzstapeln, Steinbruch mit Kran und Stolleneingang, Bauernhof mit Getreidespeicher und Weizengarben, Fischerhütte mit Netzen und Körben. Für alle: vollständig sichtbares Gebäude, warme natürliche Materialien, keine Umgebung, kein Boden und kein Text. Die drei anfangs mit Schachbretthintergrund gelieferten Bilder wurden per ImageGen-Hintergrundfreistellung in PNGs mit Alphakanal überführt.

## Sichtprüfung

- Beide PNGs nach dem Rendern visuell geprüft.
- Schrift und Zahlen sind in 1080×1920 lesbar; Kostenstatus und Sperrhinweis sind eindeutig.
- Keine abgeschnittenen Karten oder Bedienelemente, keine gespiegelten Bilder und keine leeren Inhaltszonen.
- Die erste Ansicht zeigt alle vier Gebäudekarten und die Bauschlange ohne Scrollen.
- Keine Testtexte in den Vorschauen.
