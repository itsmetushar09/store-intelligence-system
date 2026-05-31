# Store Intelligence System

## Overview

An AI-powered Store Intelligence Platform that analyzes CCTV footage to generate business insights such as footfall, customer movement, zone popularity, and operational anomalies.

## Features

- Person Detection (YOLOv8)
- Multi-Object Tracking (ByteTrack)
- Entry/Exit Counting
- Zone Analytics
- Event Generation
- REST APIs
- Streamlit Dashboard
- SQLite Event Storage

## Architecture

CCTV Cameras
↓
YOLOv8
↓
ByteTrack
↓
Event Generator
↓
SQLite Database
↓
FastAPI
↓
Streamlit Dashboard

## APIs

GET /metrics

GET /events

GET /analytics

GET /anomalies

GET /heatmap



