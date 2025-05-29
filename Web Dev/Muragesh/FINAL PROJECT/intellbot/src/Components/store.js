import { create } from "zustand";

const useStore = create((set) => ({
  ema: "i need a email", // Default value
  setEm: (newEm) => set({ ema: newEm }), // Fix: Change 'em' to 'ema'
}));

export default useStore;
