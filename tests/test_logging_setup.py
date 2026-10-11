import logging

from coffee_slm.logging_setup import setup_logging


def test_writes_formatted_line_to_file(tmp_path):
    log_file = tmp_path / "logs" / "run.log"
    setup_logging(log_file=log_file)

    logging.getLogger("coffee_slm.test").info("hello %d", 42)

    line = log_file.read_text()
    assert "| INFO    | coffee_slm.test | hello 42" in line
    logging.shutdown()


def test_respects_level():
    setup_logging(level="WARNING")
    assert logging.getLogger().level == logging.WARNING
