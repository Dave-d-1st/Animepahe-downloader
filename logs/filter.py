import logging.config
class Filtered(logging.Filter):
    def filter(self, record: logging.LogRecord):
        record.msg=record.msg.replace(f"{float('-inf')}","First").replace(f"{float('inf')}","Last")
        return record