# Case Study: Natural Language CRM Access for Medical Recruitment Agency

**Instant answers to complex recruitment questions—powered by AI and Bullhorn CRM integration.**

---

## Overview

A specialist medical recruitment agency needed faster access to critical business data locked inside their Bullhorn CRM. Consultants and managers were spending valuable time navigating complex interfaces and running manual reports instead of placing candidates.

Osher Digital built an open-source MCP (Model Context Protocol) server that connects AI assistants directly to Bullhorn's live data. Team members now ask questions in plain English and receive instant, accurate answers—transforming how the agency accesses and acts on their recruitment intelligence.

---

## About the Client

One of Australia's leading medical recruitment agencies specialising in placing doctors, nurses, and allied health professionals into locum and permanent positions across public and private healthcare facilities nationwide.

The agency manages thousands of active candidates, hundreds of open job orders, and complex placement workflows through Bullhorn CRM—the industry-standard applicant tracking system for recruitment.

---

## The Problem

Despite having comprehensive data in Bullhorn, accessing meaningful insights was frustratingly slow and technical.

**Consultants faced daily friction:**

- Finding suitable candidates for urgent roles required multiple search filters, Boolean queries, and manual cross-referencing across screens
- Answering simple questions like "Who are our most recent cardiologist applicants in Sydney?" meant navigating three or four different views
- Managers requesting performance data had to wait for manually compiled reports or export data to spreadsheets for analysis
- The Bullhorn interface, while powerful, demanded training and expertise that not all team members possessed

**The business impact was significant:**

- Senior consultants spent up to 45 minutes per day on data retrieval tasks instead of client and candidate engagement
- Response times to urgent client requests suffered when the right information wasn't immediately accessible
- Junior staff frequently interrupted experienced consultants with "how do I find..." questions
- Strategic decisions were delayed waiting for data that existed but wasn't easily extractable

The agency explored third-party reporting tools and Bullhorn add-ons, but these added cost, complexity, and still required users to learn new interfaces.

---

## The Solution

Osher Digital developed a Python-based MCP server that acts as a bridge between AI assistants and the Bullhorn REST API. The solution is open-source and available at [github.com/osherai/bullhorn-mcp-python](https://github.com/osherai/bullhorn-mcp-python).

**How it works:**

The MCP server authenticates securely with Bullhorn using OAuth 2.0 and exposes the CRM data through a standardised protocol that AI assistants understand natively. Team members interact with their data through natural conversation—no training required.

**Technical implementation:**

- **Direct API integration** — Connects to Bullhorn's REST API without expensive middleware or per-seat licensing
- **OAuth 2.0 authentication** — Secure token-based access with automatic refresh
- **Read-only by design** — Zero risk of accidental data modification
- **Six powerful query tools** — Search jobs, search candidates, retrieve details, and run complex queries
- **Universal compatibility** — Works with Claude Desktop, Cursor, VS Code extensions, and any MCP-compatible client

**Example queries the team now runs instantly:**

| Question | What it retrieves |
|----------|-------------------|
| "Who is the top performing recruitment consultant in the last 12 months?" | Placement data aggregated by owner, ranked by volume and value |
| "Who are the most recent cardiologists who have applied in Sydney?" | Candidates filtered by specialty, location, and application date |
| "What are our current open jobs?" | Active job orders sorted by date added |
| "Who are the best candidates for job #7024?" | Candidates matched by skills, availability, and location to a specific role |
| "Show me all placements made last quarter" | Placement records within date range with candidate and job details |
| "Which clients have the most open positions right now?" | Job orders grouped by client corporation |

**Deployment:**

The server runs locally alongside the AI assistant, keeping all data within the organisation's existing security perimeter. No cloud processing of sensitive candidate or client information.

---

## The Results

**Immediate time savings:**

- Data retrieval tasks reduced from 5-10 minutes to under 10 seconds
- Consultants reclaimed 30-45 minutes daily for revenue-generating activities
- Managers get real-time answers to performance questions without waiting for reports

**Operational improvements:**

- Junior staff independently find information without interrupting colleagues
- Faster response to urgent client requests—candidate shortlists generated in minutes, not hours
- Consistent, accurate data across all queries (no more conflicting spreadsheet versions)

**Strategic benefits:**

- Leadership gained on-demand visibility into pipeline health and team performance
- Data-driven decisions made in meetings rather than deferred for "further analysis"
- Competitive advantage through faster candidate submissions to clients

**Cost efficiency:**

- Zero per-seat licensing fees (open-source solution)
- No additional SaaS subscriptions required
- Deployed on existing infrastructure with minimal IT overhead

---

## Technology Stack

| Component | Purpose |
|-----------|---------|
| Python 3.10+ | Core server implementation |
| MCP SDK | Model Context Protocol for AI integration |
| Bullhorn REST API | Direct CRM data access |
| OAuth 2.0 | Secure authentication |
| httpx | Async HTTP client |

---

## Open Source

This solution is released as open-source software under the MIT License, available to the recruitment industry at no cost.

**Repository:** [github.com/osherai/bullhorn-mcp-python](https://github.com/osherai/bullhorn-mcp-python)

We believe recruitment agencies of all sizes should have access to modern AI-powered tools without prohibitive licensing costs. The project welcomes contributions from the community.

---

## About Osher Digital

[Osher Digital](https://osher.com.au) is a specialist AI consultancy helping businesses harness artificial intelligence to streamline operations and unlock new capabilities.

We design and build practical AI solutions—from automation workflows to custom integrations—that deliver measurable ROI without enterprise complexity.

**Ready to transform how your team accesses critical business data?**

[Get in touch →](https://osher.com.au/contact/)
