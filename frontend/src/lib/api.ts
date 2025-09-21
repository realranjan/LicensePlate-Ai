import axios from 'axios';

// Configure axios with Django backend URL
const API_BASE_URL = process.env.NEXT_PUBLIC_FASTAPI_API_URL || 'http://localhost:8001';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30 seconds timeout for image processing
});

// Add request interceptor to handle CSRF token if needed
api.interceptors.request.use((config) => {
  // Add any auth headers here if needed
  return config;
});

export interface DetectionResponse {
  success: boolean;
  image_url: string;
  detections: string;
  riders_without_helmets?: string[];
  processing_time?: number;
  error?: string;
}

export const uploadAndAnalyzeImage = async (file: File): Promise<DetectionResponse> => {
  try {
    const formData = new FormData();
    formData.append('image_input', file);

    const response = await api.post('/detect-license-plate/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  } catch (error) {
    console.error('API Error:', error);
    
    if (axios.isAxiosError(error)) {
      throw new Error(
        error.response?.data?.error || 
        error.message || 
        'Failed to analyze image'
      );
    }
    
    throw new Error('An unexpected error occurred');
  }
};

export default api;