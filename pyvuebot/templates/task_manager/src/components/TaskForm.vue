<template>
  <Dialog v-model="isDialogVisible" @update:modelValue="closeForm">
    <form @submit.prevent="handleSubmit">
      <!-- Title -->
      <div class="mb-6 text-center">
        <h3
          class="text-lg font-bold"
          :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
        >
          {{ editingTask ? "✏️ Edit Task" : "✨ New Task" }}
        </h3>
      </div>

      <!-- Form Fields -->
      <div class="space-y-4">
        <!-- Task Name -->
        <div>
          <input
            v-model="formData.task_name"
            type="text"
            placeholder="What needs to be done?"
            class="w-full rounded-lg px-4 py-3 transition-all duration-200"
            :class="{ 'ring-2 ring-red-500': error && !formData.task_name }"
            :style="{
              backgroundColor:
                tg?.themeParams?.secondary_bg_color ||
                'var(--color-bg-secondary)',
              color: tg?.themeParams?.text_color || 'var(--color-text)',
              borderColor: tg?.themeParams?.hint_color || 'var(--color-border)',
            }"
          />
          <p
            v-if="error && !formData.task_name"
            class="mt-1 text-xs"
            style="color: var(--color-error)"
          >
            Task name is required
          </p>
        </div>

        <!-- Description -->
        <textarea
          v-model="formData.description"
          placeholder="Add details... (optional)"
          rows="3"
          class="w-full rounded-lg px-4 py-3 transition-all duration-200"
          :style="{
            backgroundColor:
              tg?.themeParams?.secondary_bg_color ||
              'var(--color-bg-secondary)',
            color: tg?.themeParams?.text_color || 'var(--color-text)',
            borderColor: tg?.themeParams?.hint_color || 'var(--color-border)',
          }"
        ></textarea>

        <!-- Priority & Status -->
        <div class="grid grid-cols-2 gap-4">
          <div class="relative">
            <select
              v-model="formData.priority"
              class="rounded-lg pl-10 pr-4 py-3 w-full appearance-none transition-all duration-200"
              :style="{
                backgroundColor:
                  tg?.themeParams?.secondary_bg_color ||
                  'var(--color-bg-secondary)',
                color: tg?.themeParams?.text_color || 'var(--color-text)',
                borderColor:
                  tg?.themeParams?.hint_color || 'var(--color-border)',
              }"
            >
              <option value="low">🔵 Low</option>
              <option value="medium">🟡 Medium</option>
              <option value="high">🔴 High</option>
            </select>
            <div
              class="absolute top-0 bottom-0 left-0 flex items-center pl-3 pointer-events-none"
            >
              <span class="text-lg">🏷️</span>
            </div>
          </div>

          <div class="relative">
            <select
              v-model="formData.status"
              class="rounded-lg pl-10 pr-4 py-3 w-full appearance-none transition-all duration-200"
              :style="{
                backgroundColor:
                  tg?.themeParams?.secondary_bg_color ||
                  'var(--color-bg-secondary)',
                color: tg?.themeParams?.text_color || 'var(--color-text)',
                borderColor:
                  tg?.themeParams?.hint_color || 'var(--color-border)',
              }"
            >
              <option value="pending">📝 Todo</option>
              <option value="in_progress">⏳ In Progress</option>
              <option value="completed">✅ Done</option>
            </select>
            <div
              class="absolute top-0 bottom-0 left-0 flex items-center pl-3 pointer-events-none"
            >
              <span class="text-lg">📊</span>
            </div>
          </div>
        </div>

        <!-- Deadline -->
        <div class="relative">
          <input
            v-model="formData.deadline"
            type="date"
            class="w-full rounded-lg pl-10 pr-4 py-3 transition-all duration-200"
            :style="{
              backgroundColor:
                tg?.themeParams?.secondary_bg_color ||
                'var(--color-bg-secondary)',
              color: tg?.themeParams?.text_color || 'var(--color-text)',
              borderColor: tg?.themeParams?.hint_color || 'var(--color-border)',
            }"
          />
          <div
            class="absolute top-0 bottom-0 left-0 flex items-center pl-3 pointer-events-none"
          >
            <span class="text-lg">📅</span>
          </div>
        </div>

        <!-- Submit Button -->
        <button
          type="submit"
          class="w-full rounded-lg px-4 py-3 font-medium shadow-lg transition-all duration-200 hover:scale-105 hover:shadow-xl"
          :disabled="isSubmitting"
          :style="{
            background: 'var(--gradient-primary)',
            color: tg?.themeParams?.button_text_color || '#ffffff',
            opacity: isSubmitting ? '0.7' : '1',
          }"
        >
          <span v-if="isSubmitting" class="inline-flex items-center gap-2">
            <svg
              class="h-4 w-4 animate-spin"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            Saving...
          </span>
          <span v-else>
            {{ editingTask ? "✨ Update Task" : "✨ Add Task" }}
          </span>
        </button>
      </div>
    </form>
  </Dialog>
</template>

<script setup>
import { ref, reactive, watch, computed } from "vue";
import Dialog from "./base/Dialog.vue";

const props = defineProps({
  isVisible: Boolean,
  isSubmitting: Boolean,
  editingTask: {
    type: Object,
    default: null,
  },
});

const emit = defineEmits(["add-task", "update-task", "close"]);
const error = ref(false);
const tg = window.Telegram?.WebApp;

const isDialogVisible = computed({
  get: () => props.isVisible,
  set: (value) => !value && emit("close"),
});

const defaultForm = {
  task_name: "",
  description: "",
  priority: "medium",
  status: "pending",
  deadline: "",
};

const formData = reactive({ ...defaultForm });

watch(
  () => props.editingTask,
  (newTask) => {
    if (newTask) {
      Object.assign(formData, {
        ...newTask,
        deadline: newTask.deadline
          ? new Date(newTask.deadline).toISOString().split("T")[0]
          : "",
      });
    } else {
      Object.assign(formData, defaultForm);
    }
  },
  { immediate: true }
);

const handleSubmit = () => {
  if (!formData.task_name.trim()) {
    error.value = true;
    return;
  }

  error.value = false;
  const taskData = {
    ...formData,
    deadline: formData.deadline
      ? new Date(formData.deadline).toISOString()
      : null,
  };

  if (props.editingTask) {
    emit("update-task", { id: props.editingTask.id, ...taskData });
  } else {
    emit("add-task", taskData);
  }

  closeForm();
};

const closeForm = () => {
  emit("close");
  Object.assign(formData, defaultForm);
  error.value = false;
};
</script>
