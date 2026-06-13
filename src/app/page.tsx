import { getReadmeHtml } from "@/lib/api";

export default async function HomePage() {
  let html: string | null = null;
  let error: string | null = null;

  try {
    // ✅ 直接调用 Edge Function 接口
    const data = await getReadmeHtml();
    html = data.html;
  } catch (err) {
    error = err instanceof Error ? err.message : "Unknown error";
  }

  return (
    <main className="container mx-auto p-4 bg-white dark:bg-gray-900">
      <h1 className="text-2xl font-bold mb-4">四川IPTV订阅源</h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
          加载失败: {error}
        </div>
      )}

      {html && (
        <article
          className="prose dark:prose-invert max-w-none"
          dangerouslySetInnerHTML={{ __html: html }}
        />
      )}
    </main>
  );
}
