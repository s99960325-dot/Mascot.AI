// 临时类型声明，避免缺少第三方库的全局类型导致编译失败
declare module "element-plus/global";
declare module "vite/client";

// 如果有其他第三方库缺少类型声明，可以在此处补充
