import logging
import pandas as pd

from src.Utils import clear_console, clear_file, get_config, get_logger
from src.Turnament import Turnament

if __name__ == "__main__":
    clear_console()

    clear_file('output/info.log')
    clear_file('output/debug.log')
    
    logger = get_logger('info', logging.INFO, console=True, file='output/info.log')
    debugger = get_logger('debug', logging.DEBUG, file='output/debug.log')

    config = get_config()

    turnament_number = config['TURNAMENT']
    reset = config['RESET']

    if not reset:
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

    turnament = Turnament(turnament_number)
    winner_list, q_updated, visited_updated = turnament.start_turnament(logger, q, visited)

    winner_dict = {}
    for winner in winner_list:
        if winner[0].get_name() in winner_dict:
            winner_dict[winner[0].get_name()] += 1
        else:
            winner_dict[winner[0].get_name()] = 1

        logger.info(f'Player {winner[0].get_name()} won the game at loop {winner[1]} {"(Fake Winner)" if winner[2] else ""} {"(Expected Winner)" if winner[3] else ""}')

    logger.info('')

    for key, value in winner_dict.items():
        logger.info(f'Player {key} won {value} games')

    logger.info('')
    if not reset:
        logger.info(f'Wait. Saving AI brain... ;)')
        logger.info('')

        q_updated.to_csv('data/q.csv', index=True)
        visited_updated.to_csv('data/visited.csv', index=True)

    logger.info('DONE')