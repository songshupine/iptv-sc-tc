// src/app/page.tsx
"use client"

import { useState, useEffect } from 'react';

export default function Home() {
  const [htmlContent, setHtmlContent] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAndConvert = async () => {
      try {
        // 1. 获取原始 Markdown 文本（假设放在 public 目录下）
        const mdRes = await fetch('/readme.md');
        const mdText = await mdRes.text();

        // 2. 调用同域下的 FastAPI 接口
        const pyRes = await fetch('/api/convert-markdown', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ markdown: mdText }),
        });
        
        const data = await pyRes.json();
        setHtmlContent(data.html);
      } catch (err) {
        console.error('转换 Markdown 失败:', err);
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

  return (
    <div className="min-h-screen bg-black text-white p-8">
      <div 
        className="max-w-4xl mx-auto prose prose-invert"
        dangerouslySetInnerHTML={{ __html: htmlContent }} 
      />
    </div>
  );
}
