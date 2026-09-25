import { ChatWorkspace } from "@/components/chat-workspace";
import { API_URL } from "@/lib/config";


async function getWatchlist() {
  const res = await fetch(`${API_URL}/companies`, { cache: "no-store" });
  if (!res.ok) return [];
  return res.json();
}

export default async function Home() {
  const watchlist = await getWatchlist();
  return <ChatWorkspace initialWatchlist={watchlist} />;
}