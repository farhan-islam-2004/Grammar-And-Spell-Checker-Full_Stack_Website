import { useState } from 'react';
// Main App component
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import AppHeader from './components/AppHeader';
import TextInput from './components/TextInput';
import ActionButtons from './components/ActionButtons';
import ResultsSection from './components/ResultsSection';
import ThemeToggle from './components/ThemeToggle';
import type { ActionType, ProcessingResult } from './types';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function AppContent() {
  const [text, setText] = useState('');
  const [result, setResult] = useState<ProcessingResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAction = async (action: ActionType, targetLang?: string) => {
    if (!text.trim()) {
      setError('Please enter some text first!');
      return;
    }

    if (text.length > 2000) {
      setError('Text exceeds maximum length of 2000 characters');
      return;
    }

    setError(null);
    setIsLoading(true);

    try {
      let endpoint = '';
      let body = {};

      switch (action) {
        case 'correct':
          endpoint = '/api/correct';
          body = { text };
          break;
        case 'paraphrase':
          endpoint = '/api/paraphrase';
          body = { text };
          break;
        case 'humanize':
          endpoint = '/api/humanize';
          body = { text };
          break;
        case 'summarize':
          endpoint = '/api/summarize';
          body = { text };
          break;
        case 'translate':
          endpoint = '/api/translate';
          body = { text, target_lang: targetLang };
          break;
      }

      const response = await fetch(`http://localhost:5001${endpoint}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Request failed');
      }

      const data = await response.json();

      setResult({
        action,
        original: text,
        spellCorrected: data.spell_version,
        corrected: data.corrected,
        paraphrased: data.paraphrased,
        humanized: data.humanized,
        summary: data.summary,
        translated: data.translated,
      });

    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen relative overflow-hidden">
      {/* Animated background gradient */}
      <div className="fixed top-0 right-0 w-full h-full pointer-events-none">
        <div className="absolute top-[-50%] right-[-50%] w-[200%] h-[200%] bg-gradient-radial from-primary/10 via-transparent to-transparent animate-gradient" />
      </div>

      <ThemeToggle />

      <div className="relative z-10 max-w-6xl mx-auto px-4 py-8">
        <AppHeader />

        <div className="card mb-8">
          <TextInput value={text} onChange={setText} />
          <ActionButtons
            onAction={handleAction}
            onClear={handleClear}
            isLoading={isLoading}
          />
        </div>

        {error && (
          <div className="card bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800 mb-8">
            <div className="flex items-center gap-3">
              <span className="text-2xl"></span>
              <div>
                <h3 className="font-semibold text-red-900 dark:text-red-100">Error</h3>
                <p className="text-red-700 dark:text-red-300">{error}</p>
              </div>
            </div>
          </div>
        )}

        {result && <ResultsSection result={result} />}
      </div>
    </div>
  );
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AppContent />
    </QueryClientProvider>
  );
}

export default App;
