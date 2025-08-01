from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import unittest
import logging

# Logger einrichten
logger = logging.getLogger("test_logger")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.FileHandler("test_failures.log")
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def run_all_tests():
    console = Console()

    loader = unittest.TestLoader()
    suite = loader.discover("tests")

    result = unittest.TextTestRunner(verbosity=2).run(suite)

    summary = Table(title="Testzusammenfassung")
    summary.add_column("Ergebnis")
    summary.add_column("Anzahl", justify="right")

    passed = result.testsRun - len(result.failures) - len(result.errors)
    summary.add_row("Erfolgreich", str(passed))
    summary.add_row("Fehler", str(len(result.errors)))
    summary.add_row("Fehlschläge", str(len(result.failures)))
    summary.add_row("Tests insgesamt", str(result.testsRun))

    if result.failures or result.errors:
        logger.warning("Fehlschläge im Testlauf:")
        for failed_test, traceback in result.failures + result.errors:
            logger.warning("%s\n%s", failed_test, traceback)

    try:
        console.print(Panel.fit(summary, title="Testergebnisse", border_style="cyan"))
    except UnicodeEncodeError:
        console.print("[cyan]Testergebnisse:[/cyan]")
        console.print(summary)

if __name__ == "__main__":
    run_all_tests()