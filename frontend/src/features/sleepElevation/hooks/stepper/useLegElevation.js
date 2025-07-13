export function useLegElevation() {
  function elevateLegs() {
    console.log("[STEPPER] Elevating legs via stepper motor...");
    // Replace with GPIO, HTTP or WebSocket later
  }

  function lowerLegs() {
    console.log("[STEPPER] Lowering legs via stepper motor...");
  }

  return { elevateLegs, lowerLegs };
}
