"use client";

import { useEffect, useState } from "react";

import {
  getKnowledgeBase,
  KnowledgeBaseResponse,
} from "@/lib/api";


function formatCategoryLabel(
  category: string
) {
  return category
    .split("_")
    .map(
      (word) =>
        word.charAt(0).toUpperCase() +
        word.slice(1)
    )
    .join(" ");
}


export default function KnowledgeBase() {
  const [data, setData] =
    useState<KnowledgeBaseResponse | null>(
      null
    );

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);


  useEffect(() => {
    async function loadKnowledgeBase() {
      try {
        const result =
          await getKnowledgeBase();

        setData(result);
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Failed to load knowledge base."
        );
      } finally {
        setLoading(false);
      }
    }

    loadKnowledgeBase();
  }, []);


  if (loading) {
    return (
      <div className="flex h-full items-center justify-center text-zinc-500">
        Loading knowledge base...
      </div>
    );
  }


  if (error || !data) {
    return (
      <div className="flex h-full items-center justify-center">
        <div className="rounded-xl border border-red-900/40 bg-red-500/10 px-5 py-4 text-red-400">
          {error ?? "Knowledge base unavailable."}
        </div>
      </div>
    );
  }


  return (
    <div className="mx-auto w-full max-w-6xl px-6 py-8">

      <div className="mb-8">

        <h1 className="text-2xl font-semibold text-zinc-100">
          Knowledge Base
        </h1>

        <p className="mt-2 text-sm text-zinc-500">
          Explore your indexed technical documents and categories.
        </p>

      </div>


      <div className="mb-8 grid gap-4 sm:grid-cols-3">

        <div className="rounded-2xl border border-zinc-800 bg-[#151515] p-5">

          <p className="text-xs uppercase tracking-wider text-zinc-600">
            Categories
          </p>

          <p className="mt-2 text-3xl font-semibold text-red-400">
            {data.total_categories}
          </p>

        </div>


        <div className="rounded-2xl border border-zinc-800 bg-[#151515] p-5">

          <p className="text-xs uppercase tracking-wider text-zinc-600">
            Documents
          </p>

          <p className="mt-2 text-3xl font-semibold text-zinc-100">
            {data.total_documents}
          </p>

        </div>


        <div className="rounded-2xl border border-zinc-800 bg-[#151515] p-5">

          <p className="text-xs uppercase tracking-wider text-zinc-600">
            Indexed Chunks
          </p>

          <p className="mt-2 text-3xl font-semibold text-zinc-100">
            {data.total_chunks.toLocaleString()}
          </p>

        </div>

      </div>


      <div className="space-y-5">

        {data.categories.map(
          (category) => (
            <details
              key={category.category}
              className="rounded-2xl border border-zinc-800 bg-[#151515]"
            >

              <summary className="cursor-pointer select-none px-5 py-4">

                <div className="flex items-center justify-between gap-4">

                  <div>

                    <h2 className="font-medium text-zinc-200">
                      {formatCategoryLabel(
                        category.category
                      )}
                    </h2>

                    <p className="mt-1 text-xs text-zinc-600">
                      {category.document_count} documents
                      {" • "}
                      {category.chunk_count.toLocaleString()} chunks
                    </p>

                  </div>


                  <div className="rounded-full border border-red-900/40 bg-red-500/10 px-3 py-1 text-xs text-red-400">
                    {category.document_count}
                  </div>

                </div>

              </summary>


              <div className="border-t border-zinc-800 px-5 py-4">

                <div className="space-y-2">

                  {category.documents.map(
                    (document) => (
                      <div
                        key={document.document}
                        className="flex items-center justify-between gap-4 rounded-xl border border-zinc-800 bg-[#101010] px-4 py-3"
                      >

                        <div className="min-w-0">

                          <p className="truncate text-sm text-zinc-300">
                            {document.document}
                          </p>

                          <p className="mt-1 text-xs text-zinc-600">
                            {document.chunk_count.toLocaleString()} chunks
                          </p>

                        </div>


                        <span className="shrink-0 rounded-full bg-zinc-900 px-3 py-1 text-xs text-zinc-500">
                          PDF
                        </span>

                      </div>
                    )
                  )}

                </div>

              </div>

            </details>
          )
        )}

      </div>

    </div>
  );
}