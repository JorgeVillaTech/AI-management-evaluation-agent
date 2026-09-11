"use client";
import { useState } from "react";
import { CopilotChat, useAgent, useRenderTool, useConfigureSuggestions } from "@copilotkit/react-core/v2";
import { z } from "zod";
import { CompanyProfileCard } from "./company-profile-card";
import { FormalReportCard } from "./formal-report-card";
import { MeetingBriefingCard } from "./meeting-briefing-card";
import { PortfolioSummaryCard } from "./portfolio-summary-card";

interface Company {
    name: string;
    sector: string;
    risk_score: number;
}

function riskColor(score: number) {
    if (score >= 60) return "var(--risk-high)";
    if (score >= 35) return "var(--accent)";
    return "var(--risk-low)";
}

export function ChatWorkspace({ initialWatchlist }: { initialWatchlist: Company[] }) {
    const [isWatchlistOpen, setIsWatchlistOpen] = useState(true);
    const [lastReviewed, setLastReviewed] = useState<string | null>(null);
    const { agent } = useAgent({ agentId: "default" });

    useRenderTool({
        name: "get_company_profile",
        parameters: z.object({ company_name: z.string() }),
        render: ({ status, parameters, result }) => {
        if (status !== "complete" || !result) {
            return <p className="text-sm text-muted-foreground my-2">Looking up {parameters?.company_name ?? "company"}...</p>;
        }
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
        return <FormalReportCard report={JSON.parse(result)} />;
        },
    });

    useRenderTool({
    name: "prepare_meeting_briefing",
    parameters: z.object({ company_name: z.string() }),
    render: ({ status, parameters, result }) => {
        if (status !== "complete" || !result) {
        return <p className="text-sm text-muted-foreground my-2">Preparing briefing for {parameters?.company_name ?? "company"}...</p>;
        }
        return <MeetingBriefingCard briefing={JSON.parse(result)} />;
    },
    });

    useRenderTool({
    name: "get_portfolio_risk_summary",
    parameters: z.object({}),
    render: ({ status, result }) => {
        if (status !== "complete" || !result) {
        return <p className="text-sm text-muted-foreground my-2">Analyzing your portfolio...</p>;
        }
        return <PortfolioSummaryCard summary={JSON.parse(result)} />;
    },
    });


    const topRisk = [...initialWatchlist].sort((a, b) => b.risk_score - a.risk_score).slice(0, 3);
    useConfigureSuggestions({
        suggestions: topRisk.map((c) => ({
        title: `Review ${c.name}`,
        message: `What's the risk profile for ${c.name}?`,
        })),
        available: "before-first-message",
    });

    const handleCompanyClick = async (companyName: string) => {
        setLastReviewed(companyName);
        agent.addMessage({
        id: crypto.randomUUID(),
        role: "user",
        content: `What's the risk profile for ${companyName}?`,
        });
        await agent.runAgent();
    };

    return (
        <div
        className="flex h-screen w-full"
        style={{
            backgroundColor: "var(--paper)",
            backgroundImage:
            "linear-gradient(to right, var(--grid-line) 1px, transparent 1px), linear-gradient(to bottom, var(--grid-line) 1px, transparent 1px)",
            backgroundSize: "28px 28px",
        }}
        >
        <header
            className="fixed top-0 left-0 right-0 h-14 flex items-center justify-between px-6 z-10"
            style={{ background: "var(--structural)", color: "white", borderBottom: "1px solid var(--hairline)" }}
        >
            <div className="flex items-center gap-2.5">
            <span
                className="w-2 h-2 rounded-full shrink-0"
                style={{ background: "var(--risk-low)", animation: "pulse-dot 2.2s ease-in-out infinite" }}
            />
            <span className="font-display text-lg tracking-tight">Risk &amp; Growth Advisory Agent</span>
            </div>
            <button
            onClick={() => setIsWatchlistOpen((v) => !v)}
            className="flex items-center gap-1.5 text-sm px-2.5 py-1 rounded hover:bg-white/10 transition-colors"
            aria-label={isWatchlistOpen ? "Hide watchlist" : "Show watchlist"}
            >
            <svg width="16" height="16" viewBox="0 0 16 16" fill="none">
                <rect x="1" y="2" width="14" height="12" rx="1.5" stroke="currentColor" strokeWidth="1.3" />
                <line x1="10.5" y1="2" x2="10.5" y2="14" stroke="currentColor" strokeWidth="1.3" />
            </svg>
            Companies
            </button>
        </header>

        <main className="flex-1 pt-14 flex justify-center px-6">
            <div
            className="w-full max-w-3xl h-[calc(100vh-3.5rem-2rem)] my-4 overflow-hidden"
            style={{
                background: "var(--surface)",
                borderRadius: "var(--radius-md)",
                border: "1px solid var(--hairline)",
                boxShadow: "0 1px 2px rgba(18,23,43,0.04), 0 12px 32px -8px rgba(18,23,43,0.12)",
            }}
            >
            <CopilotChat className="h-full" />
            </div>
        </main>

        <aside
            className="shrink-0 pt-14 overflow-hidden border-l transition-all duration-200 ease-in-out"
            style={{ borderColor: "var(--hairline)", width: isWatchlistOpen ? "18rem" : "0rem" }}
        >
            <div className="w-72 h-full overflow-y-auto">
            <div
                className="mx-4 mt-3 mb-1 px-3 py-2 text-xs leading-relaxed"
                style={{ background: "rgba(180,83,9,0.07)", borderRadius: "var(--radius-sm)", color: "var(--ink)" }}
            >
                Click a company to pull its live risk profile into the conversation.
            </div>
            <div className="px-4 py-2 text-xs text-muted-foreground font-medium">Companies</div>
            <div>
                {initialWatchlist.map((c) => {
                const isActive = c.name === lastReviewed;
                return (
                    <button
                    key={c.name}
                    onClick={() => handleCompanyClick(c.name)}
                    className="w-full flex items-center justify-between px-4 py-2.5 border-b text-left transition-colors"
                    style={{
                        borderColor: "var(--hairline)",
                        background: isActive ? "rgba(180,83,9,0.06)" : "transparent",
                    }}
                    >
                    <div className="flex items-center gap-2 min-w-0">
                        <span
                        className="shrink-0 rounded-sm"
                        style={{ width: isActive ? "3px" : "4px", height: "16px", background: riskColor(c.risk_score) }}
                        />
                        <span className="text-sm truncate" style={{ fontWeight: isActive ? 500 : 400 }}>{c.name}</span>
                    </div>
                    <span className="font-mono text-sm shrink-0 ml-2">{c.risk_score}</span>
                    </button>
                );
                })}
            </div>
            </div>
        </aside>
        </div>
    );
}