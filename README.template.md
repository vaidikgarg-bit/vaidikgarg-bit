<!-- Generated from README.template.md by scripts/update_readme.py. Edit the template, not this file. -->
<div align="center">

# Vaidik Garg

Student developer · Java server work &amp; full-stack web

</div>

I'm a student who builds full-stack web projects and sends fixes to open source projects. **{{ MERGED_COUNT }}** so far, in Apache HugeGraph and Apache Fineract.

On [Apache HugeGraph](https://github.com/apache/hugegraph) I work on the store layer: giving RocksDB's `BackendColumn` a hash code that matches its byte-based `equals()`, so intersection and union iterators stop treating identical rows as different, and stopping `ProjectionStage` from clearing a column that was still held as a dedup key, which let duplicate rows through on id-only scans. I reported that second bug as an issue before fixing it.

On the [Apache Fineract back-office UI](https://github.com/apache/fineract-backoffice-ui) (Angular) I fixed client records that showed date-only fields as midnight timestamps in the viewer's time zone.

Outside upstream work I'm building [Study Vault](https://github.com/vaidikgarg-bit/study-vault), a course notes hub with generated quizzes and flashcards, on FastAPI and SQLite with a Tailwind front end.

## Upstream work

{{ UPSTREAM_TABLE }}

## Open PRs

Open pull requests in upstream projects (refreshed automatically).

{{ OPEN_PRS }}

## Stats

<p align="center">
  <img src="assets/stats.svg" alt="Upstream contribution stats"/>
  <img src="assets/languages.svg" alt="Languages in my pull requests"/>
</p>

## Tools

Java · Python · TypeScript · JavaScript · Angular · FastAPI · SQLite · RocksDB · Tailwind CSS · HTML/CSS · GitHub Actions · Git

---

<sub>Auto-updated {{ UPDATED }} · [workflow](.github/workflows/update-readme.yml)</sub>
