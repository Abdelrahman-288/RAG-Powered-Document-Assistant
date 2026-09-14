"use client";

type SidebarChat = {
  id: string;
  title: string;
  category: string;
  updatedAt: number;
};

type ActiveView =
  | "chat"
  | "knowledge"
  | "sources";

type SidebarProps = {
  onNewChat: () => void;

  chats: SidebarChat[];

  activeChatId: string | null;

  onOpenChat: (
    chatId: string
  ) => void;

  onDeleteChat: (
    chatId: string
  ) => void;

  activeView: ActiveView;

  onChangeView: (
    view: ActiveView
  ) => void;
};


function formatTime(
  timestamp: number
): string {
  const date =
    new Date(timestamp);

  const now =
    new Date();

  const isToday =
    date.toDateString() ===
    now.toDateString();

  if (isToday) {
    return date.toLocaleTimeString(
      [],
      {
        hour: "2-digit",
        minute: "2-digit",
      }
    );
  }

  return date.toLocaleDateString(
    [],
    {
      month: "short",
      day: "numeric",
    }
  );
}


function formatCategory(
  category: string
): string {
  const labels:
    Record<string, string> = {
      auto: "Auto",

      ai_ml:
        "AI / Machine Learning",

      algorithms_data_structures:
        "Algorithms & Data Structures",

      cybersecurity:
        "Cybersecurity",

      data_science:
        "Data Science",

      malware_analysis:
        "Malware Analysis",

      python:
        "Python",
    };

  if (labels[category]) {
    return labels[category];
  }

  return category
    .split("_")
    .map(
      (word) =>
        word.charAt(0).toUpperCase() +
        word.slice(1)
    )
    .join(" ");
}


