LEAGUES = [
    ("serie-a", "IT1"), # Italian
    ("premier-league", "GB1"), # English
    ("la-liga", "ES1"), # Spanish
    ("bundesliga", "L1"), # German
    ("ligue-1", "FR1"), # French
    ("eredivisie", "NL1"), # Dutch
    ("liga-portugal", "PO1"), # Portuguese
    ("jupiler-pro-league", "BE1"), # Belgian
    ("super-lig", "TR1"), # Turkish
    ("fortuna-liga", "TS1"), # Czech
    ("super-league-1", "GR1"), # Greek
    ("eliteserien", "NO1"), # Norwegian
    ("ekstraklasa", "PL1"), # Polish
    ("superliga", "DK1"), # Danish
    ("bundesliga", "A1"), # Austrian
    ("super-league", "C1"), # Swiss

    ("major-league-soccer", "MLS1"), # American
    ("liga-mx-apertura", "MEXA"), # Mexican

    ("campeonato-brasileiro-serie-a", "BRA1"), # Brazilian
    ("torneo-apertura", "ARG1"), # Argentinian

    ("chinese-super-league", "CSL"), # Chinese
    ("j1-league", "JAP1"), # Japanese
    ("saudi-pro-league", "SA1"), # Saudi
]

URL = f"https://www.transfermarkt.pl/{LEAGUES[0][0]}/einnahmenausgaben/wettbewerb/{LEAGUES[0][1]}"

if __name__ == "__main__":
    for league in LEAGUES:
        print(f"https://www.transfermarkt.pl/{league[0]}/einnahmenausgaben/wettbewerb/{league[1]}")
