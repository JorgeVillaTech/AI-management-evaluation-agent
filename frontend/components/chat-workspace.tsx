"use client";
import { useState, useEffect } from "react";
import { CopilotChat, useAgent, useRenderTool } from "@copilotkit/react-core/v2";
import { z } from "zod";
import { CompanyProfileCard } from "./company-profile-card";
import { FormalReportCard } from "./formal-report-card";
import { MeetingBriefingCard } from "./meeting-briefing-card";
import { PortfolioSummaryCard } from "./portfolio-summary-card";
import { PeerComparisonCard } from "./peer-comparison-card";

interface Company {
    name: string;
    sector: string;
    risk_score: number;
}

interface ConversationSummary {
    id: number;
    thread_id: string;
    title: string;
}

function riskColor(score: number) {
    if (score >= 60) return "var(--risk-high)";
    if (score >= 35) return "var(--accent)";
    return "var(--risk-low)";
}

export function ChatWorkspace({ initialWatchlist }: { initialWatchlist: Company[] }) {
    const [isWatchlistOpen, setIsWatchlistOpen] = useState(false);
    const [isConversationsOpen, setIsConversationsOpen] = useState(false);
    const [lastReviewed, setLastReviewed] = useState<string | null>(null);
    const [conversations, setConversations] = useState<ConversationSummary[]>([]);
    const [activeThreadId, setActiveThreadId] = useState<string | undefined>(undefined);
    const [renamingId, setRenamingId] = useState<number | null>(null);
    const [renameValue, setRenameValue] = useState("");

    const { agent } = useAgent({ agentId: "default" });

    useEffect(() => {
        async function loadConversations() {
        const res = await fetch("http://localhost:8000/conversations");
        const list: ConversationSummary[] = await res.json();

        if (list.length === 0) {
            const created = await fetch("http://localhost:8000/conversations", { method: "POST" }).then((r) => r.json());
            setConversations([created]);
            setActiveThreadId(created.thread_id);
        } else {
            setConversations(list);
            setActiveThreadId(list[0].thread_id);
        }
        }
        loadConversations();
    }, []);

    // Titles the conversation you're currently in, using whatever messages it
    // actually has right now. Called right before switching away or creating a
    // new one — at that exact moment, agent.messages is guaranteed to still
    // reflect THIS conversation, not an ambiguous "has the new thread loaded yet" state.
    const generateTitleIfNeeded = async () => {
        const current = conversations.find((c) => c.thread_id === activeThreadId);
        if (!current || current.title !== "New conversation") return;

        const firstUserMessage = agent.messages.find((m: any) => m.role === "user");
        if (!firstUserMessage) return;

        try {
        const res = await fetch(`http://localhost:8000/conversations/${current.id}/generate-title`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: firstUserMessage.content ?? "" }),
        });
        const updated = await res.json();
        setConversations((prev) => prev.map((c) => (c.id === current.id ? { ...c, title: updated.title } : c)));
        } catch {
        // Non-critical: if titling fails, the conversation just keeps its default name.
        }
    };

    const handleNewConversation = async () => {
        await generateTitleIfNeeded();
        const created = await fetch("http://localhost:8000/conversations", { method: "POST" }).then((r) => r.json());
        setConversations((prev) => [created, ...prev]);
        setActiveThreadId(created.thread_id);
    };

    const handleSwitchConversation = async (threadId: string) => {
        if (threadId === activeThreadId) return;
        await generateTitleIfNeeded();
        setActiveThreadId(threadId);
    };

    const handleRename = async (id: number) => {
        await fetch(`http://localhost:8000/conversations/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: renameValue }),
        });
        setConversations((prev) => prev.map((c) => (c.id === id ? { ...c, title: renameValue } : c)));
        setRenamingId(null);
    };

    const handleDeleteConversation = async (id: number, threadId: string) => {
        await fetch(`http://localhost:8000/conversations/${id}`, { method: "DELETE" });
        const remaining = conversations.filter((c) => c.id !== id);
        setConversations(remaining);

        if (activeThreadId === threadId) {
        if (remaining.length > 0) {
            setActiveThreadId(remaining[0].thread_id);
        } else {
            handleNewConversation();
        }
        }
    };

    useRenderTool({
        name: "get_company_profile",
        parameters: z.object({ company_name: z.string() }),
        render: ({ status, parameters, result }) => {
        if (status !== "complete" || !result) return <p className="text-sm text-muted-foreground my-2">Looking up {parameters?.company_name ?? "company"}...</p>;
        return <CompanyProfileCard profile={JSON.parse(result)} />;
        },
    });

    useRenderTool({
        name: "generate_formal_report",
        parameters: z.object({ company_name: z.string() }),
        render: ({ status, parameters, result }) => {
        if (status !== "complete" || !result) {
            return <p className="text-sm text-muted-foreground my-2">Generating report for {parameters?.company_name ?? "company"}...</p>;
        }
        try {
            const report = JSON.parse(result);
            if (report.error) return null;
            return <FormalReportCard report={report} />;
        } catch {
            return null;
        }
        },
    });

    useRenderTool({
        name: "prepare_meeting_briefing",
        parameters: z.object({ company_name: z.string() }),
        render: ({ status, parameters, result }) => {
        if (status !== "complete" || !result) return <p className="text-sm text-muted-foreground my-2">Preparing briefing for {parameters?.company_name ?? "company"}...</p>;
        try {
            return <MeetingBriefingCard briefing={JSON.parse(result)} />;
        } catch {
            return <p className="text-sm my-2" style={{ color: "var(--risk-high)" }}>Something went wrong preparing this briefing.</p>;
        }
        },
    });

    useRenderTool({
        name: "get_portfolio_risk_summary",
        parameters: z.object({}),
        render: ({ status, result }) => {
        if (status !== "complete" || !result) return <p className="text-sm text-muted-foreground my-2">Analyzing your portfolio...</p>;
        try {
            return <PortfolioSummaryCard summary={JSON.parse(result)} />;
        } catch {
            return <p className="text-sm my-2" style={{ color: "var(--risk-high)" }}>Something went wrong analyzing the portfolio.</p>;
        }
        },
    });

    useRenderTool({
        name: "compare_to_peers",
        parameters: z.object({ company_name: z.string() }),
        render: ({ status, parameters, result }) => {
        if (status !== "complete" || !result) return <p className="text-sm text-muted-foreground my-2">Comparing {parameters?.company_name ?? "company"} to its peers...</p>;
        try {
            return <PeerComparisonCard comparison={JSON.parse(result)} />;
        } catch {
            return <p className="text-sm my-2" style={{ color: "var(--risk-high)" }}>Something went wrong comparing peers.</p>;
        }
        },
    });

    const handleCompanyClick = async (companyName: string) => {
        setLastReviewed(companyName);
        agent.addMessage({ id: crypto.randomUUID(), role: "user", content: `What's the risk profile for ${companyName}?` });
        await agent.runAgent();
    };

    return (
        <div
        className="flex h-screen w-full"
        style={{
            backgroundColor: "var(--paper)",
            backgroundImage: "linear-gradient(to right, var(--grid-line) 1px, transparent 1px), linear-gradient(to bottom, var(--grid-line) 1px, transparent 1px)",
            backgroundSize: "28px 28px",
        }}
        >
        <header
            className="fixed top-0 left-0 right-0 h-14 grid grid-cols-3 items-center px-6 z-10"
            style={{ background: "var(--structural)", color: "white", borderBottom: "1px solid var(--hairline)" }}
        >
            <div className="flex items-center justify-start">
            <button
                onClick={() => setIsConversationsOpen((v) => !v)}
                className="inline-flex items-center gap-1.5 text-sm font-medium px-3 py-1.5 rounded-md transition-colors"
                style={{ background: isConversationsOpen ? "var(--accent)" : "rgba(255,255,255,0.12)" }}
            >
                Chats
            </button>
            </div>

            <div className="flex items-center justify-center gap-2.5">
            <span className="w-2 h-2 rounded-full shrink-0" style={{ background: "var(--risk-low)", animation: "pulse-dot 2.2s ease-in-out infinite" }} />
            <span className="font-display text-lg tracking-tight">Risk &amp; Growth Advisory</span>
            </div>

            <div className="flex items-center justify-end">
            <button
                onClick={() => setIsWatchlistOpen((v) => !v)}
                className="inline-flex items-center gap-1.5 text-sm font-medium px-3 py-1.5 rounded-md transition-colors"
                style={{ background: isWatchlistOpen ? "var(--accent)" : "rgba(255,255,255,0.12)" }}
            >
                Watchlist
            </button>
            </div>
        </header>

        <aside
            className="shrink-0 pt-14 border-r flex flex-col overflow-hidden transition-all duration-200 ease-in-out"
            style={{ borderColor: "var(--hairline)", width: isConversationsOpen ? "16rem" : "0rem" }}
        >
            <div className="w-64 h-full flex flex-col">
            <div className="p-3">
                <button onClick={handleNewConversation} className="w-full text-sm py-2 rounded-md border transition-colors hover:bg-black/3" style={{ borderColor: "var(--hairline)" }}>
                + New chat
                </button>
            </div>
            <div className="overflow-y-auto flex-1">
                {conversations.map((c) => (
                <div
                    key={c.thread_id}
                    onDoubleClick={() => { setRenamingId(c.id); setRenameValue(c.title); }}
                    className="border-b group"
                    style={{ borderColor: "var(--hairline)", background: c.thread_id === activeThreadId ? "rgba(180,83,9,0.06)" : "transparent" }}
                >
                    {renamingId === c.id ? (
                    <input
                        autoFocus
                        value={renameValue}
                        onChange={(e) => setRenameValue(e.target.value)}
                        onBlur={() => handleRename(c.id)}
                        onKeyDown={(e) => e.key === "Enter" && handleRename(c.id)}
                        className="w-full px-4 py-2.5 text-sm bg-transparent outline-none"
                    />
                    ) : (
                    <div className="w-full flex items-center">
                        <button
                        onClick={() => handleSwitchConversation(c.thread_id)}
                        className="flex-1 text-left px-4 py-2.5 text-sm truncate"
                        style={{ fontWeight: c.thread_id === activeThreadId ? 500 : 400 }}
                        >
                        {c.title}
                        </button>
                        <button
                        onClick={() => handleDeleteConversation(c.id, c.thread_id)}
                        className="px-2 opacity-0 group-hover:opacity-100 transition-opacity text-muted-foreground hover:text-current"
                        aria-label="Delete conversation"
                        >
                        <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
                            <path d="M2 3.5H12M5 3.5V2.5C5 2 5.5 1.5 6 1.5H8C8.5 1.5 9 2 9 2.5V3.5M5.5 6V10M8.5 6V10M3 3.5L3.5 11.5C3.5 12 4 12.5 4.5 12.5H9.5C10 12.5 10.5 12 10.5 11.5L11 3.5" stroke="currentColor" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round"/>
                        </svg>
                        </button>
                    </div>
                    )}
                </div>
                ))}
            </div>
            </div>
        </aside>

        <main className="flex-1 pt-14 flex justify-center px-6">
            <div
            className="w-full max-w-3xl h-[calc(100vh-3.5rem-2rem)] my-4 overflow-hidden"
            style={{ background: "var(--surface)", borderRadius: "var(--radius-md)", border: "1px solid var(--hairline)", boxShadow: "0 1px 2px rgba(18,23,43,0.04), 0 12px 32px -8px rgba(18,23,43,0.12)" }}
            >
            {activeThreadId && (
                <CopilotChat
                className="h-full"
                agentId="default"
                threadId={activeThreadId}
                labels={{ welcomeMessageText: "What would you like to review today?" }}
                />
            )}
            </div>
        </main>

        <aside
            className="shrink-0 pt-14 overflow-hidden border-l transition-all duration-200 ease-in-out"
            style={{ borderColor: "var(--hairline)", width: isWatchlistOpen ? "18rem" : "0rem" }}
        >
            <div className="w-72 h-full overflow-y-auto">
            <div className="mx-4 mt-3 mb-1 px-3 py-2 text-xs leading-relaxed" style={{ background: "rgba(180,83,9,0.07)", borderRadius: "var(--radius-sm)" }}>
                Click a company to pull its live risk profile into the conversation.
            </div>
            <div className="px-4 py-2 text-xs text-muted-foreground font-medium">Watchlist</div>
            {initialWatchlist.map((c) => {
                const isActive = c.name === lastReviewed;
                return (
                <button
                    key={c.name}
                    onClick={() => handleCompanyClick(c.name)}
                    className="w-full flex items-center justify-between px-4 py-2.5 border-b text-left transition-colors"
                    style={{ borderColor: "var(--hairline)", background: isActive ? "rgba(180,83,9,0.06)" : "transparent" }}
                >
                    <div className="flex items-center gap-2 min-w-0">
                    <span className="shrink-0 rounded-sm" style={{ width: isActive ? "3px" : "4px", height: "16px", background: riskColor(c.risk_score) }} />
                    <span className="text-sm truncate" style={{ fontWeight: isActive ? 500 : 400 }}>{c.name}</span>
                    </div>
                    <span className="font-mono text-sm shrink-0 ml-2">{c.risk_score}</span>
                </button>
                );
            })}
            </div>
        </aside>
        </div>
    );
}