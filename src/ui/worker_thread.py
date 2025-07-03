import logging
import queue
import threading
from typing import List

from src.alarm import Alarm
from src.alarm_category import AlarmCategory
from src.symbol import Symbol
from src.xls_write import write_xls_from_alarms


logger = logging.getLogger(__name__)


alarm_categories = [
    AlarmCategory(r'stS\d+DefImdt\w*\.', (165,42,42), (0,0,0)),
    AlarmCategory(r'stS\d+DefFcy\w*\.', (165,42,42), (0,0,0)),
    AlarmCategory(r'stS\d+DefAttente\w*\.', (0,0,255), (255,255,255)),
    AlarmCategory(r'stS\d+Avert\w*\.', (255,215,0), (0,0,0)),
    AlarmCategory(r'stS\d+Message\w*\.', (0,0,255), (255,255,255)),
]


def find_matching_category(symbol: Symbol, categories: List[AlarmCategory]):
    return next((cat for cat in categories if cat.is_match(symbol.name)), None)


class WorkerThread(threading.Thread):
    """
    This worker thread is intended to handle time-consuming tasks in order to keep the UI responsive.

    It works using two Queues:
        - task_queue: To get from the UI thread the data defining the task to run.
          A task is defined using a command string and optional arguments.
        - result_queue: To send back to the UI thread the result of the task.
    """
    def __init__(self, task_queue, result_queue):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        while True:
            try:
                command, cmd_args = self.task_queue.get(timeout=1)
                logger.debug(f'{command} - {cmd_args}')
                if command == 'parse':
                    import_source = cmd_args[0]
                    symbols_filepath = cmd_args[1]
                    self.parse(import_source, symbols_filepath)
                elif command == 'write_xls':
                    alarms = cmd_args[0]
                    plc_name = cmd_args[1]
                    xlsx_filepath = cmd_args[2]
                    write_xls_from_alarms(xlsx_filepath, plc_name, alarms)
                    self.result_queue.put(('write_xls_success', xlsx_filepath))
                elif command == 'stop':
                    break
            except queue.Empty:
                continue

    def parse(self, import_src, symbols_filepath):
        alarms = []

        if import_src.name == 'codesys':
            # TODO
            raise NotImplementedError
        elif import_src.name == 'omron-sysmac':
            for line in open(symbols_filepath):
                fields = line.strip().split('\t')
                symbol = Symbol(name=fields[0], type=fields[1], comment=fields[3])
                category = find_matching_category(symbol, alarm_categories)
                if category:
                    alarms.append(Alarm(symbol=symbol, category=category))

        self.result_queue.put(('parse_result', alarms))
