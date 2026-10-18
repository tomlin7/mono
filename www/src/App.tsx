import { useState } from 'react'
import {
  Terminal as TerminalIcon,
  Download,
  Copy,
  Check,
  Zap,
  Palette,
  Layers,
  Keyboard,
  Cpu,
  MonitorCheck,
  ChevronDown,
  ChevronUp,
  Moon,
  Sun,
  ExternalLink
} from 'lucide-react'

function GithubIcon({ className }: { className?: string }) {
  return (
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" className={className} fill="currentColor">
      <path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5c.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34c-.46-1.16-1.11-1.47-1.11-1.47c-.91-.62.07-.6.07-.6c1 .07 1.53 1.03 1.53 1.03c.87 1.52 2.34 1.07 2.91.83c.09-.65.35-1.09.63-1.34c-2.22-.25-4.55-1.11-4.55-4.92c0-1.11.38-2 1.03-2.71c-.1-.25-.45-1.29.1-2.64c0 0 .84-.27 2.75 1.02c.79-.22 1.65-.33 2.5-.33s1.71.11 2.5.33c1.91-1.29 2.75-1.02 2.75-1.02c.55 1.35.2 2.39.1 2.64c.65.71 1.03 1.6 1.03 2.71c0 3.82-2.34 4.66-4.57 4.91c.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2"></path>
    </svg>
  )
}

