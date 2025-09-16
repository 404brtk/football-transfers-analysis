import requests
from bs4 import BeautifulSoup
import pandas as pd
import logging
from pathlib import Path
from typing import Optional


class TransfermarktScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
        })
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    LEAGUES = [
        ("premier-league", "GB1"), # English
        ("serie-a", "IT1"), # Italian
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

    def fetch_league_data(self, league_name: str, league_id: str) -> Optional[pd.DataFrame]:
        url = f"https://www.transfermarkt.com/{league_name}/einnahmenausgaben/wettbewerb/{league_id}"

        try:
            self.logger.info(f"Fetching data for {league_name} ({league_id})")
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', class_='items')
            
            if not table:
                self.logger.warning(f"No table found for {league_name}")
                return None
            
            return self._parse_table(table, league_name)
            
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch data for {league_name}: {e}")
            return None
        except Exception as e:
            self.logger.error(f"Error parsing data for {league_name}: {e}")
            return None
    
    def _parse_table(self, table, league_name: str) -> pd.DataFrame:
        data = []
        column_headers = []

        header_row = table.find('thead')
        if header_row:
            headers = header_row.find_all('th')
            # skip first 2 columns (*#* and some empty *Club* column)
            for th in headers[2:]:
                column_headers.append(th.get_text(strip=True))
        column_headers.append("League")

        tbody = table.find('tbody')
        if tbody:
            for row in tbody.find_all('tr'):
                cells = row.find_all(['td', 'th'])
                # skipping first 2 columns
                row_data = [cell.get_text(strip=True) for cell in cells[2:]]
                row_data.append(league_name)
                data.append(row_data)
        
        if not data:
            self.logger.warning(f"No data rows found for {league_name}")
            return pd.DataFrame()
        
        return pd.DataFrame(data, columns=column_headers)
    
    def scrape_all_leagues(self) -> pd.DataFrame:
        all_data = []
        league_name_counts = {}
        
        for league_name, league_id in self.LEAGUES:
            league_name_counts[league_name] = league_name_counts.get(league_name, 0) + 1
        
        league_name_seen = {}
        for league_name, league_id in self.LEAGUES:
            df = self.fetch_league_data(league_name, league_id)
            
            if df is not None and not df.empty:
                # if this league name appears multiple times and we've seen it before, add suffix
                if league_name_counts[league_name] > 1 and league_name in league_name_seen:
                    # update the League column to add the suffix
                    df['League'] = f"{league_name}-{league_id}"
                
                # mark this league name as seen
                league_name_seen[league_name] = True
                
                all_data.append(df)
                self.logger.info(f"Successfully scraped {len(df)} rows for {league_name}")
        
        if not all_data:
            self.logger.error("No data was successfully scraped")
            return pd.DataFrame()
        
        combined_df = pd.concat(all_data, ignore_index=True)
        self.logger.info(f"Combined data: {len(combined_df)} total rows from {len(all_data)} leagues")
        return combined_df
    
    def save_data(self, df: pd.DataFrame, filename: str = "transfermarkt_data") -> None:
        if df.empty:
            self.logger.error("No data to save")
            return
        
        output_path = Path(f"{filename}.csv")
        
        try:
            df.to_csv(output_path, index=False, encoding='utf-8')
            self.logger.info(f"Data saved to {output_path}")
        except Exception as e:
            self.logger.error(f"Failed to save data: {e}")


def main():
    scraper = TransfermarktScraper()

    df = scraper.scrape_all_leagues()
    
    if not df.empty:
        print(f"\nSuccessfully scraped {len(df)} rows from {df['League'].nunique()} leagues")  
        scraper.save_data(df, "transfermarkt_data")
    else:
        print("No data was scraped successfully.")

if __name__ == "__main__":
    main()
