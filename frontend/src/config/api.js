/**
 * API配置文件
 * 包含API基础URL和AI问答功能所需的API参数
 *
 * 注意：所有真正敏感的配置都放在 frontend/.env 里，不写进代码。
 * .env 已在根目录 .gitignore 中被排除，不会提交到 Git。
 * 换台电脑请先复制 .env.example 为 .env 再填入自己的值。
 */

// API基础URL配置
export const apiConfig = {
  // 后端API基础URL
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
}

export const aiChatConfig = {
  // OpenAI 兼容模式的 API 地址
  apiEndpoint:
    import.meta.env.VITE_AI_API_ENDPOINT ||
    'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',

  // API Key（从 .env 读取，不要硬编码在代码里）
  apiKey: import.meta.env.VITE_AI_API_KEY || '',

  // 使用的模型
  model: import.meta.env.VITE_AI_MODEL || 'qwen3-max-preview',
}