export default function App() {
  const [copied, setCopied] = useState(false)
  const [activeTab, setActiveTab] = useState<'standalone' | 'tabbed'>('standalone')
  const [openFaq, setOpenFaq] = useState<number | null>(null)
  const [isDark, setIsDark] = useState(true)

  const copyInstall = () => {
    navigator.clipboard.writeText('pip install mono-term')
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const toggleTheme = () => {
    setIsDark(!isDark)
    if (!isDark) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  return (
    <div className={`min-h-screen ${isDark ? 'dark bg-[#121214] text-[#ececed]' : 'bg-[#fafafa] text-[#18181b]'} transition-colors`}>
      {/* Central Column Layout matching waku.sh */}
      <div className="mx-auto w-full max-w-[1100px] border-border/70 md:border-x border-zinc-200 dark:border-zinc-800/80 min-h-screen flex flex-col justify-between">
        <div>
          {/* Header */}
          <header className="flex h-16 items-center justify-between px-5 md:px-10 border-b border-zinc-200 dark:border-zinc-800/80">
            <a href="/" className="flex items-center gap-2.5">
              <div className="size-8 rounded-[6px] bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-500">
                <TerminalIcon className="size-4" />
              </div>
              <span className="text-[15px] font-semibold tracking-tight font-mono">Mono</span>
            </a>

            <div className="flex items-center gap-4">
              <button
                onClick={toggleTheme}
                aria-label="Toggle theme"
                className="p-2 rounded-full text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
              >
                {isDark ? <Sun className="size-4" /> : <Moon className="size-4" />}
              </button>

              <a
                href="https://github.com/tomlin7/mono"
                target="_blank"
                rel="noreferrer"
                aria-label="GitHub"
                className="rounded-full text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
              >
                <GithubIcon className="size-5" />
              </a>

              <a
                href="https://pypi.org/project/mono-term/"
                target="_blank"
                rel="noreferrer"
                className="inline-flex items-center justify-center font-medium transition-all select-none bg-zinc-900 text-zinc-50 dark:bg-zinc-100 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 h-8 gap-1.5 rounded-lg px-3 text-xs"
              >
                <Download className="size-3.5" />
                <span>PyPI</span>
              </a>
            </div>
          </header>

          <main>
            {/* Hero Section */}
            <section className="px-5 pt-14 pb-14 md:px-10 md:pt-20">
              <div className="mb-7 inline-flex items-center gap-2 rounded-full border border-zinc-200 dark:border-zinc-800 bg-zinc-100/50 dark:bg-zinc-900/50 px-3 py-1 text-xs text-zinc-600 dark:text-zinc-400">
                <span className="flex size-3.5 items-center justify-center rounded-[3px] bg-amber-500 text-[10px] font-bold text-zinc-950 font-mono">
                  M
                </span>
                Embeddable Python Terminal Emulator
              </div>

              <h1 className="max-w-4xl text-4xl font-semibold tracking-[-0.03em] md:text-[3.2rem] md:leading-[1.08]">
                Native, lightweight terminal emulator widget for Python.
              </h1>

              <p className="mt-5 max-w-[38rem] text-[17px] leading-relaxed text-zinc-600 dark:text-zinc-400">
                Mono gives your Tkinter desktop applications a high-performance pseudo-terminal with xterm 256 colors, Truecolor, ANSI SGR styles, dynamic PTY window resizing, and multi-tab management.
              </p>

              {/* Install pill & Quick action */}
              <div className="mt-8 flex flex-wrap items-center gap-x-4 gap-y-3">
                <div className="flex items-center rounded-lg border border-zinc-300 dark:border-zinc-800 bg-zinc-100/80 dark:bg-zinc-900/80 px-3.5 py-2 font-mono text-sm text-zinc-800 dark:text-zinc-200">
                  <span className="text-zinc-400 mr-2">$</span> pip install mono-term
                  <button
                    onClick={copyInstall}
                    aria-label="Copy install command"
                    className="ml-3 text-zinc-500 hover:text-zinc-900 dark:hover:text-zinc-100 transition-colors"
                  >
                    {copied ? <Check className="size-4 text-emerald-500" /> : <Copy className="size-4" />}
                  </button>
                </div>

                <a
                  href="https://github.com/tomlin7/mono"
                  target="_blank"
                  rel="noreferrer"
                  className="inline-flex items-center justify-center rounded-lg border border-transparent text-sm font-medium transition-all bg-zinc-900 text-zinc-100 dark:bg-zinc-100 dark:text-zinc-900 hover:bg-zinc-800 dark:hover:bg-zinc-200 h-10 px-4 gap-1.5"
                >
                  <GithubIcon className="size-4" />
                  View on GitHub
                </a>
              </div>

              {/* Supported Shells */}
              <div className="mt-14">
                <div className="font-mono text-[11px] tracking-[0.14em] text-zinc-500 dark:text-zinc-400 uppercase">
                  Native shell environments
                </div>
                <div className="mt-4 flex flex-wrap items-center gap-x-6 gap-y-3 font-mono text-xs text-zinc-700 dark:text-zinc-300">
                  <div className="px-3 py-1.5 rounded-md border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50">
                    PowerShell (PSReadLine safe)
                  </div>
                  <div className="px-3 py-1.5 rounded-md border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50">
                    Command Prompt (cmd.exe)
                  </div>
                  <div className="px-3 py-1.5 rounded-md border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50">
                    Bash / Zsh
                  </div>
                  <div className="px-3 py-1.5 rounded-md border border-zinc-200 dark:border-zinc-800 bg-zinc-50 dark:bg-zinc-900/50">
                    Python Interactive REPL
                  </div>
                </div>
              </div>
            </section>

            {/* Interactive Terminal Demo Widget */}
            <section className="border-t border-zinc-200 dark:border-zinc-800/80 p-5 md:p-10 bg-zinc-50/50 dark:bg-zinc-950/40">
              <div className="max-w-3xl mx-auto rounded-xl border border-zinc-300 dark:border-zinc-800 bg-[#1e1e1e] shadow-2xl overflow-hidden font-mono text-xs">
                {/* Window header */}
                <div className="flex items-center justify-between px-4 py-3 bg-[#181818] border-b border-zinc-800">
                  <div className="flex items-center gap-2">
                    <div className="size-3 rounded-full bg-red-500/80" />
                    <div className="size-3 rounded-full bg-yellow-500/80" />
                    <div className="size-3 rounded-full bg-green-500/80" />
                    <span className="ml-2 text-zinc-400 font-sans text-xs">mono — tk.Frame</span>
                  </div>
                  <div className="flex items-center gap-2 text-zinc-400">
                    <button
                      onClick={() => setActiveTab('standalone')}
                      className={`px-2 py-0.5 rounded text-[11px] ${activeTab === 'standalone' ? 'bg-zinc-800 text-zinc-100' : 'text-zinc-500'}`}
                    >
                      Default
                    </button>
                    <button
                      onClick={() => setActiveTab('tabbed')}
                      className={`px-2 py-0.5 rounded text-[11px] ${activeTab === 'tabbed' ? 'bg-zinc-800 text-zinc-100' : 'text-zinc-500'}`}
                    >
                      PowerShell
                    </button>
                  </div>
                </div>

                {/* Simulated PTY Screen */}
                <div className="p-4 space-y-2 leading-relaxed text-[#d4d4d4]">
                  {activeTab === 'standalone' ? (
                    <>
                      <div className="text-zinc-500">Microsoft Windows [Version 10.0.26200.9711]</div>
                      <div className="text-zinc-500">(c) Microsoft Corporation. All rights reserved.</div>
                      <div className="pt-2">
                        <span className="text-amber-500 font-semibold">C:\Users\Developer\project&gt;</span>{' '}
                        <span className="text-yellow-400">pytest -v</span>
                      </div>
                      <div className="text-zinc-300">
                        test_terminal.py::test_init <span className="text-emerald-400 font-semibold">PASSED</span> [ 50%]
                      </div>
                      <div className="text-zinc-300">
                        test_terminal.py::test_ansi_sgr <span className="text-emerald-400 font-semibold">PASSED</span> [100%]
                      </div>
                      <div className="text-emerald-400 font-semibold pt-1">
                        ================== 2 passed in 0.32s ==================
                      </div>
                      <div className="pt-2">
                        <span className="text-amber-500 font-semibold">C:\Users\Developer\project&gt;</span>{' '}
                        <span className="animate-pulse inline-block w-2 h-4 bg-zinc-200 translate-y-0.5" />
                      </div>
                    </>
                  ) : (
                    <>
                      <div className="text-blue-400">Windows PowerShell</div>
                      <div className="text-zinc-500">Copyright (C) Microsoft Corporation. All rights reserved.</div>
                      <div className="pt-2">
                        <span className="text-emerald-400 font-semibold">PS C:\Users\Developer&gt;</span>{' '}
                        <span className="text-yellow-400">git status</span>
                      </div>
                      <div className="text-zinc-300">On branch main</div>
                      <div className="text-zinc-400">Your branch is up to date with 'origin/main'.</div>
                      <div className="text-emerald-400">nothing to commit, working tree clean</div>
                      <div className="pt-2">
                        <span className="text-emerald-400 font-semibold">PS C:\Users\Developer&gt;</span>{' '}
                        <span className="animate-pulse inline-block w-2 h-4 bg-zinc-200 translate-y-0.5" />
                      </div>
                    </>
                  )}
                </div>
              </div>
            </section>

            {/* Feature Grid matching waku.sh */}
            <section className="border-t border-zinc-200 dark:border-zinc-800/80">
              <div className="px-5 pt-14 md:px-10">
                <div className="font-mono text-[11px] tracking-[0.14em] text-zinc-500 dark:text-zinc-400 uppercase">
                  Why Mono
                </div>
              </div>

              <div className="mt-8 grid grid-cols-1 gap-px border-t border-zinc-200 dark:border-zinc-800 bg-zinc-200 dark:bg-zinc-800/70 sm:grid-cols-2 lg:grid-cols-3">
                <div className="bg-white dark:bg-[#121214] p-6 md:p-8">
                  <div className="flex items-center gap-2.5">
                    <Zap className="size-4 text-amber-500" />
                    <h3 className="text-sm font-medium">Thread-Safe Architecture</h3>
                  </div>
                  <p className="mt-2.5 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
                    PTY background read loops dispatch output chunks cleanly through an event queue onto the Tkinter main thread via scheduled polling, preventing GUI deadlocks.
                  </p>
                </div>

                <div className="bg-white dark:bg-[#121214] p-6 md:p-8">
                  <div className="flex items-center gap-2.5">
                    <Palette className="size-4 text-emerald-500" />
                    <h3 className="text-sm font-medium">256-Color & 24-Bit RGB</h3>
                  </div>
                  <p className="mt-2.5 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
                    Full support for standard 16 ANSI colors, xterm 256-color palettes, 24-bit Truecolor escapes, bold, and underline text styles.
                  </p>
                </div>

                <div className="bg-white dark:bg-[#121214] p-6 md:p-8">
                  <div className="flex items-center gap-2.5">
                    <MonitorCheck className="size-4 text-sky-500" />
                    <h3 className="text-sm font-medium">Dynamic PTY Resizing</h3>
                  </div>
                  <p className="mt-2.5 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
                    Automatically computes character rows and columns via font metrics on window resize and syncs to the PTY via setwinsize, avoiding truncated outputs.
                  </p>
                </div>

                <div className="bg-white dark:bg-[#121214] p-6 md:p-8">
                  <div className="flex items-center gap-2.5">
                    <Layers className="size-4 text-purple-500" />
                    <h3 className="text-sm font-medium">Tabbed Terminal Manager</h3>
                  </div>
                  <p className="mt-2.5 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
                    Ready-to-use <code>Terminals</code> container widget with tab controls, allowing multiple shells to run in separate concurrent instances.
                  </p>
                </div>

                <div className="bg-white dark:bg-[#121214] p-6 md:p-8">
                  <div className="flex items-center gap-2.5">
                    <Keyboard className="size-4 text-rose-500" />
                    <h3 className="text-sm font-medium">Keyboard First Shortcuts</h3>
                  </div>
                  <p className="mt-2.5 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
                    Native keyboard bindings for Ctrl+C interrupt signals, Ctrl+L terminal clears, and Ctrl+U line deletions for fluid terminal workflows.
                  </p>
                </div>

                <div className="bg-white dark:bg-[#121214] p-6 md:p-8">
                  <div className="flex items-center gap-2.5">
                    <Cpu className="size-4 text-orange-500" />
                    <h3 className="text-sm font-medium">Command Queue & Buffering</h3>
                  </div>
                  <p className="mt-2.5 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
                    Built-in <code>TerminalCommandQueue</code> lets you queue and execute commands sequentially without dropping inputs during startup delays.
                  </p>
                </div>
              </div>
            </section>

            {/* Quickstart Code Example */}
            <section className="border-t border-zinc-200 dark:border-zinc-800/80 px-5 py-14 md:px-10">
              <div className="font-mono text-[11px] tracking-[0.14em] text-zinc-500 dark:text-zinc-400 uppercase">
                Quick Example
              </div>
              <h2 className="mt-2 text-2xl font-semibold tracking-tight">Drop into any Tkinter app in 5 lines</h2>

              <div className="mt-6 max-w-2xl rounded-xl border border-zinc-200 dark:border-zinc-800 bg-zinc-950 p-5 font-mono text-xs text-zinc-200 overflow-x-auto">
                <pre>{`import tkinter as tk
from mono.shells import Default

root = tk.Tk()
root.title("My Terminal Window")

terminal = Default(root, cwd=".")
terminal.pack(fill="both", expand=True)

root.mainloop()`}</pre>
              </div>
            </section>

            {/* FAQ Section matching waku.sh style */}
            <section className="border-t border-zinc-200 dark:border-zinc-800/80 px-5 py-14 md:px-10">
              <div className="font-mono text-[11px] tracking-[0.14em] text-zinc-500 dark:text-zinc-400 uppercase">
                Questions
              </div>

              <div className="flex w-full flex-col mt-6 max-w-2xl border-t border-zinc-200 dark:border-zinc-800">
                {[
                  {
                    q: "What platforms are supported?",
                    a: "Mono runs natively on Windows (using winpty) and Linux/macOS (using ptyprocess), giving you consistent terminal behavior across operating systems."
                  },
                  {
                    q: "Can I add custom shells or REPLs?",
                    a: "Yes! Any shell or command can be wrapped by subclassing Terminal, defining self.shell and registering it in mono.shells."
                  },
                  {
                    q: "Can I embed Mono into existing Tkinter apps?",
                    a: "Mono is built directly on ttk.Frame and tk.Text, making it an ordinary Tkinter widget that can be packed, gridded, or docked inside any layout."
                  },
                  {
                    q: "How does Mono handle terminal clears like cls and clear?",
                    a: "Mono detects ANSI VT100 erase sequences (\x1b[2J and \x1b[3J) produced by shells and immediately invokes the widget clear routine."
                  }
                ].map((item, idx) => (
                  <div key={idx} className="border-b border-zinc-200 dark:border-zinc-800">
                    <button
                      onClick={() => setOpenFaq(openFaq === idx ? null : idx)}
                      className="flex w-full items-center justify-between py-4 text-left font-medium text-[15px] hover:text-amber-500 transition-colors"
                    >
                      <span>{item.q}</span>
                      {openFaq === idx ? (
                        <ChevronUp className="size-4 text-zinc-400 shrink-0 ml-4" />
                      ) : (
                        <ChevronDown className="size-4 text-zinc-400 shrink-0 ml-4" />
                      )}
                    </button>
                    {openFaq === idx && (
                      <p className="pb-4 text-sm text-zinc-600 dark:text-zinc-400 leading-relaxed">
                        {item.a}
                      </p>
                    )}
                  </div>
                ))}
              </div>
            </section>
          </main>
        </div>

        {/* Footer */}
        <footer className="flex items-center justify-between border-t border-zinc-200 dark:border-zinc-800/80 px-5 py-8 text-xs text-zinc-500 md:px-10">
          <div className="flex items-center gap-2">
            <div className="size-3.5 rounded-[4px] bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-[8px] text-amber-500 font-mono">
              M
            </div>
            <span>© 2026 Mono Project — MIT License</span>
          </div>

          <div className="flex items-center gap-4">
            <a
              href="https://github.com/tomlin7/mono"
              target="_blank"
              rel="noreferrer"
              className="hover:text-zinc-900 dark:hover:text-zinc-100 flex items-center gap-1"
            >
              <span>GitHub</span>
              <ExternalLink className="size-3" />
            </a>
          </div>
        </footer>
      </div>
    </div>
  )
}
