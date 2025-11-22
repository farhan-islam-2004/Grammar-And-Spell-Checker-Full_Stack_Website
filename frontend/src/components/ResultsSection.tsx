import type { ProcessingResult } from '../types';

interface Props {
    result: ProcessingResult;
}

export default function ResultsSection({ result }: Props) {
    const copyToClipboard = async (text: string, id: string) => {
        try {
            await navigator.clipboard.writeText(text);
            const button = document.getElementById(`copy-${id}`);
            if (button) {
                const originalText = button.textContent;
                button.textContent = '✓ Copied!';
                button.classList.add('bg-green-500');
                setTimeout(() => {
                    button.textContent = originalText;
                    button.classList.remove('bg-green-500');
                }, 2000);
            }
        } catch (err) {
            alert('Failed to copy text');
        }
    };

    return (
        <div className="space-y-6 animate-fade-in">
            {result.action === 'correct' && (
                <>
                    <ResultCard
                        title="Spell Corrected Text"
                        content={result.spellCorrected || 'No changes detected.'}
                        color="primary"
                        onCopy={() => copyToClipboard(result.spellCorrected || '', 'spell')}
                        copyId="spell"
                    />
                    <ResultCard
                        title="Grammar Corrected Text"
                        content={result.corrected || 'No changes detected.'}
                        color="green"
                        onCopy={() => copyToClipboard(result.corrected || '', 'grammar')}
                        copyId="grammar"
                    />
                </>
            )}

            {result.action === 'paraphrase' && result.paraphrased && (
                <ResultCard
                    title="Paraphrased Text"
                    content={result.paraphrased}
                    color="secondary"
                    onCopy={() => copyToClipboard(result.paraphrased || '', 'paraphrase')}
                    copyId="paraphrase"
                />
            )}

            {result.action === 'humanize' && result.humanized && (
                <ResultCard
                    title="Humanized Text"
                    content={result.humanized}
                    color="info"
                    onCopy={() => copyToClipboard(result.humanized || '', 'humanize')}
                    copyId="humanize"
                />
            )}

            {result.action === 'summarize' && result.summary && (
                <ResultCard
                    title="Summary"
                    content={result.summary}
                    color="orange"
                    onCopy={() => copyToClipboard(result.summary || '', 'summary')}
                    copyId="summary"
                />
            )}

            {result.action === 'translate' && result.translated && (
                <ResultCard
                    title="Translated Text"
                    content={result.translated}
                    color="purple"
                    onCopy={() => copyToClipboard(result.translated || '', 'translate')}
                    copyId="translate"
                />
            )}
        </div>
    );
}

interface ResultCardProps {
    title: string;
    content: string;
    color: string;
    onCopy: () => void;
    copyId: string;
}

function ResultCard({ title, content, color, onCopy, copyId }: ResultCardProps) {
    const colorClasses = {
        primary: 'border-l-primary',
        green: 'border-l-green-500',
        secondary: 'border-l-secondary',
        orange: 'border-l-orange-500',
        purple: 'border-l-purple-500',
    };

    return (
        <div className="card hover:-translate-y-1 transition-transform">
            <div className="flex items-start justify-between mb-4">
                <h3 className="text-xl font-semibold">{title}</h3>
                <button
                    id={`copy-${copyId}`}
                    onClick={onCopy}
                    className="px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary-dark transition-colors text-sm font-medium"
                >
                    Copy
                </button>
            </div>
            <div className={`result-box p-4 rounded-xl border-l-4 ${colorClasses[color as keyof typeof colorClasses]} leading-relaxed`}>
                {content}
            </div>
        </div>
    );
}
