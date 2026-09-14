"use client";

import { useEffect, useMemo, useState } from "react";

import {
  getKnowledgeBase,
  KnowledgeBaseResponse,
} from "@/lib/api";


function formatCategoryLabel(
  category: string
): string {
  return category
    .split("_")
    .map(
      (word) =>
        word.charAt(0).toUpperCase() +
        word.slice(1)
    )
    .join(" ");
}


export default function Sources() {
  const [data, setData] =
    useState<KnowledgeBaseResponse | null>(
      null
    );

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState<string | null>(null);

  const [search, setSearch] =
    useState("");

  const [categoryFilter, setCategoryFilter] =
    useState("all");


  useEffect(() => {
    async function loadSources() {
      try {
        const result =
          await getKnowledgeBase();

        setData(result);
      } catch (error) {
        setError(
          error instanceof Error
            ? error.message
            : "Failed to load sources."
        );
      } finally {
        setLoading(false);
      }
    }

    loadSources();
  }, []);


  const documents = useMemo(() => {
    if (!data) {
      return [];
    }

    return data.categories.flatMap(
      (category) =>
        category.documents.map(
          (document) => ({
            ...document,
            category:
              category.category,
          })
        )
    );
  }, [data]);


  const filteredDocuments =
    useMemo(() => {
      return documents.filter(
        (document) => {
          const matchesSearch =
            document.document
              .toLowerCase()
              .includes(
                search.toLowerCase()
              );

          const matchesCategory =
            categoryFilter === "all" ||
            document.category ===
              categoryFilter;

          return (
            matchesSearch &&
            matchesCategory
          );
        }
      );
    }, [
      documents,
      search,
      categoryFilter,
    ]);


  if (loading) {
    return (
      <div className="flex h-full items-center justify-center text-zinc-500">
        Loading sources...
      </div>
    );
  }


  if (error || !data) {
    return (
      <div className="flex h-full items-center justify-center">

        <div className="rounded-xl border border-red-900/40 bg-red-500/10 px-5 py-4 text-red-400">
          {error ?? "Sources unavailable."}
        </div>

      </div>
    );
  }


  return (
    <div className="mx-auto w-full max-w-6xl px-6 py-8">

      <div className="mb-8">

        <h1 className="text-2xl font-semibold text-zinc-100">
          Sources
        </h1>

        <p className="mt-2 text-sm text-zinc-500">
          Browse all indexed technical documents.
        </p>

      </div>


      {/* Stats */}
      <div className="mb-6 grid gap-4 sm:grid-cols-3">

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
            Categories
          </p>

          <p className="mt-2 text-3xl font-semibold text-red-400">
            {data.total_categories}
          </p>
        </div>


        <div className="rounded-2xl border border-zinc-800 bg-[#151515] p-5">
          <p className="text-xs uppercase tracking-wider text-zinc-600">
            Chunks
          </p>

          <p className="mt-2 text-3xl font-semibold text-zinc-100">
            {data.total_chunks.toLocaleString()}
          </p>
        </div>

      </div>


      {/* Filters */}
      <div className="mb-6 flex flex-col gap-3 sm:flex-row">

        <input
          value={search}
          onChange={(event) =>
            setSearch(
              event.target.value
            )
          }
          placeholder="Search documents..."
          className="flex-1 rounded-xl border border-zinc-800 bg-[#151515] px-4 py-3 text-sm text-zinc-200 outline-none placeholder:text-zinc-600 focus:border-red-500"
        />


        <select
          value={categoryFilter}
          onChange={(event) =>
            setCategoryFilter(
              event.target.value
            )
          }
          className="rounded-xl border border-zinc-800 bg-[#151515] px-4 py-3 text-sm text-zinc-200 outline-none focus:border-red-500"
        >

          <option value="all">
            All Categories
          </option>

          {data.categories.map(
            (category) => (
              <option
                key={
                  category.category
                }
                value={
                  category.category
                }
              >
                {
                  formatCategoryLabel(
                    category.category
                  )
                }
              </option>
            )
          )}

        </select>

      </div>


      {/* Result count */}
      <p className="mb-4 text-xs text-zinc-600">
        {filteredDocuments.length} documents shown
      </p>


      {/* Documents */}
      <div className="space-y-3">

        {filteredDocuments.map(
          (document) => (

            <div
              key={`${document.category}-${document.document}`}
              className="rounded-2xl border border-zinc-800 bg-[#151515] p-5 transition hover:border-red-900/50"
            >

              <div className="flex items-start justify-between gap-4">

                <div className="min-w-0">

                  <p className="truncate text-sm font-medium text-zinc-200">
                    {document.document}
                  </p>


                  <div className="mt-2 flex flex-wrap gap-2 text-xs text-zinc-600">

                    <span className="text-red-400">
                      {
                        formatCategoryLabel(
                          document.category
                        )
                      }
                    </span>

                    <span>
                      •
                    </span>

                    <span>
                      {document.chunk_count.toLocaleString()} chunks
                    </span>

                  </div>

                </div>


                <span className="shrink-0 rounded-full border border-zinc-800 bg-zinc-950 px-3 py-1 text-xs text-zinc-500">
                  PDF
                </span>

              </div>

            </div>

          )
        )}

      </div>

    </div>
  );
}