import sys
import typing

if typing.TYPE_CHECKING:
    from django.core.management import BaseCommand

    _Base = BaseCommand
else:
    _Base = object


class PrintCommandMixin(_Base):
    """Provides the print facility."""

    def print(self, style: str, msg: str, exit_code: int | None = None) -> None:
        """Print a message using a management command style."""
        self.stdout.write(getattr(self.style, style)(msg))
        if exit_code is not None:
            sys.exit(exit_code)
