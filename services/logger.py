import logging
from datetime import datetime
from config import config

class MailingLogger:
    def __init__(self):
        logging.basicConfig(
            filename=f"logs/mailing_{datetime.now().strftime('%Y%m%d')}.log",
            level=logging.INFO,
            format="%(asctime)s - %(message)s"
        )
        self.logger = logging.getLogger("mailing")
    
    def log_action(self, user_id: int, action: str, status: str):
        self.logger.info(f"User {user_id} | {action} | {status}")