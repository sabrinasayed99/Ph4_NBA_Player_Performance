import requests
from bs4 import BeautifulSoup 
import pandas as pd
import sqlite3
from datetime import datetime
import logging
import os


def setup_logging():
    log_dir = 'logs'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_file = f'logs/nba_scraper_{datetime.now().strftime("%Y-%m-%d_%H-%M-%S")}.log'

    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        handlers=[
                        logging.FileHandler(log_file), 
                        logging.StreamHandler()
                    ]
                    )
    return logging.getLogger(__name__)

def convert_team_names_to_abbrev(df):
    team_abbrev = {
        'Atlanta Hawks': 'ATL',
        'Boston Celtics': 'BOS',
        'Charlotte Hornets': 'CHA',
        'Chicago Bulls': 'CHI',
        'Cleveland Cavaliers': 'CLE',
        'Dallas Mavericks': 'DAL',
        'Denver Nuggets': 'DEN',
        'Detroit Pistons': 'DET',
        'Golden State Warriors': 'GSW',
        'Houston Rockets': 'HOU',
        'Indiana Pacers': 'IND',
        'Los Angeles Clippers': 'LAC',
        'Los Angeles Lakers': 'LAL',
        'Memphis Grizzlies': 'MEM',
        'Miami Heat': 'MIA',
        'Milwaukee Bucks': 'MIL',
        'Minnesota Timberwolves': 'MIN',
        'New Orleans Pelicans': 'NOH',
        'New York Knicks': 'NYK',
        'Brooklyn Nets': 'BKN',
        'Oklahoma City Thunder': 'OKC',
        'Orlando Magic': 'ORL',
        'Philadelphia 76ers': 'PHI',
        'Phoenix Suns': 'PHO',
        'Portland Trail Blazers': 'POR',
        'San Antonio Spurs': 'SAS',
        'Sacramento Kings': 'SAC',
        'Toronto Raptors': 'TOR',
        'Utah Jazz': 'UTH',
        'Washington Wizards': 'WAS'
    }
    df['Team'] = df['Team'].replace(team_abbrev)
    return df

def get_conference_stats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    east_table = soup.find('table', {'id': 'confs_standings_E'})
    west_table = soup.find('table', {'id': 'confs_standings_W'})
    
    east_conf_stats_df = pd.read_html(str(east_table))[0]
    west_conf_stats_df = pd.read_html(str(west_table))[0]
    
    return east_conf_stats_df, west_conf_stats_df

def get_team_per_game_stats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    per_game_team_stats = soup.find('table', {'id': 'per_game-team'})
    per_game_team_df = pd.read_html(str(per_game_team_stats))[0]
    return per_game_team_df

def get_team_total_stats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    total_team_stats = soup.find('table', {'id': 'totals-team'})
    total_team_stats_df = pd.read_html(str(total_team_stats))[0]
    return total_team_stats_df

def get_players_regular_stats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    player_stats = soup.find('table', {'id': 'tablepress-127'})
    player_stats_df = pd.read_html(str(player_stats))[0]
    return player_stats_df

def job():

    
        #Initialize logging
    logger = setup_logging()

        # Log the start of the script
    logger.info(f"NBA data scraping started")

        
    try:
        # Create database connection
        conn = sqlite3.connect('nba_data.db')
        logger.info(f"Database connection established")
            
            # NBA Reference URL
        nba_ref_url = "https://www.basketball-reference.com/leagues/NBA_2025.html"
            
            # Get and process conference stats
        logger.info(f"Getting conference stats")
        east_stats, west_stats = get_conference_stats(nba_ref_url)
        logger.info(f"Conference stats retrieved successfully")
            
            # Process Eastern Conference stats
        logger.info(f"Processing Eastern Conference stats")
        east_stats.rename(columns={'Eastern Conference': 'Team'}, inplace=True)
        east_stats['Team'] = east_stats['Team'].str[:-4]
        east_stats['Team'] = east_stats['Team'].str.strip()
        east_stats = convert_team_names_to_abbrev(east_stats)
        east_stats.to_sql('eastern_conference_stats', conn, if_exists='replace', index=False)
        east_stats.to_csv('east_conf_stats.csv', index=False)
        logger.info(f"Eastern Conference stats saved to database")

            # Process Western Conference stats
        logger.info(f"Processing Western Conference stats")
        west_stats.rename(columns={'Western Conference': 'Team'}, inplace=True)
        west_stats['Team'] = west_stats['Team'].str[:-4]
        west_stats['Team'] = west_stats['Team'].str.strip()
        west_stats = convert_team_names_to_abbrev(west_stats)
        west_stats.to_sql('western_conference_stats', conn, if_exists='replace', index=False)
        west_stats.to_csv('west_conf_stats.csv', index=False)
        logger.info(f"Western Conference stats saved to database")

            # Get and process team per game stats
        logger.info(f"Getting team per game stats")
        per_game_team_stats = get_team_per_game_stats(nba_ref_url)
        per_game_team_stats = convert_team_names_to_abbrev(per_game_team_stats)
        per_game_team_stats = per_game_team_stats.drop(per_game_team_stats.index[-1])
        per_game_team_stats.to_sql('per_game_team_stats', conn, if_exists='replace', index=False)
        per_game_team_stats.to_csv('per_game_team_stats.csv', index=False)
        logger.info(f"Team per game stats saved to database")
            
            # Get and process team total stats
        logger.info(f"Getting team total stats")
        total_team_stats = get_team_total_stats(nba_ref_url)
        total_team_stats = convert_team_names_to_abbrev(total_team_stats)
        total_team_stats = total_team_stats.drop(total_team_stats.index[-1])
        total_team_stats.to_sql('total_team_stats', conn, if_exists='replace', index=False)
        total_team_stats.to_csv('total_team_stats.csv', index=False)
        logger.info(f"Team total stats saved to database")
            

        players_url = "https://www.nbastuffer.com/2024-2025-nba-player-stats/"

        # Get and process player stats
        logger.info(f"Getting player stats")
        players_regular_stats = get_players_regular_stats(players_url)
        players_regular_stats = players_regular_stats.drop(columns=['RANK'])
        players_regular_stats['TEAM'] = players_regular_stats['TEAM'].str.upper()
        players_regular_stats.rename(columns={
                'TEAM': 'Team',
                'NAME': 'Name',
                'AGE': 'Age'
            }, inplace=True)
        players_regular_stats.to_sql('players_stats', conn, if_exists='replace', index=False)
        players_regular_stats.to_csv('players_stats.csv', index=False)
        logger.info(f"Player stats saved to database")
            
    except requests.exceptions.RequestException as e:
            logger.error(f"Network error occurred: {str(e)}")
    except sqlite3.Error as e:
            logger.error(f"Database error occurred: {str(e)}")
    except Exception as e:
            logger.error(f"Unexpected error occurred: {str(e)}")
            logger.exception("Full traceback:")
            
    finally:
            conn.close()
            logger.info("Database connection closed")

if __name__ == "__main__":
    job()