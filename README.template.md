# Vaidik Garg

Student developer · Java server work & full-stack web

I'm a student who builds full-stack web projects and sends fixes to open source projects. {{ MERGED_COUNT }} so far, in Apache HugeGraph and Apache Fineract.

On Apache HugeGraph I work on the store layer: giving RocksDB's `BackendColumn` a hash code that matches its byte-based `equals()`, so intersection and union iterators stop treating identical rows as different, and stopping `ProjectionStage` from clearing a column that was still held as a dedup key, which let duplicate rows through on id-only scans. I reported that second bug as an issue before fixing it.

On the Apache Fineract back-office UI (Angular) I fixed client records that showed date-only fields as midnight timestamps in the viewer's time zone.

Outside upstream work I'm building Study Vault, a course notes hub with generated quizzes and flashcards, on FastAPI and SQLite with a Tailwind front end.

### Open-source pull requests

{{ OPEN_SOURCE_PRS }}

### Issues I've reported

{{ OPEN_SOURCE_ISSUES }}

### My projects

{{ PROJECTS }}

<sub>The lists above are rebuilt from the GitHub API every six hours by
[a small script](scripts/update_readme.py).</sub>
