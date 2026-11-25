from __future__ import annotations

from typing import Callable

from bcsfe import core
from bcsfe.cli.edits import map as map_edits

# Story chapters (eoc / itf / cotc) always have 48 stages and a single star.
STORY_STAGES = 48


def _stage_count(stage: object) -> int:
    """Get the clear count of a stage, whatever chapter type it came from."""
    count = getattr(stage, "clear_times", None)
    if count is None:
        count = getattr(stage, "clear_amount", 0)
    return int(count or 0)


def _total_stars(chapters: map_edits.ChaptersType, map_id: int, type: int | None) -> int:
    try:
        if isinstance(chapters, core.EventChapters):
            if type is None:
                raise ValueError("Type must be specified for EventChapters!")
            # get_total_stars falls back to the first map type when the index
            # is out of range, so check it ourselves to avoid clearing a map
            # type that doesn't exist in this save.
            if type >= len(chapters.chapters):
                return 0
            return chapters.get_total_stars(type, map_id)
        return chapters.get_total_stars(map_id)
    except (IndexError, AttributeError):
        return 0


def _total_stages(
    chapters: map_edits.ChaptersType, map_id: int, star: int, type: int | None
) -> int:
    try:
        if isinstance(chapters, core.EventChapters):
            if type is None:
                raise ValueError("Type must be specified for EventChapters!")
            if type >= len(chapters.chapters):
                return 0
            return chapters.get_total_stages(type, map_id, star)
        return chapters.get_total_stages(map_id, star)
    except (IndexError, AttributeError):
        return 0


def _clear_chapters(
    chapters: map_edits.ChaptersType, clear_amount: int, type: int | None = None
) -> int:
    """Clear every stage of every chapter, keeping any higher clear count.

    Returns the amount of stages that were cleared.
    """
    cleared = 0
    for map_id in range(map_edits.get_total_maps(chapters)):
        for star in range(_total_stars(chapters, map_id, type)):
            for stage in range(_total_stages(chapters, map_id, star, type)):
                map_edits.clear_stage(
                    chapters,
                    map_id,
                    star,
                    stage,
                    clear_amount,
                    type=type,
                    ensure_cleared_only=True,
                )
                cleared += 1
    return cleared


def _count_chapters(
    chapters: map_edits.ChaptersType, type: int | None = None
) -> tuple[int, int]:
    cleared = 0
    total = 0
    for map_id in range(map_edits.get_total_maps(chapters)):
        for star in range(_total_stars(chapters, map_id, type)):
            for stage in range(_total_stages(chapters, map_id, star, type)):
                total += 1
                try:
                    if isinstance(chapters, core.EventChapters):
                        if type is None:
                            raise ValueError
                        chapter = chapters.chapters[type].chapters[map_id].chapters[star]
                    else:
                        chapter = chapters.chapters[map_id].chapters[star]
                    if _stage_count(chapter.stages[stage]):
                        cleared += 1
                except (IndexError, AttributeError):
                    continue
    return cleared, total


