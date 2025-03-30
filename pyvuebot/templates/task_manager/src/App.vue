<template>
  <div class="min-h-screen p-4 relative">
    <!-- Background patterns (subtle) -->
    <div class="fixed inset-0 pattern-dots opacity-5 pointer-events-none"></div>

    <header class="mb-6 text-center">
      <h1
        class="text-2xl font-bold mb-1 relative inline-block"
        :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
      >
        <span class="relative z-10">✨ Task Manager</span>
        <!-- Cute underline effect -->
        <div
          class="absolute -bottom-1 left-0 right-0 h-3 -z-10 transform -rotate-1"
          style="
            background: var(--gradient-primary);
            opacity: 0.3;
            border-radius: 4px;
          "
        ></div>
      </h1>
      <p
        class="text-sm"
        :style="{
          color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)',
        }"
      >
        Keep track of your daily tasks
      </p>
    </header>

    <user-info :user="user" :tasks="tasks" />

    <div
      v-if="isLoading"
      class="flex flex-col items-center justify-center py-12"
    >
      <div class="relative w-16 h-16">
        <!-- Loading animation with cute design -->
        <div
          class="absolute inset-0 rounded-full animate-ping"
          style="background: var(--gradient-primary); opacity: 0.3"
        ></div>
        <div
          class="absolute inset-3 rounded-full animate-spin"
          style="
            border: 3px solid transparent;
            border-top-color: var(--color-primary);
            border-right-color: var(--color-primary);
          "
        ></div>
        <div
          class="absolute inset-6 rounded-full"
          style="background: var(--gradient-primary)"
        ></div>
      </div>
      <p class="mt-4 text-sm font-medium">Loading your tasks...</p>
    </div>

    <div v-else class="max-w-md mx-auto">
      <div
        v-if="error"
        class="mb-5 p-4 rounded-lg relative overflow-hidden"
        style="
          background: linear-gradient(to right, #fecaca, #fee2e2);
          color: #b91c1c;
        "
      >
        <div
          class="pattern-dots absolute inset-0 opacity-5 pointer-events-none"
        ></div>
        <div class="flex items-center gap-2 relative z-10">
          <svg class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor">
            <path
              fill-rule="evenodd"
              d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z"
              clip-rule="evenodd"
            />
          </svg>
          <span>{{ error }}</span>
        </div>
      </div>

      <task-list
        :tasks="tasks"
        @add-task="addTask"
        @update-task="updateTask"
        @remove-task="removeTask"
      />
    </div>

    <!-- Debug info - only visible in dev mode -->
    <div
      v-if="isDebugMode"
      class="mt-6 p-4 rounded-lg text-xs relative overflow-hidden"
      :style="{
        backgroundColor: 'rgba(0,0,0,0.05)',
        color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)',
      }"
    >
      <div
        class="pattern-lines absolute inset-0 opacity-5 pointer-events-none"
      ></div>
      <div class="relative z-10">
        <p class="mb-1">🆔 User ID: {{ userId }}</p>
        <p class="mb-1">📊 Tasks in storage: {{ tasks.length }}</p>
        <button
          @click="clearLocalStorage"
          class="mt-2 px-3 py-1 rounded-lg text-white transition-all hover:scale-105"
          style="background: var(--gradient-priority-high)"
        >
          🗑️ Clear Local Storage
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import telegramService from "./services/telegramService";
import apiService from "./services/apiService";
import UserInfo from "./components/UserInfo.vue";
import TaskList from "./components/TaskList.vue";

// Get user data from Telegram
const user = ref(telegramService.getUserData());

// Bot Link to open when Back to bot clicked
const BOT_LINK = import.meta.env.VITE_TELEGRAM_BOT_LINK;

// State variables
const tasks = ref([]);
const isLoading = ref(true);
const error = ref(null);
const tg = window.Telegram?.WebApp;

// Determine if we're in debug mode
const isDebugMode = ref(
  process.env.NODE_ENV === "development" ||
    window.location.search.includes("debug=true")
);

// Get user ID for API calls
const userId = user.value.id.toString();

// Load tasks from API
const loadTasks = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await apiService.getTasks(userId);
    tasks.value = response || [];
    if (isDebugMode.value) {
      console.log("Loaded tasks:", tasks.value);
    }
  } catch (err) {
    console.error("Error loading tasks:", err);
    error.value = "Failed to load tasks: " + (err.message || err);
  } finally {
    isLoading.value = false;
  }
};

// Add new task
const addTask = async (taskData) => {
  try {
    if (isDebugMode.value) {
      console.log("Adding task:", taskData);
    }
    const newTask = await apiService.createTask(userId, taskData);
    tasks.value.unshift(newTask);
  } catch (err) {
    console.error("Error adding task:", err);
    error.value = "Failed to add task: " + (err.message || err);
  }
};

// Update existing task
const updateTask = async (taskData) => {
  try {
    if (isDebugMode.value) {
      console.log("Updating task:", taskData);
    }
    const updatedTask = await apiService.updateTask(
      userId,
      taskData.id,
      taskData
    );
    const index = tasks.value.findIndex((t) => t.id === taskData.id);
    if (index !== -1) {
      tasks.value[index] = updatedTask;
      // Force reactivity update
      tasks.value = [...tasks.value];
    }
  } catch (err) {
    console.error("Error updating task:", err);
    error.value = "Failed to update task: " + (err.message || err);
  }
};

// Remove task
const removeTask = async (taskId) => {
  try {
    if (isDebugMode.value) {
      console.log("Removing task:", taskId);
    }
    await apiService.deleteTask(userId, taskId);
    tasks.value = tasks.value.filter((task) => task.id !== taskId);
  } catch (err) {
    console.error("Error removing task:", err);
    error.value = "Failed to remove task: " + (err.message || err);
  }
};

// Debug helper
const clearLocalStorage = () => {
  localStorage.removeItem(`telegram-tasks-${userId}`);
  window.location.reload();
};

onMounted(() => {
  // Initialize Telegram Mini App
  telegramService.init();

  // Load tasks from API
  loadTasks();

  // Set up Telegram main button if needed
  if (window.Telegram?.WebApp) {
    telegramService.showMainButton("Back to Bot", () => {
      window.Telegram.WebApp.openTelegramLink(BOT_LINK);
      telegramService.close();
    });
  }

  // Apply theme based on Telegram theme parameters
  if (tg?.themeParams) {
    // Check if it's a dark theme
    if (
      tg.themeParams.bg_color &&
      (tg.themeParams.bg_color.toLowerCase() === "#000000" ||
        tg.themeParams.bg_color.toLowerCase() === "#1f2937" ||
        isColorDark(tg.themeParams.bg_color))
    ) {
      document.documentElement.classList.add("dark-theme");
    }
  }

  // Log debug info
  if (isDebugMode.value) {
    console.log("Telegram Mini App initialized for user:", user.value);
  }
});

// Helper to determine if a color is dark
function isColorDark(hexColor) {
  // Remove the # if present
  hexColor = hexColor.replace("#", "");

  // Parse the hex color
  const r = parseInt(hexColor.substr(0, 2), 16);
  const g = parseInt(hexColor.substr(2, 2), 16);
  const b = parseInt(hexColor.substr(4, 2), 16);

  // Calculate relative luminance
  const luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255;

  // If luminance is less than 0.5, it's a dark color
  return luminance < 0.5;
}
</script>
