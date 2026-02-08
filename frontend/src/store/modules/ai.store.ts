import { store } from "@/store";
import { defineStore } from "pinia";
import AIServiceAPI, { ProviderOut } from "@/api/module_system/ai_service";

export const useAIStore = defineStore("ai", () => {
  const providers = ref<ProviderOut[]>([]);
  const loading = ref(false);

  async function fetchProviders() {
    loading.value = true;
    try {
      const res = await AIServiceAPI.listProviders();
      providers.value = res.data || [];
    } catch (e) {
      providers.value = [];
    } finally {
      loading.value = false;
    }
  }

  return {
    providers,
    loading,
    fetchProviders,
  };
});

export function useAIStoreHook() {
  return useAIStore(store);
}
