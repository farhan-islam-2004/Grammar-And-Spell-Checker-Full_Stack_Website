import { useState, useEffect } from 'react';

export default function ThemeToggle() {
    const [isDark, setIsDark] = useState(false);

    useEffect(() => {
        const stored = localStorage.getItem('darkMode');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const shouldBeDark = stored === 'true' || (!stored && prefersDark);

        setIsDark(shouldBeDark);
        if (shouldBeDark) {
            document.documentElement.classList.add('dark');
        }
    }, []);

    const toggleTheme = () => {
        setIsDark(!isDark);
        document.documentElement.classList.toggle('dark');
        localStorage.setItem('darkMode', (!isDark).toString());
    };

    return (
        <button
            onClick={toggleTheme}
            className="fixed top-8 right-8 z-50 card px-6 py-3 flex items-center gap-2 hover:scale-105 transition-transform"
        >
            <span className="text-xl">{isDark ? '☀️' : '🌙'}</span>
            <span className="font-medium">{isDark ? 'Light' : 'Dark'} Mode</span>
        </button>
    );
}
