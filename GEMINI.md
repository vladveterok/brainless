# Gemini Engagement Rules

This document outlines the rules and procedures for our collaboration on the shuka.app project. Please adhere to these rules in all your responses and actions.

## 1. Explicit Permission Required for Code Changes

You must not write, modify, or delete any code without first obtaining explicit permission from me. Before you intend to make any change, you must state what you are about to do and ask for confirmation to proceed.

**Example:**
*   **You:** "I am now ready to write the `Dockerfile` for our development environment. Shall I proceed?"
*   **Me:** "Yes, proceed."

## 2. One Step at a Time

Adhere to project structure described here: project_development_and_structure_rules.md

We will follow the phase documentation step-by-step.

*   Do not start a new step until the previous one is complete and confirmed.
*   The status of a step (e.g., `In Progress`, `To Do`) will only be changed with explicit permission.
*   At the beginning of each step, you must state which step you are starting.
*   After completing a step, you must create a summary document detailing what was done.

## 3. Testing and Issue Tracking

*   **Testing:** After each step that results in a functional change, you should propose a simple way to test it.
*   **Bug/Issue Identification:** If a test fails or an issue is discovered, we will create a ticket.
*   **Ticket Format:** A ticket will be a new `.md` file in a `docs/tickets` directory. The filename will be `TICKET-XXX.md` (e.g., `TICKET-001.md`). The ticket must contain:
    *   **Title:** A brief description of the issue.
    *   **Status:** `Open`, `In Progress`, `Resolved`, `Closed`.
    *   **Description:** A detailed explanation of the bug and how to reproduce it.
    *   **Fix History:** A log of all attempts to fix the issue. Each entry should include the proposed solution and the result (e.g., "Success", "Failed - caused another issue").

## 4. No Assumptions

Your implementation strategies must be based on verifiable information.

*   **Source of Truth:** Your decisions should be grounded in:
    1.  The existing code within this project.
    2.  The documentation we have created.
    3.  Information gathered from reliable internet sources (e.g., official library documentation, well-regarded technical blogs).
*   **Clarification:** If you are unsure how to proceed or face an ambiguous choice, you must ask for clarification rather than making a guess.

## 5. Development Principles

To ensure high-quality, maintainable code, we will adhere to the following principles:

*   **Modular Design:** Implement features using a modular, service-oriented approach. Each distinct logical service should reside in its own file, class, or module.
*   **Single Responsibility Principle (SRP):** Ensure each service, class, or module has one, and only one, reason to change.
*   **Pragmatic Principles:** Adhere to SOLID and KISS principles where they genuinely improve code quality and maintainability without over-engineering. Avoid dogmatic application.

## 6. Communication Style

*   **No Metaphors:** Avoid using metaphors, unnecessary colorful language, or colloquialisms (e.g., "The Brain", "The Radar").
*   **Factual & Concrete:** Providing explanations that are strictly technical, factual, and concrete.
*   **Directness:** Focus on explaining *what* something does and *how* it works logically/technically, rather than using imaginative descriptions.

## 6. Security & Configuration Rules

*   **No Hardcoded Secrets:** ALL secrets (API keys, DB passwords, Tokens) and environment-specific configuration MUST be stored in `.env` files.
*   **Docker Prohibition:** NEVER define secrets inside `docker-compose.yml` (environment blocks) or `Dockerfile` (ENV instructions). Always use `env_file` directives or runtime injection.
*   **Validation:** Use libraries like `pydantic-settings` to strictly validate that all required variables are present at startup.
*   **Clean Code:** Remove all temporary solutions, non-working fixes, and debugging code as soon as they are no longer necessary.
* **Scalability:** Every service / business process shuld be easilty scalable and configurable. Whenever we need to scale some aspect of our service, we need to be able to configure it rather then re-write it.
* **No Lazy Workarounds:** Quick hacks (e.g., copying files instead of mounting/packaging, hardcoding secrets, skipping error handling) are **STRICTLY PROHIBITED**. Every solution must be implemented as if it were going to production immediately.

## 6. Tool Usage

*   To read files, use the `read_file` tool.
*   To read the contents of a directory, use the `list_directory` tool.
*   To write new files, use the `write_file` tool.
*   To edit existing files, use the `replace` tool.

## 8. Setup Scripts
*   **Always use project-specific setup scripts** (e.g., `./scripts/setup_host.sh`) instead of generic commands like `pip install -r requirements.txt` when setting up or updating environments, as they contain critical patches (e.g., for Apple Silicon).

## 7. Communication Style

*   Do not generate apologies in your responses. Acknowledge the error and state the correction.

## 9. Write-Lock Protocol (Zero Tolerance)

To ensure 100% compliance with Rule #1, you will strictly adhere to this protocol:

1.  **Default Lock:** Treat all file-modification tools (`write_file`, `replace`, `run_in_terminal`) as **locked** by default.
2.  **The "Unlock" Check:** Before calling any of these tools, check the user's **immediately preceding message**.
    *   **If** it contains explicit confirmation (e.g., "Yes", "Proceed", "Do it"), you may execute.
    *   **If** it contains only feedback, instructions, or questions, you must **STOP**.
3.  **The Proposal Output:** Instead of acting, output the specific changes you intend to make and end your response with: **"Shall I proceed?"**
4.  **Zero Inference:** Strictly ignore implied intent. Even if a task seems obvious, do not execute it without the specific "Unlock" keyword.

## Project development and structure rules

- Project development is split into phases. Each phase dedicated for implementation of one feature or one atomic part of a feture. Project development should be as granulated as possible to ensure the development transparency and enable to developers to step back whenever it is needed and re-iterate without loosing too much of a progress.

- Project development plan should be described phase by phase in details and code snippets if needed in documentation/development/development_plan.md. When any phase is completed, its status shuold be updated in this document.

- Project development progress should be tracked in a main development progress document documentation/development/development_progress.md. Here each phase sohuld be mantioned and have a status up to date.

- Status of each phase is changed ONLY after explicit permission.

- Each phase starts and ends with explicit permission that llm agent should ask and receive.

- Each phase should start with creation of a phase development document inside documentation/development/phase_{number_of_phase}_{name_of_phase}/development_plan.md. The development_plan.md should contain a name of a phase, a status (ToDo, In Progress, Done) explicit step-by-step plan, and development history of this phase. If multiple attempts are taken to implement/debug/fix any aspect of the phase, these attempts and their resolutions should be described in the development history of this phase with the date/time stemp of teh attempt, desctription of the attempt, proposed plan and the result (success, failure, etc.)

- If bugs are identified during the phase implementation, bug_ticket file sohuld be created in a backlog in documentation/development/backlog/ directory. Ticket file should contain a bug uid, description, status, and fix history with every proposed solution, timestamp of attempt, and status (success, failure, ect).

- Each phase should end with updatgin the phase status in documentation/development/phase_{number_of_phase}_{name_of_phase}/development_plan.md, crearing a summary document documentation/development/phase_{number_of_phase}_{name_of_phase}/summary.md, updating the phase status in documentation/development/development_plan.md and in documentation/development/development_progress.md.

- **ZERO TECHNICAL DEBT & NO "MVP" SHORTCUTS POLICY**: 
  - ALWAYS choose the "Enterprise/Strict" implementation path by default. 
  - NEVER propose or implement "fast workarounds", "temporary fixes", or "MVP shortcuts" (like caching sensitive state in localStorage instead of validating with API) unless explicitly ordered to "do it quick and dirty". 
  - If a proper solution requires more steps (e.g., adding a validation endpoint), YOU MUST DO IT. Do not optimize for "saving time" at the cost of correctness or security.