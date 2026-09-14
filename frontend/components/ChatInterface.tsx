"use client";

import {
  useEffect,
  useState,
} from "react";

import Sidebar from "@/components/Sidebar";
import KnowledgeBase from "@/components/KnowledgeBase";
import Sources from "@/components/Sources";

import {
  askQuestion,
  getStats,
  type QueryResponse,
} from "@/lib/api";


type ChatMessage = {
  role:
    | "user"
    | "assistant";

  content: string;

  result?: QueryResponse;

  category?: string;

  question?: string;
};


type SavedChat = {
  id: string;

  title: string;

  messages: ChatMessage[];

  category: string;

  updatedAt: number;
};


type ActiveView =
  | "chat"
  | "knowledge"
  | "sources";


const categoryLabels:
  Record<string, string> = {

  auto:
    "Auto",

  ai_ml:
    "AI / Machine Learning",

  algorithms_data_structures:
    "Algorithms & Data Structures",

  cloud_security:
    "Cloud Security",

  computer_vision:
    "Computer Vision",

  cybersecurity:
    "Cybersecurity",

  data_science:
    "Data Science",

  deep_learning:
    "Deep Learning",

  embedded_systems:
    "Embedded Systems",

  llm:
    "LLM",

  malware_analysis:
    "Malware Analysis",

  nlp:
    "NLP",

  python:
    "Python",
};


function formatCategoryLabel(
  category: string
): string {
  if (
    categoryLabels[
      category
    ]
  ) {
    return (
      categoryLabels[
        category
      ]
    );
  }


  return category
    .split("_")
    .map(
      (word) =>
        word
          .charAt(0)
          .toUpperCase() +
        word.slice(1)
    )
    .join(" ");
}


function createChatTitle(
  question: string
): string {
  const trimmed =
    question.trim();


  if (
    trimmed.length <= 45
  ) {
    return trimmed;
  }


  return `${trimmed.slice(
    0,
    45
  )}...`;
}


