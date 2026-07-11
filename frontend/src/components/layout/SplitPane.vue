<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from "vue";

interface Props {
  defaultWidth?: number;
  minWidth?: number;
  maxWidth?: number;
  storageKey?: string;
}

const props = withDefaults(defineProps<Props>(), {
  defaultWidth: 280,
  minWidth: 220,
  maxWidth: 500,
  storageKey: "split-pane-width",
});

const width = ref(props.defaultWidth);

const resizing = ref(false);

function startResize() {
  resizing.value = true;

  document.body.style.cursor = "col-resize";
}

function stopResize() {
  resizing.value = false;

  document.body.style.cursor = "";
}

function resize(event: MouseEvent) {
  if (!resizing.value) {
    return;
  }

  const nextWidth = Math.min(
    props.maxWidth,
    Math.max(props.minWidth, event.clientX),
  );

  width.value = nextWidth;

  localStorage.setItem(props.storageKey, String(nextWidth));
}

onMounted(() => {
  const saved = localStorage.getItem(props.storageKey);

  if (saved) {
    width.value = Number(saved);
  }

  window.addEventListener("mousemove", resize);

  window.addEventListener("mouseup", stopResize);
});

onBeforeUnmount(() => {
  window.removeEventListener("mousemove", resize);

  window.removeEventListener("mouseup", stopResize);
});
</script>

<template>
  <div class="split-pane">
    <div
      class="left"
      :style="{
        width: `${width}px`,
      }"
    >
      <slot name="left" />
    </div>

    <div class="divider" @mousedown="startResize" />

    <div class="right">
      <slot name="right" />
    </div>
  </div>
</template>

<style scoped>
.split-pane {
  display: flex;
  width: 100%;
  height: 100%;
}

.left {
  overflow: auto;
}

.right {
  flex: 1;
  overflow: hidden;
}

.divider {
  width: 6px;
  cursor: col-resize;
  background: #2d2d2d;
  transition: background 0.15s;
}

.divider:hover {
  background: #4b5563;
}
</style>
