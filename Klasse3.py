from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import unittest

def run_all_tests():
    console = Console()

    loader = unittest.TestLoader()
    suite = loader.discover("tests")

    result = unittest.TextTestRunner(verbosity=2).run(suite)

    summary = Table(title="Testzusammenfassung")
    summary.add_column("Ergebnis", style="bold")
    summary.add_column("Anzahl", justify="right")

    summary.add_row("✅ Erfolgreich", str(result.testsRun - len(result.failures) - len(result.errors)))
    summary.add_row("❌ Fehler", str(len(result.errors)))
    summary.add_row("⚠️  Fehlschläge", str(len(result.failures)))
    summary.add_row("⏱️ Tests insgesamt", str(result.testsRun))

    console.print(Panel.fit(summary, title="🧪 Testergebnisse", border_style="cyan"))

if __name__ == "__main__":
    run_all_tests()



