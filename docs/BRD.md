# Business Requirements Document (BRD)

## CareerGraph AI

**Working Product Name:** CareerGraph AI  
**Project:** Patchamomma 2026 Build Phase  
**Document:** Business Requirements Document  
**Version:** 0.2  
**Date:** 16 August 2026  
**Status:** Draft  
**Repository:** Career-Intelligence-Platform

---

# 1. Executive Summary

CareerGraph AI is a data-driven, multi-agent AI platform designed to help Software Engineering candidates understand their current interview readiness, identify their highest-impact skill gaps, prepare strategically, and continuously evaluate their progress.

Software Engineering candidates today have access to an enormous amount of preparation material, including coding platforms, courses, videos, roadmaps, job descriptions, mock-interview platforms, professional communities, and AI assistants.

However, these resources are largely fragmented.

Candidates are often required to determine for themselves:

- What they should study.
- Which resources they should follow.
- Which skills are most important for their target role.
- Whether they actually understand a topic or can apply it independently.
- Whether their performance is improving.
- How much preparation is enough.
- Whether they are ready for a particular interview.

CareerGraph AI aims to address this gap by creating a continuous feedback loop between **career goals, candidate data, preparation activity, assessment performance, and interview simulation**.

The platform will initially focus on Software Engineering roles across **SDE-1, SDE-2, and SDE-3 levels**, while maintaining an architecture that can eventually be extended to other professional career domains.

---

# 2. Problem Statement

## 2.1 Background

Candidates preparing for Software Engineering interviews have abundant access to learning and preparation resources.

A typical candidate may use:

- LeetCode or other coding platforms for DSA.
- YouTube and courses for concepts.
- AI assistants for explanations.
- LinkedIn and online communities for career guidance.
- Job portals for job descriptions.
- Mock-interview platforms for practice.
- Multiple roadmaps created by different educators and professionals.

While this abundance of resources is useful, it can also create **information overload and fragmented preparation**.

Candidates may follow one roadmap for some time, discover another recommendation, switch to it, and continue without having a reliable understanding of whether the chosen approach is actually improving their interview readiness.

---

## 2.2 Core Problem

The fundamental problem is not the absence of preparation resources.

The problem is the absence of an intelligent system that continuously answers:

> **Where am I now?**

> **Where do I need to be for my target role?**

> **What are my most important gaps?**

> **What should I do next?**

> **Is my preparation actually improving my interview readiness?**

Current preparation workflows generally treat these activities independently.

For example:

```text
Resume
   ↓
Job Search

LeetCode
   ↓
DSA Practice

YouTube
   ↓
Learning

Mock Interview
   ↓
Interview Practice

AI Assistant
   ↓
Questions / Explanations