export default function ChatInterface() {
  const [
    messages,
    setMessages,
  ] =
    useState<ChatMessage[]>(
      []
    );


  const [
    input,
    setInput,
  ] =
    useState("");


  const [
    loading,
    setLoading,
  ] =
    useState(false);


  const [
    category,
    setCategory,
  ] =
    useState<string>(
      "auto"
    );


  const [
    availableCategories,
    setAvailableCategories,
  ] =
    useState<string[]>(
      []
    );


  const [
    statsLoading,
    setStatsLoading,
  ] =
    useState(true);


  const [
    savedChats,
    setSavedChats,
  ] =
    useState<SavedChat[]>(
      []
    );


  const [
    activeChatId,
    setActiveChatId,
  ] =
    useState<
      string | null
    >(
      null
    );


  const [
    activeView,
    setActiveView,
  ] =
    useState<ActiveView>(
      "chat"
    );


  // =========================================================
  // Load categories
  // =========================================================
  useEffect(() => {
    async function loadStats() {
      try {
        const stats =
          await getStats();


        setAvailableCategories(
          [
            ...stats.categories,
          ].sort(
            (a, b) =>
              formatCategoryLabel(
                a
              ).localeCompare(
                formatCategoryLabel(
                  b
                )
              )
          )
        );

      } catch (error) {
        console.error(
          "Failed to load backend stats:",
          error
        );

      } finally {
        setStatsLoading(
          false
        );
      }
    }


    loadStats();
  }, []);


  // =========================================================
  // Load saved chats
  // =========================================================
  useEffect(() => {
    try {
      const storedChats =
        localStorage.getItem(
          "techrag_chats"
        );


      if (
        !storedChats
      ) {
        return;
      }


      const parsed =
        JSON.parse(
          storedChats
        );


      if (
        Array.isArray(
          parsed
        )
      ) {
        setSavedChats(
          parsed
        );
      }

    } catch (error) {
      console.error(
        "Failed to load saved chats:",
        error
      );


      setSavedChats(
        []
      );
    }
  }, []);


  // =========================================================
  // Save chats
  // =========================================================
  function saveChats(
    chats: SavedChat[]
  ) {
    const sortedChats =
      [
        ...chats,
      ].sort(
        (a, b) =>
          b.updatedAt -
          a.updatedAt
      );


    setSavedChats(
      sortedChats
    );


    localStorage.setItem(
      "techrag_chats",
      JSON.stringify(
        sortedChats
      )
    );
  }


  // =========================================================
  // Save/update conversation
  // =========================================================
  function saveCurrentConversation(
    nextMessages:
      ChatMessage[],
    selectedCategory:
      string,
    questionForTitle?:
      string
  ) {
    if (
      nextMessages.length ===
      0
    ) {
      return;
    }


    const now =
      Date.now();


    if (
      activeChatId
    ) {
      const existingChat =
        savedChats.find(
          (chat) =>
            chat.id ===
            activeChatId
        );


      const updatedChat:
        SavedChat = {

        id:
          activeChatId,

        title:
          existingChat
            ?.title ??
          createChatTitle(
            questionForTitle ??
              "New conversation"
          ),

        messages:
          nextMessages,

        category:
          selectedCategory,

        updatedAt:
          now,
      };


      const nextChats = [
        updatedChat,

        ...savedChats.filter(
          (chat) =>
            chat.id !==
            activeChatId
        ),
      ];


      saveChats(
        nextChats
      );

      return;
    }


    const newId =
      crypto.randomUUID();


    const newChat:
      SavedChat = {

      id:
        newId,

      title:
        createChatTitle(
          questionForTitle ??
            "New conversation"
        ),

      messages:
        nextMessages,

      category:
        selectedCategory,

      updatedAt:
        now,
    };


    setActiveChatId(
      newId
    );


    saveChats([
      newChat,
      ...savedChats,
    ]);
  }


  // =========================================================
  // New chat
  // =========================================================
  function handleNewChat() {
    setMessages(
      []
    );

    setInput(
      ""
    );

    setCategory(
      "auto"
    );

    setActiveChatId(
      null
    );

    setActiveView(
      "chat"
    );
  }


  // =========================================================
  // Open chat
  // =========================================================
  function handleOpenChat(
    chatId: string
  ) {
    const chat =
      savedChats.find(
        (item) =>
          item.id ===
          chatId
      );


    if (
      !chat
    ) {
      return;
    }


    setActiveChatId(
      chat.id
    );

    setMessages(
      chat.messages
    );

    setCategory(
      chat.category
    );

    setInput(
      ""
    );

    setActiveView(
      "chat"
    );
  }


  // =========================================================
  // Delete chat
  // =========================================================
  function handleDeleteChat(
    chatId: string
  ) {
    const nextChats =
      savedChats.filter(
        (chat) =>
          chat.id !==
          chatId
      );


    saveChats(
      nextChats
    );


    if (
      activeChatId ===
      chatId
    ) {
      handleNewChat();
    }
  }


  // =========================================================
  // Change workspace
  // =========================================================
  function handleChangeView(
    view: ActiveView
  ) {
    setActiveView(
      view
    );
  }


  // =========================================================
  // Submit question
  // =========================================================
  async function handleSubmit(
    event:
      React.FormEvent<
        HTMLFormElement
      >
  ) {
    event.preventDefault();


    const question =
      input.trim();


    if (
      !question ||
      loading
    ) {
      return;
    }


    const selectedCategory =
      category;


    const userMessage:
      ChatMessage = {

      role:
        "user",

      content:
        question,

      category:
        selectedCategory,

      question,
    };


    const messagesWithUser = [
      ...messages,
      userMessage,
    ];


    setMessages(
      messagesWithUser
    );

    setInput(
      ""
    );

    setLoading(
      true
    );


    try {
      const result =
        await askQuestion(
          question,

          selectedCategory ===
            "auto"
            ? null
            : selectedCategory
        );


      const assistantMessage:
        ChatMessage = {

        role:
          "assistant",

        content:
          result.answer,

        result,

        category:
          selectedCategory,

        question,
      };


      const nextMessages = [
        ...messagesWithUser,
        assistantMessage,
      ];


      setMessages(
        nextMessages
      );


      saveCurrentConversation(
        nextMessages,
        selectedCategory,
        question
      );

    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Unknown error";


      const assistantMessage:
        ChatMessage = {

        role:
          "assistant",

        content:
          `Sorry, the backend request failed: ${errorMessage}`,

        category:
          selectedCategory,

        question,
      };


      const nextMessages = [
        ...messagesWithUser,
        assistantMessage,
      ];


      setMessages(
        nextMessages
      );


      saveCurrentConversation(
        nextMessages,
        selectedCategory,
        question
      );

    } finally {
      setLoading(
        false
      );
    }
  }


  // =========================================================
  // User chooses ambiguous field
  // =========================================================
  async function handleCategorySuggestion(
    selectedCategory:
      string,
    question:
      string
  ) {
    if (
      loading
    ) {
      return;
    }


    setCategory(
      selectedCategory
    );


    setLoading(
      true
    );


    try {
      const result =
        await askQuestion(
          question,
          selectedCategory
        );


      const assistantMessage:
        ChatMessage = {

        role:
          "assistant",

        content:
          result.answer,

        result,

        category:
          selectedCategory,

        question,
      };


      const nextMessages = [
        ...messages,
        assistantMessage,
      ];


      setMessages(
        nextMessages
      );


      saveCurrentConversation(
        nextMessages,
        selectedCategory,
        question
      );

    } catch (error) {
      const errorMessage =
        error instanceof Error
          ? error.message
          : "Unknown error";


      const assistantMessage:
        ChatMessage = {

        role:
          "assistant",

        content:
          `Sorry, the backend request failed: ${errorMessage}`,

        category:
          selectedCategory,

        question,
      };


      const nextMessages = [
        ...messages,
        assistantMessage,
      ];


      setMessages(
        nextMessages
      );


      saveCurrentConversation(
        nextMessages,
        selectedCategory,
        question
      );

    } finally {
      setLoading(
        false
      );
    }
  }


  return (
    <div className="flex h-screen overflow-hidden bg-[#0d0d0d] text-white">


      {/* Sidebar */}
      <div className="hidden shrink-0 md:block">

        <Sidebar
          onNewChat={
            handleNewChat
          }

          chats={
            savedChats
          }

          activeChatId={
            activeChatId
          }

          onOpenChat={
            handleOpenChat
          }

          onDeleteChat={
            handleDeleteChat
          }

          activeView={
            activeView
          }

          onChangeView={
            handleChangeView
          }
        />

      </div>


      {/* Main */}
      <div className="flex min-w-0 flex-1 flex-col">


        {/* Knowledge Base */}
        {activeView ===
        "knowledge" ? (

          <main className="min-h-0 flex-1 overflow-y-auto">

            <KnowledgeBase />

          </main>


        ) : activeView ===
          "sources" ? (


          /* Sources */
          <main className="min-h-0 flex-1 overflow-y-auto">

            <Sources />

          </main>


        ) : (


          /* Chat */
          <>


            {/* Header */}
            <header className="shrink-0 border-b border-zinc-800 bg-[#0d0d0d]/95 px-6 py-4 backdrop-blur">

              <div className="mx-auto flex w-full max-w-5xl items-center justify-between">


                <div>

                  <h1 className="text-lg font-semibold tracking-tight text-zinc-100">
                    TechRAG Architect
                  </h1>


                  <p className="mt-1 text-xs text-zinc-500">
                    Grounded technical knowledge assistant
                  </p>

                </div>


                {/* Keep top selector state as Auto/manual */}
                <div className="hidden rounded-full border border-red-900/40 bg-red-500/5 px-3 py-1.5 text-xs text-zinc-400 sm:block">

                  Field:{" "}

                  <span className="font-medium text-red-400">

                    {
                      formatCategoryLabel(
                        category
                      )
                    }

                  </span>

                </div>

              </div>

            </header>


            {/* Chat body */}
            <main className="flex min-h-0 flex-1 flex-col overflow-y-auto">

              <div className="mx-auto flex w-full max-w-5xl flex-1 flex-col px-5 py-6 sm:px-6">


                {/* Study field */}
                <div className="mb-6">

                  <div className="flex flex-wrap items-end justify-between gap-3">


                    <div className="w-full max-w-sm">

                      <label className="mb-2 block text-xs font-medium uppercase tracking-wider text-zinc-500">
                        Study field
                      </label>


                      <select
                        value={
                          category
                        }

                        onChange={(
                          event
                        ) =>
                          setCategory(
                            event.target.value
                          )
                        }

                        disabled={
                          loading ||
                          statsLoading
                        }

                        className="w-full rounded-xl border border-zinc-800 bg-[#171717] px-4 py-3 text-sm text-zinc-200 outline-none transition focus:border-red-500 focus:ring-2 focus:ring-red-500/10 disabled:cursor-not-allowed disabled:opacity-50"
                      >

                        <option value="auto">
                          Auto
                        </option>


                        {availableCategories.map(
                          (
                            availableCategory
                          ) => (

                            <option
                              key={
                                availableCategory
                              }

                              value={
                                availableCategory
                              }
                            >

                              {
                                formatCategoryLabel(
                                  availableCategory
                                )
                              }

                            </option>

                          )
                        )}

                      </select>

                    </div>


                    <p className="pb-1 text-xs text-zinc-600">

                      {
                        statsLoading
                          ? "Loading fields..."
                          : `${availableCategories.length} study fields available`
                      }

                    </p>

                  </div>

                </div>


                {/* Empty state */}
                {messages.length ===
                  0 && (

                  <div className="flex flex-1 items-center justify-center py-16">

                    <div className="max-w-2xl text-center">


                      <div className="mx-auto mb-6 flex h-14 w-14 items-center justify-center rounded-2xl bg-red-600 text-xl font-bold text-white shadow-xl shadow-red-950/30">
                        T
                      </div>


                      <h2 className="text-3xl font-semibold tracking-tight text-zinc-100 sm:text-4xl">
                        What would you like to learn?
                      </h2>


                      <p className="mx-auto mt-4 max-w-lg text-sm leading-6 text-zinc-500">
                        Ask questions grounded in your indexed technical books and documents.
                      </p>


                      <div className="mt-6 inline-flex rounded-full border border-zinc-800 bg-[#151515] px-4 py-2 text-sm text-zinc-500">

                        Current field:&nbsp;

                        <span className="font-medium text-red-400">

                          {
                            formatCategoryLabel(
                              category
                            )
                          }

                        </span>

                      </div>

                    </div>

                  </div>

                )}


                {/* Messages */}
                <div className="space-y-6">

                  {messages.map(
                    (
                      message,
                      index
                    ) => (

                      <div
                        key={
                          index
                        }

                        className={
                          message.role ===
                          "user"
                            ? "flex justify-end"
                            : "flex justify-start"
                        }
                      >


                        <div
                          className={
                            message.role ===
                            "user"
                              ? "max-w-[85%] rounded-2xl rounded-br-md bg-red-600 px-5 py-3 text-white shadow-lg shadow-red-950/10 sm:max-w-2xl"
                              : "w-full max-w-3xl rounded-2xl border border-zinc-800 bg-[#161616] px-5 py-5"
                          }
                        >


                          <p className="whitespace-pre-wrap text-sm leading-7 text-zinc-100 sm:text-base">

                            {
                              message.content
                            }

                          </p>


                          {message.result && (

                            <div className="mt-5">


                              {/* Ambiguous category */}
                              {message
                                .result
                                .needs_category_selection &&
                                message.question && (

                                  <div className="mb-5 rounded-xl border border-zinc-800 bg-[#111111] p-4">


                                    <div className="mb-4">

                                      <p className="text-sm font-medium text-zinc-200">
                                        Choose the field you mean
                                      </p>


                                      <p className="mt-1 text-xs leading-5 text-zinc-500">
                                        Recommended fields are shown first. You can also choose any indexed field.
                                      </p>

                                    </div>


                                    <div className="flex flex-wrap gap-2">

                                      {[
                                        ...message
                                          .result
                                          .suggested_categories,

                                        ...availableCategories.filter(
                                          (
                                            availableCategory
                                          ) =>
                                            !message
                                              .result!
                                              .suggested_categories
                                              .includes(
                                                availableCategory
                                              )
                                        ),
                                      ].map(
                                        (
                                          fieldOption
                                        ) => {

                                          const isSelected =
                                            category ===
                                            fieldOption;


                                          const isSuggested =
                                            message
                                              .result!
                                              .suggested_categories
                                              .includes(
                                                fieldOption
                                              );


                                          return (

                                            <button
                                              key={
                                                fieldOption
                                              }

                                              type="button"

                                              disabled={
                                                loading
                                              }

                                              onClick={() =>
                                                handleCategorySuggestion(
                                                  fieldOption,
                                                  message.question!
                                                )
                                              }

                                              className={
                                                isSelected
                                                  ? "rounded-xl border border-red-500 bg-red-600 px-4 py-2 text-sm font-medium text-white shadow-md shadow-red-950/20 transition"
                                                  : "rounded-xl border border-zinc-700 bg-zinc-900 px-4 py-2 text-sm text-zinc-300 transition hover:border-red-500 hover:bg-red-500/10 hover:text-red-300 disabled:cursor-not-allowed disabled:opacity-50"
                                              }
                                            >

                                              {
                                                formatCategoryLabel(
                                                  fieldOption
                                                )
                                              }


                                              {isSuggested && (

                                                <span className="ml-2 text-xs opacity-60">
                                                  • suggested
                                                </span>

                                              )}

                                            </button>

                                          );
                                        }
                                      )}

                                    </div>

                                  </div>

                                )}


                              {/* Status */}
                              <div className="flex flex-wrap gap-2 text-xs">


                                {!message
                                  .result
                                  .needs_category_selection && (

                                    <span
                                      className={
                                        message
                                          .result
                                          .grounding_success

                                          ? "rounded-full border border-emerald-800/50 bg-emerald-500/10 px-3 py-1 text-emerald-400"

                                          : "rounded-full border border-red-900/50 bg-red-500/10 px-3 py-1 text-red-400"
                                      }
                                    >

                                      {
                                        message
                                          .result
                                          .grounding_success

                                          ? "Grounded"

                                          : "Not fully grounded"
                                      }

                                    </span>

                                  )}


                                {!message
                                  .result
                                  .needs_category_selection && (

                                    <span className="rounded-full border border-zinc-800 bg-zinc-950 px-3 py-1 text-zinc-400">

                                      {
                                        message
                                          .result
                                          .citation_count
                                      }{" "}
                                      citations

                                    </span>

                                  )}


                                {/* Actual category used */}
                                <span className="rounded-full border border-zinc-800 bg-zinc-950 px-3 py-1 text-zinc-400">

                                  Field:{" "}

                                  <span className="text-red-400">

                                    {
                                      formatCategoryLabel(
                                        message
                                          .result
                                          .resolved_category ??
                                        message
                                          .category ??
                                        "auto"
                                      )
                                    }

                                  </span>

                                </span>

                              </div>


                              {/* Sources */}
                              {message
                                .result
                                .sources
                                .length >
                                0 && (

                                  <details className="mt-4">


                                    <summary className="cursor-pointer select-none text-sm font-medium text-zinc-500 transition hover:text-red-400">
                                      View retrieved sources
                                    </summary>


                                    <div className="mt-3 space-y-3">


                                      {message
                                        .result
                                        .sources
                                        .map(
                                          (
                                            source
                                          ) => (

                                            <div
                                              key={`${source.rank}-${source.document}-${source.page}`}

                                              className="rounded-xl border border-zinc-800 bg-[#101010] p-4 transition hover:border-red-900/60"
                                            >


                                              <div className="text-sm font-medium leading-5 text-zinc-300">

                                                {
                                                  source.document
                                                }

                                              </div>


                                              <div className="mt-2 flex flex-wrap gap-2 text-xs text-zinc-600">


                                                <span>
                                                  Page{" "}
                                                  {
                                                    source.page
                                                  }
                                                </span>


                                                <span>
                                                  •
                                                </span>


                                                <span className="text-red-400">

                                                  {
                                                    formatCategoryLabel(
                                                      source.category
                                                    )
                                                  }

                                                </span>


                                                <span>
                                                  •
                                                </span>


                                                <span>
                                                  Similarity{" "}

                                                  {
                                                    source
                                                      .similarity
                                                      .toFixed(
                                                        4
                                                      )
                                                  }

                                                </span>


                                                {source
                                                  .reranker_score !==
                                                  null && (

                                                    <>

                                                      <span>
                                                        •
                                                      </span>


                                                      <span>
                                                        Reranker{" "}

                                                        {
                                                          source
                                                            .reranker_score
                                                            .toFixed(
                                                              4
                                                            )
                                                        }

                                                      </span>

                                                    </>

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


                  {/* Loading */}
                  {loading && (

                    <div className="flex justify-start">

                      <div className="flex items-center gap-3 rounded-2xl border border-zinc-800 bg-[#161616] px-5 py-4 text-sm text-zinc-500">


                        <div className="h-4 w-4 animate-spin rounded-full border-2 border-zinc-700 border-t-red-500" />


                        Searching documents and generating answer...

                      </div>

                    </div>

                  )}

                </div>


                <div className="min-h-8 flex-1" />


                {/* Composer */}
                <div className="sticky bottom-0 mt-8 bg-gradient-to-t from-[#0d0d0d] via-[#0d0d0d] to-transparent pb-5 pt-8">


                  <form
                    onSubmit={
                      handleSubmit
                    }

                    className="rounded-2xl border border-zinc-800 bg-[#171717] p-3 shadow-2xl shadow-black/30 transition focus-within:border-red-500/70 focus-within:ring-1 focus-within:ring-red-500/10"
                  >


                    <div className="flex items-end gap-3">


                      <input
                        value={
                          input
                        }

                        onChange={(
                          event
                        ) =>
                          setInput(
                            event.target.value
                          )
                        }

                        placeholder={
                          category ===
                          "auto"
                            ? "Ask anything about your technical documents..."
                            : `Ask about ${formatCategoryLabel(
                                category
                              )}...`
                        }

                        disabled={
                          loading
                        }

                        className="min-w-0 flex-1 bg-transparent px-2 py-2.5 text-sm text-zinc-100 outline-none placeholder:text-zinc-600 sm:text-base"
                      />


                      <button
                        type="submit"

                        disabled={
                          loading ||
                          !input.trim()
                        }

                        className="shrink-0 rounded-xl bg-red-600 px-5 py-2.5 text-sm font-medium text-white transition hover:bg-red-500 disabled:cursor-not-allowed disabled:bg-zinc-800 disabled:text-zinc-600"
                      >

                        {
                          loading
                            ? "Thinking..."
                            : "Send"
                        }

                      </button>

                    </div>


                    <div className="mt-2 flex items-center justify-between border-t border-zinc-800/70 px-2 pt-2">


                      <span className="text-xs text-zinc-600">
                        Grounded retrieval enabled
                      </span>


                      {/* This describes the selected mode */}
                      <span className="text-xs text-zinc-500">

                        Mode:{" "}

                        <span className="text-red-400">

                          {
                            formatCategoryLabel(
                              category
                            )
                          }

                        </span>

                      </span>

                    </div>

                  </form>

                </div>

              </div>

            </main>

          </>

        )}

      </div>

    </div>
  );
}