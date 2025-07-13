export function usePillowAdjustment() {
  function adjustPillow(angle) {
    // Replace this with GPIO / serial / HTTP POST, etc.
    console.log(`[PILLOW] Adjusting to angle: ${angle}°`);
  }

  return { adjustPillow };
}
