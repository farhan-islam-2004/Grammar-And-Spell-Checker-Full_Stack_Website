export interface CorrectionResponse {
    original: string;
    spell_version: string;
    corrected: string;
}

export interface HealthResponse {
    status: string;
    languagetool_available: boolean;
    languagetool_type: string;
}

export type ActionType = 'correct' | 'paraphrase' | 'summarize' | 'translate' | 'humanize';

export interface ProcessingResult {
    action: ActionType;
    original: string;
    spellCorrected?: string;
    corrected?: string;
    paraphrased?: string;
    summary?: string;
    translated?: string;
    humanized?: string;
}
