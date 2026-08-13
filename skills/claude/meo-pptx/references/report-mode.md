# Report mode (進捗報告・課題検討会)

Load khi build deck báo cáo tiến độ / 課題検討会. Luật cứng về số liệu nằm ở §0.2 của SKILL.md.

---


Goal: agenda + important-topic slides for a progress meeting. **Progress/backlog data is
verified and entered by the user — this skill does NOT generate it.**

Allowed (Claude builds these), following the lean skeleton in §2:
- Cover (with agenda folded in).
- **重要トピック / 課題** explanation slides (same patterns as Technical mode — tables,
  flows, before/after) for qualitative topics that don't depend on unverified numbers.
- まとめ / 次のアクション.

For any progress/backlog/status table, insert a **placeholder slide**:
- Title + correctly formatted empty table (columns like 項目 | ステータス | 進捗 | 備考,
  `CCCCCC` borders, ice-blue header).
- Fill cells with a visible marker: `［要手動入力：verify済みデータ］`.
- Add a speaker-note / on-screen reminder: 「※進捗・課題の数値は手動で確認・入力すること」.
- **Never** auto-fill completion %, ticket counts, dates, or status flags.

When unsure whether data is "verified" → treat it as unverified and leave a placeholder.
