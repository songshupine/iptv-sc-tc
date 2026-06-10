export interface ReadmeResponse {
  html: string;
  source: string;
}

export async function getReadmeHtml(): Promise<ReadmeResponse> {
  const res = await fetch("https://tv.gotonas.com/api/readme", {
    method: "GET",
  });

  if (!res.ok) {
    throw new Error(`README API error: ${res.status}`);
  }

  return res.json();
}

