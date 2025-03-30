<template>
  <div
    class="relative overflow-hidden rounded-2xl p-4 mb-5"
    :style="{
      backgroundColor:
        tg?.themeParams?.secondary_bg_color || 'var(--color-bg-secondary)',
      boxShadow: 'var(--shadow-md)',
    }"
  >
    <!-- Background pattern -->
    <div
      class="absolute inset-0 pattern-dots opacity-5 pointer-events-none"
    ></div>

    <!-- Content -->
    <div class="flex items-center gap-4 relative z-10">
      <!-- Avatar with gradient border -->
      <div class="relative">
        <div
          class="absolute inset-0 rounded-full bg-gradient-to-r from-pink-500 via-purple-500 to-indigo-500 p-0.5 animate-spin-slow"
        ></div>
        <div
          class="w-14 h-14 rounded-full flex items-center justify-center text-xl font-bold text-white relative z-10"
          :style="{
            background: 'var(--gradient-primary)',
          }"
        >
          {{ user.first_name.charAt(0)
          }}{{ user.last_name ? user.last_name.charAt(0) : "" }}
        </div>
      </div>

      <!-- User info -->
      <div class="flex-1">
        <h2
          class="text-base font-bold flex items-center gap-1"
          :style="{ color: tg?.themeParams?.text_color || 'var(--color-text)' }"
        >
          {{ user.first_name }} {{ user.last_name }}
          <!-- <span class="text-xs bg-blue-500 text-white px-1.5 py-0.5 rounded-md"
            >User</span
          > -->
        </h2>
        <p
          class="text-xs"
          :style="{
            color: tg?.themeParams?.hint_color || 'var(--color-text-secondary)',
          }"
        >
          @{{ user.username || "no_username" }}
        </p>
      </div>

      <!-- Task statistics with fun animations -->
      <div class="flex gap-2">
        <div
          class="stat-card flex flex-col items-center p-2 rounded-lg relative overflow-hidden hover:scale-105 transition-transform"
          :style="{
            background: 'var(--gradient-priority-low)',
            boxShadow: 'var(--shadow-sm)',
          }"
        >
          <span class="text-white font-bold text-lg">{{
            taskStats.pending
          }}</span>
          <span class="text-white text-xs">Todo</span>
        </div>

        <div
          class="stat-card flex flex-col items-center p-2 rounded-lg relative overflow-hidden hover:scale-105 transition-transform"
          :style="{
            background: 'var(--gradient-success)',
            boxShadow: 'var(--shadow-sm)',
          }"
        >
          <span class="text-white font-bold text-lg">{{
            taskStats.completed
          }}</span>
          <span class="text-white text-xs">Done</span>
        </div>
      </div>
    </div>

    <!-- Progress bar if there are tasks -->
    <div
      v-if="taskStats.total > 0"
      class="mt-3 bg-gray-200 dark:bg-gray-700 rounded-full h-2 overflow-hidden"
    >
      <div
        class="h-full transition-all duration-500"
        :style="{
          width: `${(taskStats.completed / taskStats.total) * 100}%`,
          background: 'var(--gradient-primary)',
        }"
      ></div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  user: {
    type: Object,
    required: true,
  },
  tasks: {
    type: Array,
    default: () => [],
  },
});

const tg = window.Telegram?.WebApp;

const taskStats = computed(() => ({
  total: props.tasks.length,
  completed: props.tasks.filter((t) => t.status === "completed").length,
  pending: props.tasks.filter((t) => t.status !== "completed").length,
}));
</script>

<style scoped>
.animate-spin-slow {
  animation: spin 8s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.stat-card {
  min-width: 60px;
}

.stat-card::before {
  content: "";
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.3) 0%,
    transparent 60%
  );
  opacity: 0;
  transition: opacity 0.3s;
}

.stat-card:hover::before {
  opacity: 1;
}
</style>
