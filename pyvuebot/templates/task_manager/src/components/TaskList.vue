<template>
  <div class="mt-4 space-y-4">
    <!-- Modernized Add Task Button -->
    <div class="flex justify-end mb-4">
      <button
        @click="showTaskForm = !showTaskForm"
        class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full shadow-md hover:shadow-lg transition-all duration-300 transform hover:scale-105"
        :style="{
          background: 'var(--gradient-primary)',
          color: tg?.themeParams?.button_text_color || '#ffffff',
        }"
      >
        <svg
          class="w-5 h-5"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 6v6m0 0v6m0-6h6m-6 0H6"
          />
        </svg>
        <span class="text-sm font-medium">New Task</span>
      </button>
    </div>

    <!-- Task Form -->
    <task-form
      :is-visible="showTaskForm"
      :is-submitting="isSubmitting"
      :editing-task="editingTask"
      @add-task="handleAddTask"
      @update-task="handleUpdateTask"
      @close="closeTaskForm"
    />

    <!-- Modernized Filters -->
    <div class="flex gap-3 overflow-x-auto py-3 px-1 -mx-1 scrollbar-hidden">
      <div
        class="px-2 py-1 rounded-lg flex items-center"
        :style="{
          backgroundColor:
            tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
          borderLeft: '3px solid var(--color-primary)',
        }"
      >
        <span class="text-sm mr-1">🔍</span>
        <select
          v-for="(options, filter) in filters"
          :key="filter"
          v-model="activeFilters[filter]"
          class="px-2 py-1 rounded-lg text-sm transition-all duration-200 border-0 focus:ring-0 bg-transparent"
          :style="{
            color: tg?.themeParams?.text_color || 'var(--color-text)',
          }"
          @change="applyFilters"
        >
          <option
            v-for="opt in options"
            :key="opt.value"
            :value="opt.value"
            :style="{
              backgroundColor:
                tg?.themeParams?.secondary_bg_color ||
                'var(--color-bg-secondary)',
              color: tg?.themeParams?.text_color || 'var(--color-text)',
            }"
          >
            {{ opt.label }}
          </option>
        </select>
      </div>
    </div>

    <!-- Loading State -->
    <div
      v-if="isSubmitting"
      class="fixed inset-0 bg-black bg-opacity-30 backdrop-blur-sm flex items-center justify-center z-50"
    >
      <div
        class="p-6 rounded-xl shadow-xl"
        :style="{
          backgroundColor: tg?.themeParams?.bg_color || 'var(--color-bg)',
        }"
      >
        <div class="flex flex-col items-center">
          <div
            class="animate-spin rounded-full h-12 w-12 border-b-3 mb-3"
            :style="{
              borderColor: 'var(--color-primary)',
            }"
          ></div>
          <p class="text-sm font-medium">Processing...</p>
        </div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="filteredTasks.length === 0" class="text-center p-8 card">
      <div class="inline-flex flex-col items-center opacity-60">
        <div
          class="w-16 h-16 mb-4 rounded-full flex items-center justify-center"
          :style="{
            background: 'var(--gradient-secondary)',
            opacity: '0.7',
          }"
        >
          <svg
            class="w-8 h-8 text-white"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="1.5"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
            />
          </svg>
        </div>
        <h3 class="text-lg font-medium mb-1">
          {{ tasks.length === 0 ? "No Tasks Yet" : "No Matching Tasks" }}
        </h3>
        <p class="text-sm" :style="{ color: 'var(--color-text-secondary)' }">
          {{
            tasks.length === 0
              ? "Create your first task to get started!"
              : "Try changing your filters to see more tasks."
          }}
        </p>
      </div>
    </div>

    <!-- Task List with Animations -->
    <TransitionGroup name="task-list" tag="div" class="space-y-3">
      <template v-for="task in filteredTasks" :key="task.id">
        <task-item
          :task="task"
          :class="{ 'opacity-50 pointer-events-none': isSubmitting }"
          @update="handleUpdate"
          @remove="$emit('remove-task', $event)"
          @edit="handleEdit"
        />
      </template>
    </TransitionGroup>
  </div>
</template>

<style scoped>
/* Enhanced animations */
.task-list-move,
.task-list-enter-active,
.task-list-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.task-list-enter-from,
.task-list-leave-to {
  opacity: 0;
  transform: scale(0.9) translateY(30px);
}

.task-list-leave-active {
  position: absolute;
  width: 100%;
}

.scrollbar-hidden::-webkit-scrollbar {
  display: none;
}

.scrollbar-hidden {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>

<script setup>
import { ref, computed } from "vue";
import TaskItem from "./TaskItem.vue";
import TaskForm from "./TaskForm.vue";

const props = defineProps({
  tasks: {
    type: Array,
    required: true,
  },
});

const emit = defineEmits(["update-task", "remove-task", "add-task"]);
const tg = window.Telegram?.WebApp;

// Form state
const showTaskForm = ref(false);
const isSubmitting = ref(false);
const editingTask = ref(null);

// Filters
const filters = {
  status: [
    { value: "", label: "📋 All Status" },
    { value: "pending", label: "📝 Todo" },
    { value: "in_progress", label: "⏳ In Progress" },
    { value: "completed", label: "✅ Completed" },
  ],
  priority: [
    { value: "", label: "🌟 All Priority" },
    { value: "high", label: "🔴 High" },
    { value: "medium", label: "🟡 Medium" },
    { value: "low", label: "🔵 Low" },
  ],
  sort: [
    { value: "deadline|asc", label: "📅 Deadline ↑" },
    { value: "priority|desc", label: "🏷️ Priority ↓" },
    { value: "created_at|desc", label: "🆕 Newest" },
  ],
};

const activeFilters = ref({
  status: "",
  priority: "",
  sort: "created_at|desc",
});

// Methods
const handleAddTask = (taskData) => {
  emit("add-task", taskData);
};

const handleUpdateTask = (taskData) => {
  emit("update-task", taskData);
};

const handleUpdate = (task) => {
  emit("update-task", task);
};

const handleEdit = (task) => {
  editingTask.value = task;
  showTaskForm.value = true;
};

const closeTaskForm = () => {
  showTaskForm.value = false;
  editingTask.value = null;
};

// Filters don't need to explicitly call applyFilters since we're using computed property
const applyFilters = () => {
  // This function is kept for the template, but filtering is handled by the computed property
};

// Computed
const filteredTasks = computed(() => {
  let result = [...props.tasks];

  if (activeFilters.value.status) {
    result = result.filter(
      (task) => task.status === activeFilters.value.status
    );
  }

  if (activeFilters.value.priority) {
    result = result.filter(
      (task) => task.priority === activeFilters.value.priority
    );
  }

  const [sortField, direction] = activeFilters.value.sort.split("|");
  if (sortField && direction) {
    const priorityValues = { low: 1, medium: 2, high: 3 };

    result.sort((a, b) => {
      const valueA =
        sortField === "priority" ? priorityValues[a[sortField]] : a[sortField];
      const valueB =
        sortField === "priority" ? priorityValues[b[sortField]] : b[sortField];
      return direction === "asc"
        ? valueA > valueB
          ? 1
          : -1
        : valueA < valueB
        ? 1
        : -1;
    });
  }

  return result;
});
</script>
