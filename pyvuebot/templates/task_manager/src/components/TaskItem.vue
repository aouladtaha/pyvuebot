<template>
  <div
    class="task-item relative group overflow-hidden"
    :class="task.status === 'completed' ? 'opacity-85' : ''"
  >
    <div
      class="flex items-start p-4 rounded-lg shadow-sm hover:shadow-md transition-all duration-200"
      style="border-radius: var(--radius-lg); overflow: hidden"
      :style="{
        backgroundColor: tg?.themeParams?.bg_color || 'var(--color-bg)',
        boxShadow: 'var(--shadow-md)',
        borderLeft: '4px solid transparent',
        borderLeftColor:
          task.priority === 'high'
            ? 'var(--color-priority-high)'
            : task.priority === 'medium'
            ? 'var(--color-priority-medium)'
            : 'var(--color-priority-low)',
      }"
    >
      <!-- Background pattern -->
      <div
        class="absolute inset-0 pattern-dots opacity-5 pointer-events-none"
      ></div>

      <!-- Status toggle button with animation -->
      <button
        @click="handleStatusChange"
        class="flex-shrink-0 w-6 h-6 mt-0.5 mr-3 rounded-full border-2 flex items-center justify-center transition-all duration-300 hover:scale-110"
        :style="{
          borderColor:
            task.status === 'completed'
              ? 'var(--color-success)'
              : 'var(--color-border)',
          backgroundColor:
            task.status === 'completed'
              ? 'var(--color-success)'
              : 'transparent',
        }"
      >
        <svg
          v-if="task.status === 'completed'"
          class="w-4 h-4 text-white"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
          />
        </svg>
      </button>

      <!-- Task content -->
      <div class="flex-grow min-w-0">
        <!-- Task title with emoji based on status -->
        <h3
          class="font-medium truncate flex items-center gap-1"
          :class="task.status === 'completed' ? 'line-through' : ''"
          :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
        >
          <span v-if="task.status === 'in_progress'" class="text-sm">⏳</span>
          <span v-if="task.status === 'completed'" class="text-sm">✅</span>
          <span v-if="task.status === 'pending'" class="text-sm">📝</span>
          {{ task.task_name }}
        </h3>

        <!-- Description with better styling -->
        <div
          v-if="task.description"
          class="mt-2 text-sm rounded-md p-2"
          :style="{
            backgroundColor: 'rgba(0,0,0,0.03)',
            color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)',
          }"
        >
          {{ task.description }}
        </div>

        <!-- Meta information with modern badges -->
        <div class="mt-2 flex flex-wrap gap-2 text-xs">
          <span
            class="px-3 py-1 rounded-full badge"
            :style="{
              background:
                task.priority === 'high'
                  ? 'var(--gradient-priority-high)'
                  : task.priority === 'medium'
                  ? 'var(--gradient-priority-medium)'
                  : 'var(--gradient-priority-low)',
              color: task.priority === 'medium' ? '#7C2D12' : 'white',
            }"
          >
            {{
              task.priority === "high"
                ? "🔴"
                : task.priority === "medium"
                ? "🟡"
                : "🔵"
            }}
            {{ task.priority.charAt(0).toUpperCase() + task.priority.slice(1) }}
          </span>

          <span
            v-if="task.status === 'in_progress'"
            class="px-3 py-1 rounded-full badge"
            style="background: var(--gradient-secondary); color: white"
          >
            ⏳ In Progress
          </span>

          <span
            v-if="task.deadline"
            class="px-3 py-1 rounded-full badge"
            :style="{
              background: isOverdue
                ? 'var(--gradient-priority-high)'
                : 'linear-gradient(135deg, #94A3B8 0%, #CBD5E1 100%)',
              color: 'white',
            }"
          >
            📅 {{ formatDate(task.deadline) }}
          </span>
        </div>
      </div>

      <!-- Actions -->
      <div class="flex gap-2 ml-4">
        <button
          @click="$emit('edit', task)"
          class="p-1.5 rounded-full transition-all duration-200 hover:scale-110"
          :style="{
            backgroundColor: 'var(--color-bg-tertiary)',
            color: 'var(--color-primary)',
          }"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z"
            />
          </svg>
        </button>

        <button
          @click="$emit('remove', task.id)"
          class="p-1.5 rounded-full transition-all duration-200 hover:scale-110"
          :style="{
            backgroundColor: 'var(--color-bg-tertiary)',
            color: 'var(--color-error)',
          }"
        >
          <svg
            class="w-4 h-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
            />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  task: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(["edit", "remove", "update"]);
const tg = window.Telegram?.WebApp;

const isOverdue = computed(() => {
  if (!props.task.deadline) return false;
  return new Date(props.task.deadline) < new Date();
});

const handleStatusChange = () => {
  const nextStatus =
    props.task.status === "completed" ? "pending" : "completed";
  emit("update", { ...props.task, status: nextStatus });
};

const formatDate = (dateString) => {
  try {
    return new Date(dateString).toLocaleDateString();
  } catch (e) {
    return dateString;
  }
};
</script>

<style scoped>
.task-item {
  transition: all 0.3s ease-in-out;
}

.task-item:hover {
  transform: translateY(-3px);
}
</style>
