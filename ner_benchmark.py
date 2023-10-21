import argparse
from flair.data import Sentence
from flair.models import SequenceTagger
import flair, torch
import time


if __name__ == "__main__":
    if torch.cuda.is_available():
        print("CUDA is available!")
        torch.device("cuda")
    else:
        print("CUDA is not available. Using CPU...")
        torch.device("cpu")

    text = """
@rive. ni};IEEEEET @rivm. ni]

Received: Thur 8/6/2020 9:40:44 AM

Ja doe ik. Ik had dit al zo gelezen
*

ero: INENECIN SEEN ovr.

Sent: donderdag 6 augustus 2020 11:40

To: 5.1.2e 4 5.1.2¢ @rivm.nl>

ce SER RES >; IEEE EE o>

Subject: RE: Dutch Science Board COVID-19 vaccines

Wil je een boeking maken voor wat betreft de 2020 kosten? Budget vanuit calamiteiten budget via de 80655. Het

2021 deel komt uit het covid-19 programma.

wo

From: CEE EEN© v.01>
Sent: donderdag 6 augustus 2020 11:29

@rivm.nl>

@rivm.nl>

Subject: RE: Dutch Science Board COVID-19 vaccines

De kosten voor 2020 moeten van het cb, de kosten voor 2021 moet van het nieuwe p19 af.

van: EEE vn.
Datum: 6 augustus 2020 om 10:33:10 CEST
Drivm.nl>

@rivm.nl>,

[EE rivn.nl>

Onderwerp: RE: Dutch Science Board COVID-19 vaccines

o-JEN
Ik heb nog niet helemaal scherp of er nu separaat budget beschikbaar wordt gesteld of dat er budget vanuit het

Calamiteitenbudget moet komen. Kun jij antwoorden wat de bedoeling is? Wellicht heb ik niet goed gelezen?

Sent: dinsdag 4 augustus 2020 21:37

q 5.1.2e @rivm.nl>

Subject: RE: Dutch Science Board COVID-19 vaccines

|
Helder en prima om hier een aparte opdracht voor te maken.

EEjij een additionele opdracht aanmaken (projectsoort 02)? Daarin kan de berekening worden

toegevoegd en inhoudelijke tekst. Als je hulp nodig hebt om de financién te vullen laat mij weten dan doe ik dit wel

even. Dan de offerte draaien zodat deze ingediend kan worden voor akkoord.

5318



oly
moet dan budget worden overgeboekt van het calamiteitenbudget naar de nieuwe opdracht kan ik ook

doen akkoord? En tevens in het COVID-19 overzicht toevoegen

Sent: dinsdag 4 augustus 2020 21:12

@rivm.nl>

@rivm.nl>; < rivm.nl>

Subject: RE: Dutch Science Board COVID-19 vaccines

Geen excel, maar wel een berekening:

Interne experts: 6 x 27 (weken in 2020)

‘TEEInterne experts : 6 x 25 (weken in 2021) x

Vacatiegelden/onkosten externe experts: 4 x 8EE
totaal: |
Totaal 2020

5.1.2b
b Dit zou dan van het CB af gaan

Totaal 2021
-

b Dit zou van nieuwe P19 moeten komen

De reden dat] dit toch apart wil hebben is de status aparte van deze adviesraad. Belangrijk om ze expliciet te

benoemen, ook wat hun mandaat is en aan welke kaders ze zich moeten houden, maar qua kosten kan het dus wel

van CB af.

VWS heeft een concept opdrachtbrief liggen, wij kunnen daarop een offerte indienen en zij kunnen dan een akkoord

geven op het inrichten van deze adviesraad en dat de kosten van het CB af mogen. Is dat akkoord? Of zien jullie
het anders?

Dank voor het meedenken alvast!

Verzonden: dinsdag 4 augustus 2020 16:55

Aan: 5.1.2e rivm.nl>

AA... CE ECEciv >
Onderwerp: FW: Dutch Science Board COVID-19 vaccines

Onderstaande mail krijg ik van |EEESIhaar heb jij voor mij (en EEE] de Excel met daarin het budget.
We moeten even kijken of er een aparte opdracht voor moet worden gemaakt en/of dit als oblige in het

calamiteitenbudget wordt verwerkt.

Dank je wel alvast.

srost- [EAE
From: 5 5.1.2e <| rivm.nl>

Sent: dinsdag 4 augustus 2020 16:42

Subject: FW: Dutch Science Board COVID-19 vaccines

5318



Hartelijke groet,

Programma’s I&V& DVP | Control & Advies | RIVM |
@rivm.nl | www.rivm.nl

Werkdagen:

uiiirr—...a2

Verzonden: maandag 3 augustus 2020 18:58

Aan: rivm.nl>

Onderwerp: RE: Dutch Science Board COVID-19 vaccines

IEE
Wacht nog maar even alsje wilt, ik begreep net dat het misschien van het calamiteiten budget af moet ipv additioneel.

lk weet morgen meer!

Groeten

van:
ECE EEi. >

Datum: 3 augustus 2020 om 17:44:08 CEST

Onderwerp: RE: Dutch Science Board COVID-19 vaccines

Kan ik vast een nummer aanmaken in SAP.

Dan kan BEY =r het plan van aanpak en haar financiéle planning invullen.

Hartelijke groet,

5 5.1.2e

| RIVM |
@rivm.nl | www.rivm.nl

Werkdagen:

ECE+8 EE
Verzonden: maandag 3 augustus 2020 11:07

5.1.2¢ 5.1.2e ®rivm.nl>

@ rive ni; [EE rivm.nl>

Onderwerp: FW: Dutch Science Board COVID-19 vaccines

Ik heb op basis van de opdrachtbrief (die ik naar ik meen nog in concept is) een format voor een additionele offerte

ingevuld. Er moet uiteraard nog een budget aan worden toegevoegd, maar deze is in de opdrachtbrief ook nog niet

duidelijk, en ik begrijp dat jij daar mee bezig bent. Ook is de start van de looptijd nog niet helder, misschien kan je
dat aanvullen.

5318



5318

Als jij het hebt aangevuld, kunnen we het eventueel laagdrempelig nog even naar VWS sturen om af te stemmen

en dan kan het hier het systeem in, en vervolgens met aanbiedingsbrief naar VWS verzonden worden.

Groeten JETS

RIVM - Centrum Infectiezie| strijding (Clb)
Postbus 1 (interne postbak

hoyven3720 BA

Mob: OGRE

www rivm.nl/infectieziekten

Verzonden: vrijdag 31 juli 2020 13:01

Aan: JIE vn.
Onderwerp: FW: Dutch Science Board COVID-19 vaccines

Ha

Wil je BPLE begeleiden bij het maken van een (zo beknopt mogelijke) offerte aan VWS voor onderstaande. Ik heb

APM gevraagd alvast een kostenraming te maken voor inzet rivmers en experts. Voor vergoeding experts heb ik

aar aangeraden de richtlijnen van OMT aan te houden.

Met vriendelijke groet
5.1.2e

aanwe zig Fl} ti].

r.030- oe|
E: rivm.nl

Centrum Infectieziektebestrijding (Clb) | Rijksinstituut voor Volksgezondheid en Milieu (RIVM)

Antonie v. Leeuwenhoeklaan 9 | Postbus 1 | 3720 BA | Bilthoven
rivm.nl>

: vrijdag 31 juli 2020 10:34

G rivm.nl>; [IEEE rivm.nl>

Onderwerp: FW: Dutch Science Board COVID-19 vaccines

IE
Heb jij (vandaag) tijd voor kort overleg over het volgende:
VWS heeft bijgaande opdrachtbriefaan RIVM opgesteld met als opdracht een expertgroep in te richten ten behoeve

van de advisering van het onderhandelingsteam mbt de wetenschappelijke kant van COVID-19 vaccin kandidaten.

Feitelijk hebben we al zo'n expertgroep gevormd met RIVM-ers als leads (zie excel) en adviseren we ook al een

aantal weken, maar er is nog geen formeel kader.



5318

Wat nog ontbreekt is een budget, voor vacatiekosten en reiskosten, dus dat heb ik nog als wijziging voorgesteld
voor de opdrachtbrief.

EEE] vroeg me om dat met jou af te stemmen.

Zou jij een budget willen opstellen/inrichten? Vanuit RIVM A ik in de groep, en maken hier best

wat uren voor. Wellicht komt daar nog een derde RIVM-er bij (| ) ivm een opengevallen plek voor

expertise vanuit toelatingseisen. Het budget zou dan ook interne uren kunnen vergoeden.

Ik wil vandaag naar VWS laten weten of de brief met toevoeging okay is.

Zou fijn zijn als we even contact hebben.

Groet,

5.1.2e

5.1.2e

"Centre for Immunology of Infectious Diseases and Vaccines | National Institute for Public Health and the Environment (RIVM) | Antonie van Leeuwenhoeklaan 9 [PO
boEER 3720 BA BILTHOVEN | The Netherlands

ZInfectious Diseases & Immunology | Dept. Biomolecular Health Sciences | Faculty of Veterinary Medicine | Utrecht University | Yalelaan 1 | PO vox RES 3508 TD

UTRECHT| The Netherlands

T. +31 v1(EE= ERE civil

rrom: [IEE< rivm.nl>

Sent: vrijdag 31 juli 2020 09:45

Subject: RE: Dutch Science Board COVID-19 vaccines

Is OK. Meestal schrijft VWS de opdrachtbrief zelf. Moet er nog iets over budget bij? mvrcr EEE

Sent: woensdag 29 juli 2020 06:21
rivm.nl>

Subject: FW: Dutch Science Board COVID-19 vaccines

Beste

Een procedureel advies gevraagd over het volgende:
Zoals je weet adviseren en ik VWS ten behoeve van gaande EU onderhandelingen over kansrijke COVID-

19 kandidaat-vaccins. Het gaat om wetenschappelijke, onafhankelijke duiding van de veiligheid, werkzaamheid,

toediening en beschikbaarheid van gevorderde COVID-19 kandidaat-vaccins. Om voldoende kennis en slagkracht te

hebben hebben we inmiddels een panel van experts gevormd, ook van buiten het RIVM (zie excel lijst).
Het is zaak om dit panel nu zo snel mogelijk te formaliseren met een taakomschrijving en het ondertekenen van

een onafhankelijkheids/integriteits verklaring, zodat leden zelfstandig kunnen opereren.

Nu komt het voorstel van VWS om dit via een opdracht aan het RIVMEE laten lopen.
Is dit logisch? Ik had zelf verwacht (voorgesteld) dat dit rechtsreeks vanuit VWS kon worden geregeld, maar is het

vanuit VWS met het oog op de te borgen onafhankelijkheid en expertise van het panel juist beter om deze opdracht
uit te zetten bij het RIVM?

Graag je advies.

Groet, EE (0SEE

NB: indien de route via RIVM de beste is, dan zal bijgaande concept opdrachtbrief (bijlage) vanuit de directie

Volksgezondheid naar worden gestuurd.
NB2. Indien de route via RIVM de beste is, dan zal er daarna vanuit RIVM een soort benoemingsbrief naar de leden

moeten worden opgesteld, verwijzend naar de opdracht en naar de te ondertekenen declaration-of-absence-of-

conflict-of-interests verbonden aan de EU onderhandelingen (bijlage). Deze onafhankelijkheidsverklaring kan ik, ivm

de urgentie nu, ook alvast uitzetten bij de leden...

NB3. Indien de route via RIVM de beste is, dan RIVM ook formeel verantwoordelijk zijn voor de expertise in het

panel en daar kunnen cok weer vragen over komen....



"Centre for Immunology of Infectious Diseases and Vaccines | National Institute for Public Health and the Environment (RIVM) | Antonie van Leeuwenhoeklaan 9 |PO

boxEE 3720 BA BILTHOVEN | The Netherlands

?Infectious Diseases & Immunology | Dept. Biomolecular Health Sciences | Faculty of Veterinary Medicine | Utrecht University | Yalelaan 1| PO box [RIE] 3508 TD

UTRECHT| The Netherlands

From: [IEE minvws.nl>

Sent: dinsdag 28 juli 2020 16:32

To: 5.1.2e <BR Bl Drivm.nl>

Subject: FW: Dutch Scientific Committee COVID-19 vaccines

Beste | EEN
Bij afwezigheid var [ERED

ik nu deze opdrachtbrief verder op. Naar aanleiding van jouw commentaar heb ik een eerste

aanzet van de brief aangepast. In de bijlage vind je de concept-opdracht. Ik hoor graag van je of deze brief past bij je

verwachtingen en of dit voldoende handvatten biedt voor het adviespanel. Ik wil je daarbij vragen of naast eventuele

opmerkingen ook specifieke tekstvoorstellen te doen, dan kunnen we er met elkaar voor zorgen dat we snel kunnen handelen en

de brief op korte termijn verzonden kan worden.

Als bijlage vind je tevens een integriteit/onafhankelijkheidsverklaring die ook wordt gebruikt voor de deelnemers aan het INT

(Joint Negotiation Team). De Nederlandse collega’s die vanuit VWS betrokken zijn hebben ook deze verklaring getekend. Deze

verklaring zouden we ook kunnen gebruiken voor experts van het panel, daar hun werk in het verlengde ligt van het INT. Mocht

je nog ideeén hebben over andere mogelijke verklaring(en), horen we het graag.

Groet,

n ingien Infectieziekten

Directie Publieke Gezondheid

Min VWS

Verzonden: woensdag 22 juli 2020 19:58

aminvws.nt>; [ERE minvws.nl>

@rivm.nl>

Onderwerp: Dutch Scientific Committee COVID-19 vaccines

De activiteiten voor de ‘expert/klankbord groep COVID-19 vaccins’ deze week waren leuk en leerzaam voor mij,
vooral omdat doel en context wat concreter werden. Ik deel even mijn ‘evaluatie’ omdat de expert-groep nog niet

goed aan de slag kan, mijns inziens.

Het wetenschappelijk advies aan de overheid over COVID-19 vaccins begon bij het RIVM met het bijhouden en

samenvatten van ontwikkelingen in het vaccin landschap inclusief het in meer detail beschrijven van de meest

geavanceerde/ kansrijke producten. Daarnaast werden een paar productpresentaties bijgewoond, die vanuit VWS

waren georganiseerd. Meeting verslagen en stukken voor VWS en het alliantie-team waren tot nu toe in het

Nederlands. Voor een bredere wetenschappelijke basis voor de adviezen maar ook om een werkverdeling te kunnen

maken is vorige week de expert/klankbord groep opgericht. Inmiddels bestaat die uit 7 cen EEEheeft zich gisteren aangesloten (bijl).

uidelijk dat we nog niet de juiste slagkracht hebben om eigen bevindingen internationaal paraat te hebben. Ook

ontbreekt het ons nog aan mandaat om vertrouwelijke gegevens onderling uit te kunnen wisselen.

CBRPCN on ik vandaag tot de conclusie dat dit snel verholpen zou moeten worden. Ook wees vanuit

eerdere ervaringen op het belang van een goed kader voor wetenschappelijke adviezen ten behoeve van vaccins

bij een pandemische situatie. Het zou goed zijn om een transparante procedure te hebben en een goede borging
van onafhankelijkheid (van industrie en overheid) en integriteit van de commissie [JE{ERPrees er verder op dat

niet onderschat moet worden dat, om resultaten van producten onderling te kunnen vergelijken, centrale

testplatforms nodig zijn om samples uit meerdere studies te testen, onafhankelijk van partijen. Er zijn wel

internationale initiatieven op dit gebied en het verdient aanbeveling iemand in de commissie te hebben met kennis

van dit internationale speelveld. JERE bereid om hier input over te geven.

5318



5318

Mijn conclusie is daarom dat we behoefte hebben, vanuit (het) ministerie(s), aan:

« een opdrachtbrief (liefst in het Engels) aan de ‘Dutch Scientific Committee COVID-19 vaccines’, met formele

kaders ten aanzien van de precieze opdracht en bijbehorende verantwoordelijkheden, bevoegdheden en

onafhankelijkheid/integriteit. De opdracht zou op grote lijnen kunnen beschrijven waarop producten in de

pijplijn wetenschappelijk geevalueerd dienen te worden ten behoeve van adviezen (bijv. eigenschappen van

belang voor veiligheid, werkzaamheid, toediening en beshikbaarheid van vaccins), en welke bronnen de

Committee ter beschikking staan (bijv. gepubliceerde wetenschappelijke bronnen, wetenschappelijk

gecontroleerde overzichtssites zoals die van de WHO, ECDC, KNVM etc, via VWS verkregen vertrouwelijke

gegevens van derden, door de commissie actief zelf ingewonnen vertrouwelijke informatie, etc).
+ een geheimhoudingsverklaring customized voor commissieleden, voor het (doorlopend) vertrouwelijk
uitwisselen van informatie in het kader van de opdracht, nationaal maar ook internationaal verkregen bijv. via

lidstaten en afkomstig van andere scientific committees voor COVID-19 vaccins

* een integriteitsverklaring customized voor commissieleden

« een Engelstalige template non-disclosure agreement voor het vertrouwelijk uitwisselen van product

gegevens en data tussen individuele partijen en de Dutch Scientific Committee COVID-19 Vaccines

Gezien het internationale speelveld zou de Dutch Scientific Committee COVID-19 vaccines verslagen, evaluaties,

updates naar VWS etc in het Engels willen opstellen.

Tot zover mijn analyse.
Ik ben benieuwd hoe jullie eea zien en hoe het ministerie de commissie verder kan formaliseren en operationeel
maken.

Misschien kunnen we morgen telefonisch overleggen en dan met die informatie de commissie updaten over de

stand van zaken; commissie samenstelling, procedurele acties die ondernomen gaan worden, recente en

toekomstige inhoudelijke acties, etc.

Hartelijke groet,

"Centre for Immunology of Infectious Diseases and Vaccines | National Institute for Public Health and the Environment (RIVM) | Antonie van Leeuwenhoeklaan 9 |PO

box§B 3720 BA BILTHOVEN | The Netherlands

?Infectious Diseases & Immunology | Dept. Biomolecular Health Sciences | Faculty of Veterinary Medicine | Utrecht University | Yalelaan 1] PO FX 5.1.22 | 3508TD
UTRECHT | The Netherlands

Te +31 (03(EET M: +31 oiEEN e: IEEE @rivnnl

Sent: woensdag 15 juli 2020 09:38
rivm.nl>; A. erasmusme.nl>; @cbg-meb.nl'
. g.nl>; @lumc.nl'

aminvws.n>;[EKER minyws.nl>

Subject: expert/klankboard groep COVID-19 vaccin ontwikkeling

Beste allemaal,

Ik heb met ieder van jullie contact gehad met de vraag of jullie onderdeel zouden willen zijn van een

expert/klankboard groep voor het voor VWS beantwoorden van wetenschappelijke vragen en het duiden van

gegevens die beschikbaar komen van de verschillende COVID-19 vaccins in ontwikkeling. Heel fijn dat jullie
allemaal mee willen werken.

De bedceling is dat ik een whatsapp groep aanmaak, waar ik op het moment dat er iets van ons gevraagd wordt

kan aankondigen dat er een verzoek vanuit VWS is, viaFre) met de vraag wie er op dat moment tijd heeft

en de juiste expertise om het verzoek op te pakken. Vervolgens zal ik per mail aan deze mensen, meestal zal 2

ersonen genoeg zijn, het verzoek om input doorsturen. Het zal over het algemeen gaan om een snelle duiding.

ee]staat in de cc en komt ook in de whatsapp groep maar communicatie van hem gaat via mij|
als ik er niet ben.



Daarnaast willen we een set aan inhoudelijke criteria opstellen waar een COVID-19 vaccin minimaal aan zou moeten

voldoen en welke data zouden we graag willen zien. Zou fijn zijn als jullie hier ideeen over hebben om die met

elkaar te delen en te kijken of we tot een gezamenlijke lijst kunnen komen die we bij een mogelijke deal kunnen

gebruiken.

Hierbij tevens de contact gegevens van jullie allemaal zodat jullie indien nodig ook onderling contact kunnen leggen.
Laten we het zo proberen en kijken hoe het gaat. Mochten er nog vragen of suggesties zijn dan hoor ik het graag.

Ik ben van 16 juli t/m 10 augustus met vakantie, in deze periode is eerste aanspreek punt.

Naam Email adres Telefoonnr. Organisatie
rivm.nl RIVM/ universiteit

Utrecht

EE

BEE ecrasmusmenl Erasmus MC

5.1.20
|

IEEE © cbs meb ni e

[sie JL oe [CERN [O[F  510c Universiteit Groningen

EE© ncn |ORE | UMC Leiden
EEN |EEENenn

CBG

RIVM

Met vriendelijke groet/kind regards
51.2e

[sie
Centre for Immunology of Infectious diseases and Vaccines

RIVM, Centre for Infectious Disease Control (Cib)
PO BoxgIE3720 AL Bilthoven, The Netherlands

IEEvr.

Dit bericht kan informatie bevatten die niet voor u is bested. Indien u niet de geadresseerde bent of dit bericht abusievelijk aan u is verzonden, wordt u

verzocht dat aan de afzender te melden en het bericht te verwijderen. Het RIVM aanvaardt geen aansprakelijkheid voor schade, van welke aard ook, die

verband houdt met risico's verbonden aan het elektronisch verzenden van berichten.
www.rivim.nl De zorg voor morgen begint vandaag

This message may contain information that is not intended for you. If you are not the addressee or if this message was sent to you by mistake, you are

requested to inform the sender and delete the message. RIVM accepts no liability for damage of any kind resulting from the risks inherent in the electronic

transmission of messages.
www.rivm.nl/en Committed to health and sustainability

5318
"""

    sentence = Sentence(text)
    tagger = SequenceTagger.load("flair/ner-dutch-large")

    start_time = time.time()
    tagger.predict(sentence)
    end_time = time.time()

    keywords = {}
    for entity in sentence.get_spans("ner"):
        if entity.score > 0.9:
            if entity.text in keywords:
                keywords[entity.text]["count"] += 1
            else:
                keywords[entity.text] = {
                    "count": 1,
                    "tag": entity.tag,
                    "labels": entity.labels,
                }

    print(keywords)

    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.6f} seconds")
