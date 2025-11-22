import axios from 'axios';
import type { CorrectionResponse, HealthResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 30000, // 30 seconds for model processing
});

export const healthCheck = async (): Promise<HealthResponse> => {
    const response = await api.get<HealthResponse>('/health');
    return response.data;
};

export const correctText = async (text: string): Promise<CorrectionResponse> => {
    const response = await api.post<CorrectionResponse>('/api/correct', { text });
    return response.data;
};

export default api;
