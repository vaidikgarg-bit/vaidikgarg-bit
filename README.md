<p align="center">
  <b>Vaidik Garg</b><br>
  Student developer · Java server work &amp; full-stack web
</p>

I'm a student who builds full-stack web projects and sends fixes to open source projects. 10 merged upstream PRs so far, in Apache HugeGraph and Apache Fineract.

On Apache HugeGraph I work on the store layer: giving RocksDB's `BackendColumn` a hash code that matches its byte-based `equals()`, so intersection and union iterators stop treating identical rows as different, and stopping `ProjectionStage` from clearing a column that was still held as a dedup key, which let duplicate rows through on id-only scans. I reported that second bug as an issue before fixing it.

On the Apache Fineract back-office UI (Angular) I fixed client records that showed date-only fields as midnight timestamps in the viewer's time zone.

Outside upstream work I'm building Study Vault, a course notes hub with generated quizzes and flashcards, on FastAPI and SQLite with a Tailwind front end.

### Open-source pull requests

| Pull request | Repository | Status |
| --- | --- | --- |
| [fix(clients): open the birth-date picker on the platform's month](https://github.com/apache/fineract-backoffice-ui/pull/864) | [apache/fineract-backoffice-ui](https://github.com/apache/fineract-backoffice-ui) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [feat(share-dividends): approve a dividend and view its per-account payout](https://github.com/apache/fineract-backoffice-ui/pull/852) | [apache/fineract-backoffice-ui](https://github.com/apache/fineract-backoffice-ui) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [fix(store): harden MultiListIterator close and next](https://github.com/apache/hugegraph/pull/3445) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![approved](https://img.shields.io/badge/approved-1a7f37?style=flat-square) |
| [fix(store): close sub-iter when MultiListIter closed early](https://github.com/apache/hugegraph/pull/3437) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [feat(external-services): configure the SMS message gateway](https://github.com/apache/fineract-backoffice-ui/pull/842) | [apache/fineract-backoffice-ui](https://github.com/apache/fineract-backoffice-ui) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [fix(store): keep pending rows in dedup iterators](https://github.com/apache/hugegraph/pull/3424) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [test(store): cover the id-only projection through QueryUtil.buildPlan](https://github.com/apache/hugegraph/pull/3410) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [feat(scheduler): edit a job's cron expression, name and active flag](https://github.com/apache/fineract-backoffice-ui/pull/838) | [apache/fineract-backoffice-ui](https://github.com/apache/fineract-backoffice-ui) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [fix(store): stop ProjectionStage clearing dedup keys in place](https://github.com/apache/hugegraph/pull/3408) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |
| [fix(store): hash BackendColumn by its name and value](https://github.com/apache/hugegraph/pull/3404) | [apache/hugegraph](https://github.com/apache/hugegraph) | ![merged](https://img.shields.io/badge/merged-8250df?style=flat-square) |

### Issues I've reported

- [[Bug] Store MultiListIterator leaks sub-iterators on close failure, NPEs on bare next(), and probes sources after close](https://github.com/apache/hugegraph/issues/3444) in `apache/hugegraph` (open)
- [[Store] LIMIT_DEDUP on NO_SCAN with loadPropertyFromIndex compares BaseVertex by reference](https://github.com/apache/hugegraph/issues/3443) in `apache/hugegraph` (open)
- [[Bug] Store MultiListIterator leaks its sub-iterators when closed before the first hasNext()](https://github.com/apache/hugegraph/issues/3436) in `apache/hugegraph` (closed)
- [[Bug] Store dedup iterators drop rows at query batch boundaries](https://github.com/apache/hugegraph/issues/3415) in `apache/hugegraph` (closed)
- [[Bug] Store limit dedup emits duplicates on id-only scans because ProjectionStage mutates the stored column](https://github.com/apache/hugegraph/issues/3407) in `apache/hugegraph` (closed)

### My projects

- [Hacktober-Fest](https://github.com/vaidikgarg-bit/Hacktober-Fest) `Python`
- [study-vault](https://github.com/vaidikgarg-bit/study-vault): 🎓 Campus Course Notes Hub & AI-powered Quiz and 3D Flashcard Study Engine built with FastAPI, SQLite, and Tailwind CSS. `Python`

<sub>The lists above are rebuilt from the GitHub API every six hours by
[a small script](scripts/update_readme.py).</sub>
