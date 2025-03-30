const API_URL = "/api";

const handleResponse = async (response) => {
  const contentType = response.headers.get("content-type");

  if (!contentType || !contentType.includes("application/json")) {
    throw new Error("Invalid response format from server");
  }

  const data = await response.json();

  if (!response.ok) {
    throw new Error(data.detail || `HTTP error! status: ${response.status}`);
  }

  return data;
};

const apiService = {
  async getTasks(userId) {
    try {
      const response = await fetch(`${API_URL}/tasks?user_id=${userId}`, {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
      });
      return await handleResponse(response);
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  },

  async createTask(userId, task) {
    try {
      const response = await fetch(`${API_URL}/tasks/task?user_id=${userId}`, {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(task),
      });
      return await handleResponse(response);
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  },

  async updateTask(userId, taskId, updates) {
    try {
      const response = await fetch(
        `${API_URL}/tasks/${taskId}?user_id=${userId}`,
        {
          method: "PUT",
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
          body: JSON.stringify(updates),
        }
      );
      return await handleResponse(response);
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  },

  async deleteTask(userId, taskId) {
    try {
      const response = await fetch(
        `${API_URL}/tasks/${taskId}?user_id=${userId}`,
        {
          method: "DELETE",
          headers: {
            Accept: "application/json",
          },
        }
      );
      return await handleResponse(response);
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  },
};

export default apiService;
