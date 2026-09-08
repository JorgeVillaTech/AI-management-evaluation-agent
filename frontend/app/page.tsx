"use client";
import { CopilotChat } from "@copilotkit/react-ui";

export default function Home() {
  return (
    <div className="flex justify-center items-center h-screen w-full">
      <div className="h-full w-full max-w-2xl">
        <CopilotChat className="h-full rounded-2xl" />
      </div>
    </div>
  );
}