/**
 * API service for communicating with the backend
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('API request failed:', error);
      throw error;
    }
  }

  // Health check
  async healthCheck() {
    return this.request('/health');
  }

  // Medicine endpoints
  async getMedicines(params = {}) {
    const queryString = new URLSearchParams(params).toString();
    return this.request(`/medicines?${queryString}`);
  }

  async getMedicineById(id) {
    return this.request(`/medicines/${id}`);
  }

  async searchMedicines(searchData) {
    return this.request('/medicines/search', {
      method: 'POST',
      body: JSON.stringify(searchData),
    });
  }

  // Symptom endpoints
  async getSymptoms() {
    return this.request('/symptoms');
  }

  async getConditions() {
    return this.request('/conditions');
  }

  // Recommendation endpoints
  async getRecommendations(recommendationData) {
    return this.request('/recommend', {
      method: 'POST',
      body: JSON.stringify(recommendationData),
    });
  }

  // Tablet recognition endpoints
  async identifyTablet(formData) {
    return this.request('/identify', {
      method: 'POST',
      headers: {
        // Don't set Content-Type, let browser set it with boundary
      },
      body: formData,
    });
  }

  // Chat endpoints
  async chatWithDoctor(chatData) {
    return this.request('/chat', {
      method: 'POST',
      body: JSON.stringify(chatData),
    });
  }
}

// Create and export a singleton instance
export const apiService = new ApiService();
