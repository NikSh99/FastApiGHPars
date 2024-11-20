import logging


def setup_logging():
    # log_path = "/tmp/ghparser.log"
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        handlers=[
            logging.StreamHandler(),
            # logging.FileHandler(log_path)
        ]
    )
