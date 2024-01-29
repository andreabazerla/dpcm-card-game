import logging
import pandas as pd

from src.Logger import Logger
from src.Utils import clear_console, get_config
from src.Turnament import Turnament

if __name__ == "__main__":
    clear_console()

    logger = Logger('logging', 'output.log')
    logger.setup_logger(console=True, file=True)
    logger.clear_output()

    debug = Logger('logging', 'debug.log')
    debug.setup_logger(console=False, file=True)
    debug.info('test')

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