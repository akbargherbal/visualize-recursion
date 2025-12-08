/**
 * API service for communicating with the Flask backend.
 * Centralized HTTP client with error handling.
 */

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class APIError extends Error {
  constructor(message, status, details) {
    super(message);
    this.name = 'APIError';
    this.status = status;
    this.details = details;
  }
}

async function fetchJSON(url, options = {}) {
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    const data = await response.json();

    if (!response.ok) {
      throw new APIError(
        data.error || 'Request failed',
        response.status,
        data.details
      );
    }

    return data;
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError('Network error: ' + error.message, 0);
  }
}

export const api = {
  /**
   * Fetch all available algorithms
   */
  async fetchAlgorithms() {
    const data = await fetchJSON(`${API_BASE}/algorithms`);
    return data.algorithms;
  },

  /**
   * Fetch algorithms by category
   */
  async fetchAlgorithmsByCategory(category) {
    const data = await fetchJSON(`${API_BASE}/algorithms/${category}`);
    return data.algorithms;
  },

  /**
   * Fetch all categories
   */
  async fetchCategories() {
    const data = await fetchJSON(`${API_BASE}/algorithms/categories`);
    return data.categories;
  },

  /**
   * Fetch algorithm metadata
   */
  async fetchAlgorithmInfo(algorithmId) {
    const data = await fetchJSON(`${API_BASE}/algorithm/${algorithmId}`);
    return data.algorithm;
  },

  /**
   * Get default example for algorithm
   */
  async getDefaultExample(algorithmId) {
    const data = await fetchJSON(`${API_BASE}/algorithm/${algorithmId}/example`);
    return data.example;
  },

  /**
   * Generate trace for algorithm with input data
   */
  async generateTrace(algorithmId, inputData) {
    const data = await fetchJSON(`${API_BASE}/algorithm/${algorithmId}/trace`, {
      method: 'POST',
      body: JSON.stringify(inputData),
    });
    return {
      trace: data.trace,
      result: data.result,
    };
  },

  /**
   * Health check
   */
  async healthCheck() {
    const data = await fetchJSON(`${API_BASE}/health`);
    return data;
  },
};

export default api;