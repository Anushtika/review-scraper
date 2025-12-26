# SaaS Review Scraper

A clean, CLI-based Python tool to scrape SaaS product reviews from multiple platforms
(G2, Capterra, TrustRadius) within a given date range.

Designed as a take-home assignment to demonstrate real-world scraping logic,
pagination handling, and production-oriented code structure.

## Why this project?

Scraping SaaS reviews involves real-world challenges such as:
- Platform-specific HTML structures
- Pagination with unknown page limits
- Rate limits and bot protection
- Inconsistent date formats

This project focuses on **design clarity and robustness**, not brute-force scraping.

## Design Decisions

- Modular scraper per source to allow easy extension
- Date-based early stopping to avoid unnecessary requests
- Unified output schema across all platforms
- Graceful failure handling instead of hard crashes
