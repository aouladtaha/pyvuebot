<template>
  <transition
    enter-active-class="transition duration-300 ease-out"
    enter-from-class="opacity-0 scale-95"
    enter-to-class="opacity-100 scale-100"
    leave-active-class="transition duration-200 ease-in"
    leave-from-class="opacity-100 scale-100"
    leave-to-class="opacity-0 scale-95"
  >
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 overflow-y-auto"
      @click.self="$emit('update:modelValue', false)"
    >
      <!-- Overlay with blur effect -->
      <div
        class="fixed inset-0 backdrop-blur-md"
        :style="{
          backgroundColor: 'rgba(0, 0, 0, 0.3)',
        }"
      ></div>

      <!-- Dialog -->
      <div class="flex min-h-full items-center justify-center p-4">
        <div
          class="relative w-full max-w-md rounded-2xl shadow-xl transform card"
          :style="{
            backgroundColor: tg?.themeParams?.bg_color || 'var(--color-bg)',
            boxShadow: 'var(--shadow-lg)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
          }"
        >
          <!-- Close button -->
          <button
            type="button"
            class="absolute -right-0 -top-0 z-10 rounded-full m-2 p-2 shadow-lg transition-all duration-200 hover:scale-110"
            :style="{
              background: 'var(--gradient-primary)',
              color: '#ffffff',
            }"
            @click="$emit('update:modelValue', false)"
          >
            <svg
              class="h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>

          <!-- Content with subtle pattern -->
          <div
            class="p-6 relative overflow-hidden"
            style="border-radius: var(--radius-lg)"
          >
            <div class="pattern-dots absolute inset-0 opacity-5"></div>
            <div class="relative">
              <slot></slot>
            </div>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script setup>
defineProps({
  modelValue: {
    type: Boolean,
    required: true,
  },
});

defineEmits(["update:modelValue"]);

const tg = window.Telegram?.WebApp;
</script>
