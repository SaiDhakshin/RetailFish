# RetailFish Keyboard Shortcuts Guide

Keyboard shortcuts are enabled when focus is **not** inside input fields (input, textarea, select, or contenteditable elements). This allows fast navigation without losing typing capability in search fields.

## Navigation Shortcuts

| Shortcut | Action | Context |
|----------|--------|---------|
| **↑ Arrow Up** | Select previous stock | Watchlist or Scanner view |
| **↓ Arrow Down** | Select next stock | Watchlist or Scanner view |
| **Home** | Jump to first stock | Watchlist or Scanner view |
| **End** | Jump to last stock | Watchlist or Scanner view |
| **Enter** | Select current stock (re-emit) | Watchlist or Scanner view |

## Mode Switching

| Shortcut | Action |
|----------|--------|
| **S** | Switch to Scanner mode |
| **W** | Switch to Watchlist mode |

## Scanner Shortcuts

| Shortcut | Action | Availability |
|----------|--------|---|
| **R** | Run the current scanner with selected filters | Scanner mode |
| **A** | Add selected scanner result to watchlist | Scanner mode (when stock not already in watchlist) |

## Watchlist Shortcuts

| Shortcut | Action | Availability |
|----------|--------|---|
| **Delete / Backspace** | Remove selected stock from watchlist | Watchlist mode (with confirmation) |
| **A** | Add selected scanner stock to watchlist | Scanner mode only |

## Dialog Control

| Shortcut | Action |
|----------|--------|
| **Escape** | Close any open dialogs or popups |

## Behavior Details

### Auto-Scroll
When navigating with arrow keys or Home/End shortcuts, the selected stock automatically scrolls into view using smooth scrolling. The viewport centers on the selected item when it's outside the current visible area.

### Selection Highlight
The selected stock remains visually highlighted with the application's accent color (green). This highlight persists as you navigate and is updated in real-time.

### Confirmation Dialogs
Destructive actions like removing a stock from a watchlist require confirmation. A browser confirmation dialog will appear asking to confirm the deletion.

### Input Focus Detection
All keyboard shortcuts are automatically disabled when you're typing inside:
- Text input fields (`<input>`)
- Text areas (`<textarea>`)
- Select dropdowns (`<select>`)
- Contenteditable elements

This prevents shortcuts from interfering with your typing while searching or entering data.

## Examples

### Quickly Browse Watchlist
1. Press **W** to switch to Watchlist view
2. Use **↑** and **↓** to navigate through stocks
3. Press **Home** to jump to the first stock
4. Press **End** to jump to the last stock

### Find and Add to Watchlist
1. Press **S** to switch to Scanner mode
2. Configure filters in the Scanner panel
3. Press **R** to run the scanner
4. Use **↑** and **↓** to navigate results
5. Press **A** to add the selected stock to your watchlist

### Clean Up Watchlist
1. Press **W** to switch to Watchlist view
2. Use **↑** and **↓** to find stocks to remove
3. Press **Delete** or **Backspace** to remove
4. Confirm removal in the dialog

## Tips for Power Users

- **Quick Mode Switching**: Keep alternating between S and W to compare scanner results with your watchlist
- **Keyboard-Only Navigation**: Never touch the mouse! Use keyboard shortcuts for the fastest workflow
- **Familiar Keybindings**: Shortcuts follow common conventions (S = Scanner, W = Watchlist, R = Run, A = Add)
- **Visual Feedback**: All interactive elements show tooltip hints with their keyboard shortcuts (hover to see)
