"use client";

import { useState } from "react";
import {
  askQuestion,
  QueryResponse,
} from "@/lib/api";


type ChatMessage = {
  role: "user" | "assistant";
  content: string;
  result?: QueryResponse;
};


const categoryLabels: Record<string, string> = {
  auto: "Auto",
  ai_ml: "AI / Machine Learning",
  algorithms_data_structures: "Algorithms & Data Structures",
  cybersecurity: "Cybersecurity",
  data_science: "Data Science",
  malware_analysis: "Malware Analysis",
  python: "Python",
};


export default function ChatInterface() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [category, setCategory] = useState<string>("auto");


  async function handleSubmit(
    event: React.FormEvent<HTMLFormElement>
  ) {
    event.preventDefault();

    const question = input.trim();

    if (!question || loading) {
      return;
    }

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: question,
      },
    ]);

    setInput("");
    setLoading(true);

    try {
      const result = await askQuestion(
        question,
        category === "auto"
          ? null
          : category
      );

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: result.answer,
          result,
        },
      ]);
    } catch (error) {
      const message =
        error instanceof Error
          ? error.message
          : "Unknown error";

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            `Sorry, the backend request failed: ${message}`,
        },
      ]);
    } finally {
      setLoading(false);
    }
  }


  return (
    <div className="flex min-h-screen flex-col bg-zinc-950 text-white">

      <header className="border-b border-zinc-800 px-6 py-4">
        <div className="mx-auto max-w-5xl">

          <h1 className="text-xl font-semibold">
            TechRAG Architect
          </h1>

          <p className="mt-1 text-sm text-zinc-400">
            Grounded technical answers from your document knowledge base
          </p>

        </div>
      </header>


      <main className="mx-auto flex w-full max-w-5xl flex-1 flex-col px-6 py-6">

        {/* Study field selector */}
        <div className="mb-6">

          <label className="mb-2 block text-sm font-medium text-zinc-400">
            Study field
          </label>

          <select
            value={category}
            onChange={(event) =>
              setCategory(event.target.value)
            }
            disabled={loading}
            className="w-full max-w-sm rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-3 text-white outline-none transition focus:border-zinc-500 disabled:cursor-not-allowed disabled:opacity-50"
          >
            <option value="auto">
              Auto
            </option>

            <option value="ai_ml">
              AI / Machine Learning
            </option>

            <option value="algorithms_data_structures">
              Algorithms & Data Structures
            </option>

            <option value="cybersecurity">
              Cybersecurity
            </option>

            <option value="data_science">
              Data Science
            </option>

            <option value="malware_analysis">
              Malware Analysis
            </option>

            <option value="python">
              Python
            </option>

          </select>

          <p className="mt-2 text-xs text-zinc-500">
            Select a field to keep retrieval focused, or use Auto to search all indexed documents.
          </p>

        </div>


        {/* Chat area */}
        <div className="flex-1 space-y-6">

          {messages.length === 0 && (
            <div className="flex min-h-[50vh] items-center justify-center">

              <div className="max-w-xl text-center">

                <h2 className="text-3xl font-semibold">
                  What can I help you understand?
                </h2>

                <p className="mt-3 text-zinc-400">
                  Ask questions about AI, algorithms,
                  cybersecurity, data science,
                  malware analysis, Python,
                  and your indexed technical documents.
                </p>

                <p className="mt-4 text-sm text-zinc-500">
                  Current field:{" "}
                  <span className="font-medium text-zinc-300">
                    {categoryLabels[category]}
                  </span>
                </p>

              </div>

            </div>
          )}


          {messages.map(
            (message, index) => (
              <div
                key={index}
                className={
                  message.role === "user"
                    ? "flex justify-end"
                    : "flex justify-start"
                }
              >

                <div
                  className={
                    message.role === "user"
                      ? "max-w-2xl rounded-2xl bg-blue-600 px-5 py-3"
                      : "max-w-3xl rounded-2xl border border-zinc-800 bg-zinc-900 px-5 py-4"
                  }
                >

                  <p className="whitespace-pre-wrap leading-7">
                    {message.content}
                  </p>


                  {message.result && (
                    <div className="mt-4">

                      <div className="flex flex-wrap gap-2 text-xs">

                        <span
                          className={
                            message.result
                              .grounding_success
                              ? "rounded-full bg-green-500/10 px-3 py-1 text-green-400"
                              : "rounded-full bg-red-500/10 px-3 py-1 text-red-400"
                          }
                        >
                          {message.result
                            .grounding_success
                            ? "Grounded"
                            : "Not fully grounded"}
                        </span>


                        <span className="rounded-full bg-zinc-800 px-3 py-1 text-zinc-300">
                          {
                            message.result
                              .citation_count
                          }{" "}
                          citations
                        </span>


                        <span className="rounded-full bg-zinc-800 px-3 py-1 text-zinc-300">
                          Field:{" "}
                          {categoryLabels[category]}
                        </span>

                      </div>


                      {message.result.sources.length > 0 && (
                        <details className="mt-4">

                          <summary className="cursor-pointer text-sm font-medium text-zinc-300">
                            View retrieved sources
                          </summary>


                          <div className="mt-3 space-y-3">

                            {message.result.sources.map(
                              (source) => (
                                <div
                                  key={`${source.rank}-${source.document}-${source.page}`}
                                  className="rounded-xl border border-zinc-800 bg-zinc-950 p-4"
                                >

                                  <div className="text-sm font-medium">
                                    {source.document}
                                  </div>


                                  <div className="mt-2 text-xs text-zinc-400">

                                    Page {source.page}

                                    {" • "}

                                    {
                                      categoryLabels[
                                        source.category
                                      ] ??
                                      source.category
                                    }

                                    {" • "}

                                    Similarity{" "}

                                    {source.similarity.toFixed(
                                      4
                                    )}

                                  </div>

                                </div>
                              )
                            )}

                          </div>

                        </details>
                      )}

                    </div>
                  )}

                </div>

              </div>
            )
          )}


          {loading && (
            <div className="flex justify-start">

              <div className="rounded-2xl border border-zinc-800 bg-zinc-900 px-5 py-4 text-zinc-400">
                Searching documents and generating answer...
              </div>

            </div>
          )}

        </div>


        {/* Input */}
        <div className="sticky bottom-0 mt-8 bg-zinc-950 pb-6 pt-4">

          <form
            onSubmit={handleSubmit}
            className="flex items-center gap-3 rounded-2xl border border-zinc-700 bg-zinc-900 p-3"
          >

            <input
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              placeholder={
                category === "auto"
                  ? "Ask a technical question..."
                  : `Ask about ${categoryLabels[category]}...`
              }
              disabled={loading}
              className="flex-1 bg-transparent px-3 py-2 text-white outline-none placeholder:text-zinc-500"
            />


            <button
              type="submit"
              disabled={
                loading ||
                !input.trim()
              }
              className="rounded-xl bg-white px-5 py-2 font-medium text-black transition hover:bg-zinc-200 disabled:cursor-not-allowed disabled:opacity-40"
            >
              {loading
                ? "Thinking..."
                : "Send"}
            </button>

          </form>

        </div>

      </main>

    </div>
  );
}