import { useState, useEffect } from 'react';

// TextInput component for user input

interface Props {
    value: string;
    onChange: (value: string) => void;
}

export default function TextInput({ value, onChange }: Props) {
    const [charCount, setCharCount] = useState(0);

    useEffect(() => {
        setCharCount(value.length);
    }, [value]);

    const getCounterColor = () => {
        if (charCount > 1800) return 'text-red-600 dark:text-red-400';
        if (charCount > 1500) return 'text-orange-600 dark:text-orange-400';
        return 'text-gray-500 dark:text-gray-400';
    };

    return (
        <div className="mb-6">
            <label htmlFor="input_text" className="block text-sm font-semibold text-primary uppercase tracking-wide mb-2">
                Enter Your Text
            </label>
            <textarea
                id="input_text"
                value={value}
                onChange={(e) => onChange(e.target.value)}
                rows={8}
                maxLength={2000}
                placeholder="Type or paste your text here (max 2000 characters)..."
                className="input resize-y"
            />
            <div className={`text-right text-sm mt-2 ${getCounterColor()}`}>
                <span className="font-semibold">{charCount}</span> / 2000 characters
            </div>
        </div>
    );
}
