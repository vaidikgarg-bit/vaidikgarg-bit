<p align="center">
  <b>Vaidik Garg</b><br>
  Student developer · Java server work &amp; full-stack web
</p>

I'm a student who builds full-stack web projects and sends fixes to open source projects. 3 merged upstream PRs so far, in Apache HugeGraph and Apache Fineract.

On Apache HugeGraph I work on the store layer: giving RocksDB's `BackendColumn` a hash code that matches its byte-based `equals()`, so intersection and union iterators stop treating identical rows as different, and stopping `ProjectionStage` from clearing a column that was still held as a dedup key, which let duplicate rows through on id-only scans. I reported that second bug as an issue before fixing it.

On the Apache Fineract back-office UI (Angular) I fixed client records that showed date-only fields as midnight timestamps in the viewer's time zone.

Outside upstream work I'm building Study Vault, a course notes hub with generated quizzes and flashcards, on FastAPI and SQLite with a Tailwind front end.

### Open-source pull requests

| Pull request | Repository | Status |
| --- | --- | --- |
| [test(store): cover the id-only projection through QueryUtil.buildPlan](https://github.com/apache/hugegraph/pull/3410) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![approved](https://img.shields.io/badge/approved-1a7f37?style=flat-square) |
| [feat(scheduler): edit a job's cron expression, name and active flag](https://github.com/apache/fineract-backoffice-ui/pull/838) | [apache/fineract-backoffice-ui](https://github.com/apache/fineract-backoffice-ui) | ![open](https://img.shields.io/badge/open-2da44e?style=flat-square) |
| [fix(store): stop ProjectionStage clearing dedup keys in place](https://github.com/apache/hugegraph/pull/3408) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [fix(store): hash BackendColumn by its name and value](https://github.com/apache/hugegraph/pull/3404) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [fix(clients): show activation and submitted dates without a time or zone](https://github.com/apache/fineract-backoffice-ui/pull/830) | [apache/fineract-backoffice-ui](https://github.com/apache/fineract-backoffice-ui) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |

### Issues I've reported

- [[Bug] Store limit dedup emits duplicates on id-only scans because ProjectionStage mutates the stored column](https://github.com/apache/hugegraph/issues/3407) in `apache/hugegraph` (closed)

### My projects

- [study-vault](https://github.com/vaidikgarg-bit/study-vault): 🎓 Campus Course Notes Hub & AI-powered Quiz and 3D Flashcard Study Engine built with FastAPI, SQLite, and Tailwind CSS. `Python`

<sub>The lists above are rebuilt from the GitHub API every six hours by
[a small script](scripts/update_readme.py).</sub>