def clear_story(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    """Clear eoc / itf / cotc."""
    chapters = save_file.story.get_real_chapters()
    cleared = 0
    for chapter in chapters:
        clear_times = [
            max(_stage_count(stage), clear_amount)
            for stage in chapter.stages[:STORY_STAGES]
        ]
        chapter.apply_progress(STORY_STAGES, clear_times)
        cleared += len(clear_times)
    return cleared


def count_story(save_file: core.SaveFile) -> tuple[int, int]:
    chapters = save_file.story.get_real_chapters()
    cleared = 0
    total = 0
    for chapter in chapters:
        for stage in chapter.stages[:STORY_STAGES]:
            total += 1
            if _stage_count(stage):
                cleared += 1
    return cleared, total


def _clear_sol(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.event_stages, clear_amount, type=0)


def _clear_events(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.event_stages, clear_amount, type=1)


def _clear_collab(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.event_stages, clear_amount, type=2)


def _clear_uncanny(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.uncanny.chapters, clear_amount)


def _clear_catamin(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.catamin_stages.chapters, clear_amount)


def _clear_legend_quest(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.legend_quest, clear_amount)


def _clear_towers(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.tower.chapters, clear_amount)


def _clear_gauntlets(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.gauntlets, clear_amount)


def _clear_collab_gauntlets(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.collab_gauntlets, clear_amount)


def _clear_enigma(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.enigma_clears, clear_amount)


def _clear_behemoth(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.behemoth_culling, clear_amount)


def _clear_zero_legends(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    chapters = save_file.zero_legends
    cleared = _clear_chapters(chapters, clear_amount)
    # zero legends reads/writes `unlock_state` rather than
    # `chapter_unlock_state`, so clear_stage never actually unlocks the next
    # chapter. Do it here so the cleared chapters are playable in-game.
    for chapters_stars in chapters.chapters:
        for chapter in chapters_stars.chapters:
            if chapter.stages:
                chapter.unlock_state = max(chapter.unlock_state, 3)
    return cleared


def _clear_catclaw(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    return _clear_chapters(save_file.dojo_chapters, clear_amount)


def _clear_aku(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    cleared = 0
    for chapters_stars in save_file.aku.chapters:
        for chapter in chapters_stars.chapters:
            for stage in chapter.stages:
                stage.clear_stage(max(_stage_count(stage), clear_amount))
                cleared += 1
            chapter.current_stage = max(chapter.current_stage, len(chapter.stages))
    return cleared


CLEAR_TARGETS: list[tuple[str, Callable[[core.SaveFile, int], int]]] = [
    ("story", clear_story),
    ("sol", _clear_sol),
    ("event", _clear_events),
    ("collab", _clear_collab),
    ("uncanny", _clear_uncanny),
    ("catamin_stages", _clear_catamin),
    ("legend_quest", _clear_legend_quest),
    ("towers", _clear_towers),
    ("gauntlets", _clear_gauntlets),
    ("collab_gauntlets", _clear_collab_gauntlets),
    ("enigma_stages", _clear_enigma),
    ("behemoth_culling", _clear_behemoth),
    ("zero_legends", _clear_zero_legends),
    ("dojo_catclaw_championships", _clear_catclaw),
    ("aku_chapters", _clear_aku),
]


def clear_all_stages(save_file: core.SaveFile, clear_amount: int = 1) -> int:
    cleared = 0
    for _, clear_func in CLEAR_TARGETS:
        cleared += clear_func(save_file, clear_amount)
    return cleared


def count_all_stages(save_file: core.SaveFile) -> tuple[int, int]:
    cleared, total = count_story(save_file)
    for _, attr in [
        ("sol", (save_file.event_stages, 0)),
        ("event", (save_file.event_stages, 1)),
        ("collab", (save_file.event_stages, 2)),
        ("uncanny", (save_file.uncanny.chapters, None)),
        ("catamin_stages", (save_file.catamin_stages.chapters, None)),
        ("legend_quest", (save_file.legend_quest, None)),
        ("towers", (save_file.tower.chapters, None)),
        ("gauntlets", (save_file.gauntlets, None)),
        ("collab_gauntlets", (save_file.collab_gauntlets, None)),
        ("enigma_stages", (save_file.enigma_clears, None)),
        ("behemoth_culling", (save_file.behemoth_culling, None)),
        ("zero_legends", (save_file.zero_legends, None)),
        ("dojo_catclaw_championships", (save_file.dojo_chapters, None)),
    ]:
        chapters, type = attr
        c, t = _count_chapters(chapters, type=type)  # type: ignore[arg-type]
        cleared += c
        total += t

    for chapters_stars in save_file.aku.chapters:
        for chapter in chapters_stars.chapters:
            for stage in chapter.stages:
                total += 1
                if _stage_count(stage):
                    cleared += 1

    return cleared, total
