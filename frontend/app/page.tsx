"use client";
import { CopilotChat, useRenderTool } from "@copilotkit/react-core/v2";
import { z } from "zod";
import { CompanyProfileCard } from "../components/company-profile-card";

export default function Home() {
  useRenderTool({
    name: "get_company_profile",
    parameters: z.object({
      company_name: z.string().describe("The name of the company to look up"),
    }),
    render: ({ status, parameters, result }) => {
      if (status !== "complete" || !result) {
        return (
          <p className="text-sm text-muted-foreground my-2">
            Looking up {parameters?.company_name ?? "company"}...
          </p>
        );
      }
      const profile = JSON.parse(result);
      return <CompanyProfileCard profile={profile} />;
    },
  });

  return (
    <div className="flex justify-center items-center h-screen w-full">
      <div className="h-full w-full max-w-2xl">
        <CopilotChat className="h-full rounded-2xl" />
      </div>
    </div>
  );
}