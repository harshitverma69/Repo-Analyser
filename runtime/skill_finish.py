"""Post-skill hook: display report in the terminal (no file writes by default)."""

from __future__ import annotations

import sys
from pathlib import Path

from runtime.report_renderer import export_run_markdown, export_skill_markdown, find_skill_json, load_skill_payload
from runtime.report_ui import render_terminal_ui

ROOT = Path(__file__).resolve().parent.parent
GENERATED_ROOT = ROOT / "generated_projects"


def show_skill_report(
    run_dir: Path,
    skill_id: str,
    *,
    save_md: bool = False,
    interactive: bool = False,
) -> int:
    """Render a skill report to the terminal. Markdown files are opt-in only."""
    skill_id = skill_id.upper()
    skill_dir = run_dir / skill_id
    json_path = find_skill_json(skill_dir)

    if json_path is None:
        print(f"No output found for {skill_id} in {run_dir.name}", file=sys.stderr)
        print(f"Expected JSON under: {skill_dir}/", file=sys.stderr)
        return 1

    if save_md:
        try:
            export_skill_markdown(skill_dir)
            export_run_markdown(run_dir)
        except Exception as exc:
            print(f"Warning: markdown export failed: {exc}", file=sys.stderr)

    task_id, payload = load_skill_payload(skill_dir)
    print(render_terminal_ui(run_dir.name, task_id or skill_id, payload, run_dir=run_dir))

    if not interactive:
        return 0

    return _interactive_menu(run_dir, skill_id)


def _interactive_menu(run_dir: Path, skill_id: str) -> int:
    from runtime.report_cli import interactive_loop, list_skills

    print("\n" + "─" * 62)
    print("  [Enter] menu   [r] refresh   [b] browse runs   [q] quit")
    while True:
        try:
            raw = input("\n> ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            return 0

        if raw in {"q", "quit", "exit"}:
            print("Bye.")
            return 0
        if raw in {"r", "refresh"}:
            return show_skill_report(run_dir, skill_id, interactive=True)
        if raw in {"b", "browse"}:
            return interactive_loop(GENERATED_ROOT)
        if raw in {"", "m", "menu"}:
            while True:
                print("\n── What next? ──")
                print("  1. View this report again")
                print("  2. Browse all skills in this run")
                print("  3. Open full run browser")
                print("  4. Quit")
                try:
                    choice = input("Choice [1-4]: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nBye.")
                    return 0
                if choice in {"1", "r"}:
                    show_skill_report(run_dir, skill_id, interactive=False)
                elif choice == "2":
                    skills = list_skills(run_dir)
                    for index, (sid, jp) in enumerate(skills, start=1):
                        marker = "✓" if jp else "·"
                        print(f"  {index}. [{marker}] {sid}")
                    pick = input("Skill number (blank=back): ").strip()
                    if pick.isdigit() and 1 <= int(pick) <= len(skills):
                        show_skill_report(run_dir, skills[int(pick) - 1][0], interactive=False)
                elif choice == "3":
                    return interactive_loop(GENERATED_ROOT)
                elif choice in {"4", "q", ""}:
                    break
            continue
        print("  Unknown command. Try Enter, r, b, q.")


def finish_skill(run_id: str, skill_id: str, *, generated_root: Path | None = None) -> int:
    """Display the report for a completed skill run (terminal only)."""
    root = generated_root or GENERATED_ROOT
    run_dir = root / run_id
    if not run_dir.is_dir():
        print(f"Run directory not found: {run_dir}", file=sys.stderr)
        return 1
    return show_skill_report(run_dir, skill_id.upper())


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Display CAC-OS skill report in the terminal")
    parser.add_argument("--run-id", required=True, help="Run directory name, e.g. master-mapping")
    parser.add_argument("--skill", required=True, help="Skill ID, e.g. B1")
    parser.add_argument("--save-md", action="store_true", help="Also write output.md files (off by default)")
    parser.add_argument("--interactive", action="store_true", help="Enter interactive menu after display")
    args = parser.parse_args(argv)

    run_dir = GENERATED_ROOT / args.run_id
    return show_skill_report(
        run_dir,
        args.skill.upper(),
        save_md=args.save_md,
        interactive=args.interactive,
    )


if __name__ == "__main__":
    raise SystemExit(main())
