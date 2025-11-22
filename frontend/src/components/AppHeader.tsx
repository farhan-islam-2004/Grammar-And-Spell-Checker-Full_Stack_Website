export default function AppHeader() {
    return (
        <header className="text-center mb-16 animate-fade-in-down">
            <h1 className="text-4xl md:text-6xl font-extrabold tracking-tight mb-4 
                     bg-gradient-to-r from-blue-600 via-purple-500 to-pink-500 
                     bg-clip-text text-transparent">
                AI Text Assistant
            </h1>
            <p className="text-base md:text-lg text-gray-700 dark:text-gray-300 max-w-2xl mx-auto">
                Elevate your writing with intelligent grammar correction, spell checking, paraphrasing, summarization, and translation.
            </p>
        </header>
    );
}