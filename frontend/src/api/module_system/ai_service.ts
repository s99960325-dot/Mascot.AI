import request from "@/utils/request";

const API_PATH = "/admin/ai_service";

const AIServiceAPI = {
  listProviders() {
    return request<ApiResponse<ProviderOut[]>>({
      url: `${API_PATH}/providers`,
      method: "get",
    });
  },
};

export default AIServiceAPI;

export interface ProviderOut {
  id: string;
  name: string;
  status?: string;
}
