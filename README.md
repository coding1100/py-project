# Problem Processor

This project processes problem statements using OpenAI's GPT model to generate mutations based on given prompts. The results are saved in an output directory, and a leaderboard is maintained to track the highest-scoring problems.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Running Tests](#running-tests)
- [License](#license)

## Features

- Load problem statements from a text file.
- Mutate problems using OpenAI's API.
- Save processed problems in an output directory.
- Maintain a leaderboard of top problems based on scores.

## Requirements

- Docker
- Docker Compose
- Python 3.9+
- An OpenAI API key (Azure OpenAI service)

## Installation

### 1. Install Docker and Docker Compose

Follow the instructions for your operating system:

- **Windows/Mac**: Download and install [Docker Desktop](https://www.docker.com/products/docker-desktop).
- **Linux**: Install Docker by following the [official guide](https://docs.docker.com/engine/install/).

### 2. Clone the Repository

Clone the repository to your local machine:

```bash
git clone https://github.com/yourusername/problem-processor.git
cd problem-processor