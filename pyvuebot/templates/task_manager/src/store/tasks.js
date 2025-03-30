import { ref, computed } from "vue";
import apiService from "../services/apiService";

export default function useTaskStore(userId) {
  const tasks = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  const loadTasks = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const fetchedTasks = await apiService.getTasks(userId);
      tasks.value = fetchedTasks || [];
    } catch (err) {
      console.error("Error loading tasks:", err);
      error.value = "Failed to load tasks";
    } finally {
      isLoading.value = false;
    }
  };

  const addTask = async (task) => {
    isLoading.value = true;
    error.value = null;

    try {
      const newTask = await apiService.createTask(userId, task);
      tasks.value.unshift(newTask);
      return newTask;
    } catch (err) {
      console.error("Error adding task:", err);
      error.value = "Failed to add task";
      return null;
    } finally {
      isLoading.value = false;
    }
  };

  const toggleTask = async (taskId) => {
    const task = tasks.value.find(t => t.id === taskId);
    if (!task) return;

    const newStatus = task.status === "completed" ? "pending" : "completed";
    try {
      await apiService.updateTask(userId, taskId, { status: newStatus });
      task.status = newStatus;
    } catch (err) {
      console.error("Error updating task:", err);
      error.value = "Failed to update task";
    }
  };

  const removeTask = async (taskId) => {
    try {
      await apiService.deleteTask(userId, taskId);
      tasks.value = tasks.value.filter(t => t.id !== taskId);
    } catch (err) {
      console.error("Error removing task:", err);
      error.value = "Failed to remove task";
    }
  };

  const activeTasks = computed(() => 
    tasks.value.filter(task => task.status !== "completed").length
  );

  return {
    tasks,
    isLoading,
    error,
    loadTasks,
    addTask,
    toggleTask,
    removeTask,
    activeTasks,
  };
}