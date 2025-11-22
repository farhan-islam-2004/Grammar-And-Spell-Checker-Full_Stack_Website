"""
Simple NLPModel used by the Flask app.

Behavior:
- Uses TextBlob for lightweight spell correction.
- Uses language_tool_python only if a remote server URL is provided
  via `server_url` or if `disable_local_lt` is False and Java is present.
- By default we avoid starting a local LanguageTool Java process so
  the app can run without Java during development. Set
  `disable_local_lt=False` to allow local LanguageTool startup.
"""

from typing import Optional, Tuple
import os
from textblob import TextBlob
import language_tool_python


class NLPModel:
    def __init__(self, server_url: Optional[str] = None, disable_local_lt: bool = True):
        """Create the model.

        - server_url: if provided, connect to that LanguageTool server.
        - disable_local_lt: if True and server_url is None, do not try to start local Java process.
        """
        self.server_url = server_url
        self.disable_local_lt = disable_local_lt
        self.tool = None

        # Initialize language tool only when a server_url is given, or when local startup is allowed
        if self.server_url:
            try:
                self.tool = language_tool_python.LanguageTool(server_url=self.server_url)
            except Exception:
                # leave tool as None on failure
                self.tool = None
        else:
            if not self.disable_local_lt:
                try:
                    # This may attempt to start a Java process (will block if Java isn't available)
                    self.tool = language_tool_python.LanguageTool('en-US')
                except Exception:
                    self.tool = None

    def _spell_correct(self, text: str) -> str:
        if not text:
            return text
        try:
            blob = TextBlob(text)
            return str(blob.correct())
        except Exception:
            return text

    def _grammar_fix_with_languagetool(self, text: str) -> str:
        if not text:
            return text
        if not self.tool:
            return text
        try:
            matches = self.tool.check(text)
            corrected = language_tool_python.utils.correct(text, matches)
            return corrected
        except Exception:
            return text

    def correct(self, text: str, do_spell: bool = True, do_grammar: bool = True) -> Tuple[str, str]:
        if not isinstance(text, str):
            raise TypeError('text must be a string')
        if text.strip() == '':
            return text, text

        spell_text = text
        if do_spell:
            spell_text = self._spell_correct(text)

        final_text = spell_text
        if do_grammar:
            final_text = self._grammar_fix_with_languagetool(spell_text)

        return spell_text, final_text

    def close(self):
        try:
            if self.tool is not None:
                self.tool.close()
        except Exception:
            pass