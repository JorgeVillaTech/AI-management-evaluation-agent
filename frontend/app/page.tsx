import { ChatWorkspace } from "@/components/chat-workspace";

async function getWatchlist() {
  const res = await fetch("http://localhost:8000/companies", { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export default async function Home() {
  const watchlist = await getWatchlist();
  return <ChatWorkspace initialWatchlist={watchlist} />;
}