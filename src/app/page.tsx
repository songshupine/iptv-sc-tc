// src/app/page.tsx
"use client"

import { useState, useEffect } from 'react';

export default function Home() {
  const [htmlContent, setHtmlContent] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchAndConvert = async () => {
      try {
        // 1. 获取本地 public 目录下的 readme.md
        const mdRes = await fetch('/readme.md');
        if (!mdRes.ok) throw new Error('获取 README.md 失败');
        const mdText = await mdRes.text();

        // 2. 调用 Python 转换接口 (增加 5秒超时控制)
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 5000); 

        const pyRes = await fetch('/api/convertmarkdown/convertmarkdown', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ markdown: mdText }),
          signal: controller.signal,
        });

        clearTimeout(timeoutId);

        if (!pyRes.ok) {
          throw new Error(`Python 接口请求失败: ${pyRes.status} ${pyRes.statusText}`);
        }
        
        const data = await pyRes.json();
        
        // 如果 Python 端返回了错误信息
        if (data.error) throw new Error(data.error);

        setHtmlContent(data.html);
      } catch (err) {
        console.error('转换 Markdown 失败:', err);
        // 使用类型断言，安全地获取错误信息
        const errorMessage = err instanceof Error ? err.message : '未知错误';
        setError(errorMessage);
      } finally {
        setLoading(false);
      }
    };

    fetchAndConvert();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black text-white">
        正在通过 Python 转换文档...
      </div>
    );
  }

  // 如果发生错误，直接在黑底上显示红字
  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-black text-red-500 p-8 text-center">
        <div>
          <h1 className="text-2xl font-bold mb-4">转换失败</h1>
          <p>{error}</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-black text-white p-8">
      <div 
        className="max-w-4xl mx-auto prose prose-invert"
        dangerouslySetInnerHTML={{ __html: htmlContent }} 
      />
    </div>
  );
}
