import { onMounted, onUnmounted } from "vue";

export interface KeyboardShortcutCallbacks {
  next?: () => void;
  previous?: () => void;
  first?: () => void;
  last?: () => void;
  selectCurrent?: () => void;
  runScanner?: () => void;
  showScanner?: () => void;
  showWatchlists?: () => void;
  addToWatchlist?: () => void;
  removeFromWatchlist?: () => void;
  closeDialog?: () => void;
}

export function useKeyboardShortcuts(callbacks: KeyboardShortcutCallbacks) {
  const isInputFocused = (): boolean => {
    const activeElement = document.activeElement as HTMLElement;
    const tagName = activeElement?.tagName.toLowerCase();
    const isContentEditable = activeElement?.getAttribute("contenteditable") === "true";

    return (
      tagName === "input" ||
      tagName === "textarea" ||
      tagName === "select" ||
      isContentEditable
    );
  };

  const handleKeyDown = (event: KeyboardEvent): void => {
    if (isInputFocused()) {
      return;
    }

    switch (event.key) {
      case "ArrowDown":
        event.preventDefault();
        callbacks.next?.();
        break;

      case "ArrowUp":
        event.preventDefault();
        callbacks.previous?.();
        break;

      case "Home":
        event.preventDefault();
        callbacks.first?.();
        break;

      case "End":
        event.preventDefault();
        callbacks.last?.();
        break;

      case "Enter":
        event.preventDefault();
        callbacks.selectCurrent?.();
        break;

      case "s":
      case "S":
        event.preventDefault();
        callbacks.showScanner?.();
        break;

      case "w":
      case "W":
        event.preventDefault();
        callbacks.showWatchlists?.();
        break;

      case "r":
      case "R":
        event.preventDefault();
        callbacks.runScanner?.();
        break;

      case "a":
      case "A":
        event.preventDefault();
        callbacks.addToWatchlist?.();
        break;

      case "Delete":
      case "Backspace":
        event.preventDefault();
        callbacks.removeFromWatchlist?.();
        break;

      case "Escape":
        event.preventDefault();
        callbacks.closeDialog?.();
        break;

      default:
        break;
    }
  };

  onMounted(() => {
    window.addEventListener("keydown", handleKeyDown);
  });

  onUnmounted(() => {
    window.removeEventListener("keydown", handleKeyDown);
  });
}

export function scrollElementIntoView(element: HTMLElement | null): void {
  if (element) {
    element.scrollIntoView({
      behavior: "smooth",
      block: "nearest",
    });
  }
}
