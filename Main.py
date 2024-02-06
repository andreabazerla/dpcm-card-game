import logging
import numpy as np
import pandas as pd

from src.Utils import clear_console, clear_file, get_config, get_logger
from src.Turnament import Turnament

if __name__ == '__main__':
    clear_console()

    clear_file('output/info.log')
    clear_file('output/debug.log')
    
    logger = get_logger('info', logging.INFO, console=True, file='output/info.log')
    debugger = get_logger('debug', logging.DEBUG, file='output/debug.log')

    config = get_config()

    turnament_config = config['TURNAMENT']
    players_config = config['PLAYERS']

    turnament_number = turnament_config['NUMBER']
    turnament_fair = turnament_config['FAIR']

    try:
        logger.info(f'Wait. Trying to load AI... :/')
        logger.info('')

        q = pd.read_csv('data/q.csv', index_col=0, converters={0: lambda x: eval(x)})
        visited = pd.read_csv('data/visited.csv', index_col=0, converters={0: lambda x: eval(x)})
        
        logger.info(f'AI loaded. :D Go!')
        logger.info('')
    except:
        q = None
        visited = None

    turnament = Turnament(turnament_number, turnament_fair)
    winner_list = turnament.start(logger, q, visited)

    visits = None
    state_seen = None
    players = turnament.get_players()
    for player in players:
        visited = player.get_visited()
        if player.is_ai():
            q = player.get_q()
            visits = player.get_visits()
            state_seen = player.get_state_seen()
            break

    winner_list_light = []
    winner_dict = {}
    for winner in winner_list:
        if winner[0].get_name() in winner_dict:
            winner_dict[winner[0].get_name()] += 1
        else:
            winner_dict[winner[0].get_name()] = 1

        logger.info(f'Player {winner[0].get_name()} won the game at turn {winner[1]} {"(Fake Winner)" if winner[2] else ""} {"(Expected Winner)" if winner[3] else ""}')

        winner_list_light.append([winner[0].get_name(), winner[1]])

    logger.info('')

    for key, value in winner_dict.items():
        logger.info(f'Player {key} won {value} games')

    results = pd.DataFrame(winner_list_light, columns=['Winner', 'Turns'])

    results['Rate'] = np.where(results['Winner'] == players_config[0]['NAME'], 1, 0)
    results['Rate'] = results['Rate'].cumsum() / (results.index + 1)

    logger.info('')
    logger.info(f'Wait. Saving AI brain... ;)')
    logger.info('')

    results.to_csv('data/results.csv', index=False)
    
    if q is not None:
        q.index.rename('ID', inplace=True)
        q.to_csv('data/q.csv', index=True)
    
    if visited is not None:
        visited.index.rename('ID', inplace=True)
        visited.to_csv('data/visited.csv', index=True)

    if visits is not None:
        pd.DataFrame(visits, columns=['Visits']).to_csv('data/visits.csv', index=False)

    if state_seen is not None:
        state_before = [state_seen[0] for state_seen in state_seen]
        state_after = [state_seen[1] for state_seen in state_seen]

        pd.DataFrame({'Before': state_before, 'After': state_after}).to_csv('data/state_seen.csv', index=False)

    logger.info('DONE')