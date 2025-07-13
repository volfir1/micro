    export function useSpeakerControl() {
  function playAlert(message = "Wake up! Snoring detected!") {
    // Replace this with backend GPIO/audio trigger
    console.log(`[SPEAKER] ${message}`);
  }

  return { playAlert };
}
