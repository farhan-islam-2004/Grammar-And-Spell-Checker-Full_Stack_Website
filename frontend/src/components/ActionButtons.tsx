import { useState } from 'react';
import type { ActionType } from '../types';

interface Props {
    onAction: (action: ActionType, targetLang?: string) => void;
    onClear: () => void;
    isLoading: boolean;
}

const LANGUAGES = [
    'French', 'Spanish', 'German', 'Italian', 'Russian', 'Chinese', 'Hindi'
];

export default function ActionButtons({ onAction, onClear, isLoading }: Props) {
    const [targetLang, setTargetLang] = useState('French');

    return (
        <div>
            <div className="mb-6">
                <label
                    htmlFor="target_lang"
                    className="block text-sm font-semibold text-primary uppercase tracking-wide mb-2"
                >
                    Translation Language
                </label>
                <select
                    id="target_lang"
                    value={targetLang}
                    onChange={(e) => setTargetLang(e.target.value)}
                    className="input"
                >
                    {LANGUAGES.map((lang) => (
                        <option key={lang} value={lang}>
                            {lang}
                        </option>
                    ))}
                </select>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4">
                <button
                    onClick={() => onAction('correct')}
                    disabled={isLoading}
                    className="btn btn-primary"
                >
                    Grammar & Spell
                </button>
                <button
                    onClick={() => onAction('paraphrase')}
                    disabled={isLoading}
                    className="btn btn-secondary"
                >
                    Paraphrase
                </button>
                <button
                    onClick={() => onAction('humanize')}
                    disabled={isLoading}
                    className="btn btn-info"
                >
                    Humanize
                </button>
                <button
                    onClick={() => onAction('summarize')}
                    disabled={isLoading}
                    className="btn btn-success"
                >
                    Summarize
                </button>
                <button
                    onClick={() => onAction('translate', targetLang)}
                    disabled={isLoading}
                    className="btn btn-warning"
                >
                    Translate
                </button>
                <button
                    onClick={onClear}
                    disabled={isLoading}
                    className="btn btn-outline"
                >
                    Clear
                </button>
            </div>

            {isLoading && (
                <div className="mt-6 text-center">
                    <div className="inline-block w-12 h-12 border-4 border-primary border-t-transparent rounded-full animate-spin" />
                    <p className="mt-3 text-primary font-semibold">Processing your text...</p>
                </div>
            )}
        </div>
    );
} 