export default function Sidebar({
  onNewChat,
  chats,
  activeChatId,
  onOpenChat,
  onDeleteChat,
  activeView,
  onChangeView,
}: SidebarProps) {
  return (
    <aside className="flex h-screen w-64 flex-col border-r border-zinc-800 bg-[#111111]">

      {/* Logo */}
      <div className="flex items-center gap-3 px-5 py-5">

        <div className="flex h-9 w-9 items-center justify-center rounded-xl bg-red-600 font-bold text-white shadow-lg shadow-red-950/30">
          T
        </div>

        <div>

          <h1 className="font-semibold text-white">
            TechRAG
          </h1>

          <p className="text-xs text-zinc-500">
            Architect
          </p>

        </div>

      </div>


      {/* New Chat */}
      <div className="px-3">

        <button
          type="button"
          onClick={onNewChat}
          className="flex w-full items-center gap-3 rounded-xl bg-red-600 px-4 py-3 text-sm font-medium text-white transition hover:bg-red-500"
        >

          <span className="text-lg">
            +
          </span>

          <span>
            New Chat
          </span>

        </button>

      </div>


      {/* Workspace */}
      <div className="mt-6 px-3">

        <p className="mb-2 px-3 text-xs font-medium uppercase tracking-wider text-zinc-600">
          Workspace
        </p>


        {/* Current Chat */}
        <button
          type="button"
          onClick={() =>
            onChangeView("chat")
          }
          className={
            activeView === "chat"
              ? "flex w-full items-center gap-3 rounded-xl border border-red-900/30 bg-red-500/10 px-3 py-2.5 text-left text-sm text-red-300"
              : "flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm text-zinc-500 transition hover:bg-zinc-900 hover:text-zinc-200"
          }
        >

          <span>
            💬
          </span>

          <span>
            Current Chat
          </span>

        </button>


        {/* Knowledge Base */}
        <button
          type="button"
          onClick={() =>
            onChangeView(
              "knowledge"
            )
          }
          className={
            activeView ===
            "knowledge"
              ? "mt-1 flex w-full items-center gap-3 rounded-xl border border-red-900/30 bg-red-500/10 px-3 py-2.5 text-left text-sm text-red-300"
              : "mt-1 flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm text-zinc-500 transition hover:bg-zinc-900 hover:text-zinc-200"
          }
        >

          <span>
            📚
          </span>

          <span>
            Knowledge Base
          </span>

        </button>


        {/* Sources */}
        <button
          type="button"
          onClick={() =>
            onChangeView(
              "sources"
            )
          }
          className={
            activeView ===
            "sources"
              ? "mt-1 flex w-full items-center gap-3 rounded-xl border border-red-900/30 bg-red-500/10 px-3 py-2.5 text-left text-sm text-red-300"
              : "mt-1 flex w-full items-center gap-3 rounded-xl px-3 py-2.5 text-left text-sm text-zinc-500 transition hover:bg-zinc-900 hover:text-zinc-200"
          }
        >

          <span>
            📄
          </span>

          <span>
            Sources
          </span>

        </button>

      </div>


      {/* Recent Chats */}
      <div className="mt-8 min-h-0 flex-1 overflow-y-auto px-3">

        <div className="mb-2 flex items-center justify-between px-3">

          <p className="text-xs font-medium uppercase tracking-wider text-zinc-600">
            Recent Chats
          </p>


          {chats.length > 0 && (

            <span className="text-xs text-zinc-700">
              {chats.length}
            </span>

          )}

        </div>


        {chats.length === 0 && (

          <div className="rounded-xl px-3 py-2.5 text-sm text-zinc-600">
            No saved chats yet
          </div>

        )}


        <div className="space-y-1">

          {chats.map(
            (chat) => {

              const isActive =
                chat.id ===
                  activeChatId &&
                activeView ===
                  "chat";


              return (

                <div
                  key={chat.id}
                  className={
                    isActive
                      ? "group relative rounded-xl border border-red-900/40 bg-red-500/10"
                      : "group relative rounded-xl border border-transparent transition hover:bg-zinc-900"
                  }
                >

                  <button
                    type="button"
                    onClick={() => {

                      onOpenChat(
                        chat.id
                      );

                      onChangeView(
                        "chat"
                      );

                    }}
                    className="w-full px-3 py-3 pr-10 text-left"
                  >

                    <p
                      className={
                        isActive
                          ? "truncate text-sm font-medium text-red-300"
                          : "truncate text-sm text-zinc-400 group-hover:text-zinc-200"
                      }
                    >
                      {chat.title}
                    </p>


                    <div className="mt-1 flex items-center justify-between gap-2">

                      <span className="truncate text-[11px] text-zinc-600">

                        {
                          formatCategory(
                            chat.category
                          )
                        }

                      </span>


                      <span className="shrink-0 text-[11px] text-zinc-700">

                        {
                          formatTime(
                            chat.updatedAt
                          )
                        }

                      </span>

                    </div>

                  </button>


                  {/* Delete Chat */}
                  <button
                    type="button"
                    title="Delete chat"
                    onClick={(
                      event
                    ) => {

                      event.stopPropagation();

                      const confirmed =
                        window.confirm(
                          `Delete "${chat.title}"?`
                        );


                      if (confirmed) {

                        onDeleteChat(
                          chat.id
                        );

                      }

                    }}
                    className="absolute right-2 top-3 hidden h-7 w-7 items-center justify-center rounded-lg text-sm text-zinc-600 transition hover:bg-red-500/10 hover:text-red-400 group-hover:flex"
                  >
                    ×
                  </button>

                </div>

              );
            }
          )}

        </div>

      </div>


      {/* Bottom */}
      <div className="border-t border-zinc-800 p-4">

        <div className="flex items-center gap-3">

          <div className="flex h-8 w-8 items-center justify-center rounded-full bg-red-600/20 text-sm font-medium text-red-400">
            T
          </div>


          <div className="min-w-0">

            <p className="truncate text-sm text-zinc-300">
              TechRAG
            </p>

            <p className="truncate text-xs text-zinc-600">
              Local RAG System
            </p>

          </div>

        </div>

      </div>

    </aside>
  );
}